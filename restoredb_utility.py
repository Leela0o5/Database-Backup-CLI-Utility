import subprocess
import os
import shutil
import zipfile
import sqlite3

def restore_sqlite(db_name,input_file):
    try:
         shutil.copy2(input_file, db_name)
         print(f"SQLite restore successful!File '{input_file}' copied to '{db_name}'")
         return True
    except Exception as e:
        print(f"SQLite restore failed: {e}")
        return False

def restore_mysql(host, port, user, password, db_name, input_file):
    try:
        print("Starting MySQL restore...")
        command = [
            'mysql', '--host', host, '--port', str(port or 3306),
            '--user', user,
        ]
        if password:
            command.append(f'--password={password}')
        command.append(db_name)
        with open(input_file, 'r') as f:
            process = subprocess.run(command, stdin=f, check=True, capture_output=True, text=True)
        print(f"MySQL restore successful for database '{db_name}'.")
        return True
    except Exception as e:
        print(f"MySQL restore failed: {e}")
        return False

def restore_mongodb(host, port, user, password, db_name, input_file):
    restore_dir = "mongo_restore_temp"
    try:
        print(f"Extracting backup file '{input_file}' to '{restore_dir}'.")
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(restore_dir)
        dump_path = os.path.join(restore_dir, "mongo_dump_temp", db_name)
        if not os.path.exists(dump_path):
             dump_path = os.path.join(restore_dir, db_name)
             if not os.path.exists(dump_path):
                 dump_path = restore_dir 
        command = [
            'mongorestore', '--host', host, '--port', str(port or 27017),
            '--db', db_name, 
            '--drop',
            dump_path
        ]
        if user and password:
            command.extend(['--username', user, f'--password={password}', '--authenticationDatabase=admin'])
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"MongoDB restore successful for database '{db_name}'.")
        return True
    except Exception as e:
        print(f"MongoDB restore failed: {e}")
        return False
    finally:
        if os.path.exists(restore_dir):
            print(f"Cleaning up temporary directory '{restore_dir}'.")
            shutil.rmtree(restore_dir)

def restore_postgres(host, port, user, password, db_name, input_file):
    try:
        env = os.environ.copy()
        if password:
            env['PGPASSWORD'] = password
        command = [
            'pg_restore', '--host', host, '--port', str(port or 5432),
            '--username', user, '--dbname', db_name,
            '--clean', 
            input_file
        ]
        process = subprocess.run(command, env=env, check=True, capture_output=True, text=True)
        print(f"PostgreSQL restore successful for database '{db_name}'.")
        return True
    except Exception as e:
        print(f"PostgreSQL restore failed: {e}")
        return False

def restore_db(db_type, host, port, user, password, db_name, input_file):
    if db_type == 'postgres':
        return restore_postgres(host, port, user, password, db_name, input_file)
    elif db_type == 'mysql':
        return restore_mysql(host, port, user, password, db_name, input_file)
    elif db_type == 'mongodb':
        return restore_mongodb(host, port, user, password, db_name, input_file)
    elif db_type == 'sqlite':
        return restore_sqlite(db_name, input_file)
    else:
        print(f"Error: Unsupported database type '{db_type}' for restore.")
        return False
