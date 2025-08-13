import shutil
import pymysql
import psycopg2
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sqlite3
import os
import subprocess

def test_mysql_connection(host,port,user,password,db_name):
    try:
        print("Testing MYSQL connection:")
        conn = pymysql.connect(
            host=host,
            port=port or 3306,
            user=user,
            password=password,
            database=db_name,
            connect_timeout=5
        )
        conn.close()
        print('MYSQL connection successful.')
        return True
    except Exception as e:
        print(f"MySQL connection failed: {e}")
        return False
    
def test_mongodb_connection(host,port,user,password,db_name):
        try:
            print("Testing MongoDB connection:")
            if user and password:
                uri = f"mongodb://{user}:{password}@{host}:{port or 27017}/{db_name}?authSource=admin"
            else:
               uri = f"mongodb://{host}:{port or 27017}/" 
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)  
            client.admin.command('ismaster')
            client.close()
            print("MongoDB connection successful.")
            return True
        except Exception as e:
           print(f"MongoDB connection failed: {e}")
           return False
        
def test_sqlite_connection(db_name):
    print(f"Checking for SQLite database file at: {db_name}")
    if os.path.exists(db_name):
        print('SQLite database file found.')
        return True
    else:
        print(f"Error: SQLite database file not found at '{db_name}'")
        return False
    
def test_postgres_connection(host, port, user, password, db_name):
    try:
        print("Testing PostgreSQL connection...")
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port or 5432,
            connect_timeout=5
        )
        conn.close()
        print('PostgreSQL connection successful.')
        return True
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        return False


def backup_postgres(host, port, user, password, db_name, output_file):
    try:
        env = os.environ.copy()
        if password:
            env['PGPASSWORD'] = password
        command = [
            'pg_dump', '--host', host, '--port', str(port or 5432),
            '--username', user, '--dbname', db_name, '--file', output_file,
            '--format', 'c'
        ]
        process = subprocess.run(command,env=env,check=True,capture_output=True,text=True)
        print(f"PostgreSQL backup successful! File saved to {output_file}")
        return True
    except Exception as e:
        print(f"PostgreSQL backup failed: {e}")
        return False
    
def backup_mysql(host, port, user, password, db_name, output_file):
    try:
        command = [
            'mysqldump', '--host', host, '--port', str(port or 3306),
            '--user', user,
        ]
        if password:
            command.append(f'--password={password}')
        command.extend(['--result-file', output_file, db_name])   
        process = subprocess.run(command,check=True,capture_output=True,text=True)
        print(f"MySQL backup successful! File saved to {output_file}")
        return True
    except Exception as e:
        print(f"MYSQL backup failed: {e}")
        return False
    
def backup_sqlite(db_name, output_file):
    try:
        shutil.copy2(db_name, output_file)
        print(f"SQLite backup successful! File copied to {output_file}")
        return True
    except Exception as e:
        print(f"SQLite backup failed: {e}")
        return False
    
def backup_mongodb(host, port, user, password, db_name, output_file):
    try:
        dump_dir = "mongo_dump_temp" 
        command = [
            'mongodump', '--host', host, '--port', str(port or 27017),
            '--db', db_name, '--out', dump_dir
        ]
        if user and password:
              command.extend(['--username', user, f'--password={password}', '--authenticationDatabase=admin'])
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        shutil.make_archive(output_file, 'zip', dump_dir)
        shutil.rmtree(dump_dir)
        print(f"MongoDB backup successful! Archive saved to {output_file}.zip")
        return True
    except Exception as e:
        print(f"MongoDb backup failed: {e}")
        return False

def test_db_connection(db_type, host, port, user, password, db_name):
    if db_type == 'postgres':
        return test_postgres_connection(host, port, user, password, db_name)
    elif db_type == 'mysql':
        return test_mysql_connection(host, port, user, password, db_name)
    elif db_type == 'mongodb':
        return test_mongodb_connection(host, port, user, password, db_name)
    elif db_type == 'sqlite':
        return test_sqlite_connection(db_name)
    else:
        print(f"Error: Unsupported database type '{db_type}' for connection test.")
        return False

def backup_db(db_type, host, port, user, password, db_name, output_file):
    if db_type == 'postgres':
        return backup_postgres(host, port, user, password, db_name, output_file)
    elif db_type == 'mysql':
        return backup_mysql(host, port, user, password, db_name, output_file)
    elif db_type == 'mongodb':
        return backup_mongodb(host, port, user, password, db_name, output_file)
    elif db_type == 'sqlite':
        return backup_sqlite(db_name, output_file)
    else:
        print(f"Error: Unsupported database type '{db_type}' for backup.")
        return False

