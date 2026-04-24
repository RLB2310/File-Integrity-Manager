# Authored and hand-coded by Rylan B
import sqlite3
import hashlib
import os, time
from pathlib import Path
import configparser
import subprocess


# Function to walk through the disk, grabbing file paths. These paths will be used as the keys, with hashing used to obtain the values.
def file_traverse(path):
    files_list = []
    print("Grabbing files...")
    config = configparser.ConfigParser()
    config.read("config.ini")
    excludes_str = config.get("SETTINGS", "excludes", fallback=None)
    if excludes_str != None:
        excludes = [os.path.normpath(e.strip()) for e in excludes_str.split(",")]
    else:
        excludes = []
    for root, dirs, files in os.walk(path):
        for d in list(dirs):
            full_dir_path = os.path.join(root, d)
            if full_dir_path in excludes:
                dirs.remove(d)
        for f in files:
            print(os.path.join(root, f))
            if os.path.isfile(os.path.join(root, f)):
                files_list.append((os.path.join(root, f)))

    return files_list


# MD5 Hash creation
def hashing():
    config = configparser.ConfigParser()
    config.read("config.ini")
    target_dir = config.get("SETTINGS", "target", fallback="Test_dir").strip('"')

    # Easier to use a list, and pass through a dict for SQL integration
    hash_dict = []

    # Now call it
    files_list = file_traverse(target_dir)

    print("Beginning hashing...")
    for file in files_list:
        try:
            with open(Path(file), "rb") as file_obj:
                if file_obj:
                    file_contents = file_obj.read()
                    md5_hash = hashlib.md5(file_contents).hexdigest()
                    print(f"File: {file}, Hash: {md5_hash}")
                    hash_dict.append({"filepath": file, "hash": md5_hash})
        except (FileNotFoundError, OSError):
            pass
    return hash_dict


# Database function
def database(dictionary):
    # wrap the database transactions in a connection
    with sqlite3.connect("Hash.db") as connection:
        cursor = connection.cursor()

        # Intialise the table, check if exists
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS files ( filepath TEXT PRIMARY KEY, hash TEXT NOT NULL ) """
        )

        connection.commit()

        # Grab the file count in db before to compare later
        pre_file_count = cursor.execute(""" SELECT COUNT(*) FROM files""")
        pre_file_count = int(str(pre_file_count.fetchall()[0])[1:-2])
        cursor.execute(""" SELECT filepath, hash FROM files """)
        db_pre_state = {row[0]: row[1] for row in cursor.fetchall()}
        connection.commit()
        sql = """ INSERT OR REPLACE INTO files (filepath, hash)
        VALUES (:filepath, :hash)
        """
        cursor.executemany(sql, dictionary)
        connection.commit()

        # Grab the post-transaction file count in db after
        post_file_count = cursor.execute(""" SELECT COUNT(*) FROM files""")
        post_file_count = int(str((post_file_count.fetchall()[0]))[1:-2])
    # End connection to db
    connection.close()

    # Return changed file count
    return db_pre_state, post_file_count - pre_file_count


def file_alerts(db_pre_state, dict):
    new_files = []
    changed_files = []
    for file_data in dict:
        # loop through lists in dict
        filepath = file_data["filepath"]
        pre_hash = file_data["hash"]
        if filepath not in db_pre_state:
            # It's a new file
            new_files.append(filepath)
        elif db_pre_state[filepath] != pre_hash:
            # It's changed
            changed_files.append(filepath)
    config = configparser.ConfigParser()
    config.read("config.ini")
    notification_toggle = config.get("SETTINGS", "noti", fallback="False")
    notification_server = config.get("SETTINGS", "server", fallback=None)
    if notification_toggle == "True":
        if len(changed_files) > 0:
            print(changed_files)
            subprocess.run(
                [
                    "curl",
                    "-d",
                    f"FIM: Files have been changed: {changed_files}",
                    notification_server,
                ]
            )


if __name__ == "__main__":
    print("""
░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████████████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
    File Integrity Manager By Rylan                          """)

    print()
    print("Loading timer for performance measuring...")
    time.sleep(1)
    start = time.time()

    print("Ready")
    print("----------")
    dic = hashing()
    print("Hashing complete.")
    print()
    print("Updating database...")
    db_pre_state, file_count = database(dic)
    print("Database updated")
    file_alerts(db_pre_state, dic)
    end = time.time()
    print("Time: ", end - start)
