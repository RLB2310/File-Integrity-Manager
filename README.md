```
 ░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████████████▓▒░  
 ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
 ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
 ░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
 ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
 ░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
 ░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░
```
A simple file integrity manager (FIM) written in Python, which stores filepaths and hashes in a SQLite database for management of a targeted file system.

<img width="1861" height="663" alt="image" src="https://github.com/user-attachments/assets/ae81c34f-8006-435a-b5b4-3ada4b7cf8e4" />

# Usage

Run the `fim.py` program with `python`.

**Note**: If you are hashing a privileged directory, you must run the program as `sudo`.

## Ntfy 

The program supports Ntfy notifications on changed hashes. To set this up, edit the `config.ini` with the relevant `server` settings.


