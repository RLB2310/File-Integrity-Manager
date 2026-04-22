# Authored and hand-coded by Rylan B
import sqlite3
import hashlib
import os, time
from pathlib import Path


# Function to walk through the disk, grabbing file paths. These paths will be used as the keys, with hashing used to obtain the values.
def file_traverse(path):
    files_list = []
    print("Grabbing files...")
    for root, dirs, files in os.walk(path):
        for f in files:
            files_list.append((os.path.join(root, f)))

    return files_list


# MD5 Hash creation
def hashing():
    # Directory used: current is testing
    files_list = file_traverse("/home/rylan/Test_dir/")
    # Easier to use a list, and pass through a dict for SQL integration
    hash_dict = []
    for file in files_list:
        with open(Path(file), "rb") as file_obj:
            file_contents = file_obj.read()
            md5_hash = hashlib.md5(file_contents).hexdigest()
        hash_dict.append({"filepath": file, "hash": md5_hash})
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
        print("DEBUG: pre_file_count")
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
    return post_file_count - pre_file_count


# TODO: Make program interactive with either
# - Paths as input
# - Config file stating path to traverse
# Also add actual comparison function, to be used as a recurring job
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
    print("Conducting hashing...")
    dic = hashing()
    print("Hashing complete.")
    print()
    print("Updating database...")
    file_count = database(dic)
    print("Database updated")

    end = time.time()
    print("Time: ", end - start)
    print(f"Files added: {file_count}")
