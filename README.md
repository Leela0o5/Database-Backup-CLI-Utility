# Database-Backup-CLI-Utility

A command-line utility to back up and restore databases. Supports PostgreSQL, MySQL, MongoDB, and SQLite.

## Features
- Backup and restore databases using native tools  
- Connection testing before backup/restore  
- Logging to file (`backup_activity.log`) and console  

## Installation
### Clone the repository:
```bash
git clone https://github.com/Leela005/Database-Backup-CLI-Utility.git
cd Database-Backup-CLI-Utility
```

## Commands

| Command | Description                       | Key Options                                                                 |
|---------|-----------------------------------|------------------------------------------------------------------------------|
| backup  | Back up a database                | `--db-type`, `--host`, `--port`, `--user`, `--password`, `--db-name`, `--output-file` |
| restore | Restore a database from backup file | `--db-type`, `--host`, `--port`, `--user`, `--password`, `--db-name`, `--input-file`  |

### Example Usage:

```bash
python main.py backup --db-type postgres --host localhost --port 5432 --user myuser --password mypass --db-name mydb --output-file /path/to/backup_file

python main.py restore --db-type mysql --host localhost --port 3306 --user myuser --password mypass --db-name mydb --input-file /path/to/backup_file
```
