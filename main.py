import argparse
import logging
import sys
from db_connectors import test_db_connection,backup_db
from restoredb_utility import restore_db

def main():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backup_activity.log"),
        logging.StreamHandler(sys.stdout)
    ]
    )
    parser = argparse.ArgumentParser(description="A CLI utility for backing up the databases.")
    subparsers = parser.add_subparsers(dest='command',help='Available commands')

    backup_parser = subparsers.add_parser('backup',help='Perform a database backup')
    backup_parser.add_argument('--db-type',required=True,choices=['postgres','mysql','mongodb','sqlite'],help='Type of the database')
    backup_parser.add_argument('--host',default='localhost',help='Database host')
    backup_parser.add_argument('--port',type=int,help='Database Port')
    backup_parser.add_argument('--user',help='Database Username')
    backup_parser.add_argument('--password',help='Database Password')
    backup_parser.add_argument('--db-name',help='Database name to back up')
    backup_parser.add_argument('--output-file',required=True,help='Path to save the backup file')

    restore_parser = subparsers.add_parser('restore', help='Restore a database from a backup')
    restore_parser.add_argument('--db-type', required=True, choices=['postgres', 'mysql', 'mongodb', 'sqlite'], help='Type of the database')
    restore_parser.add_argument('--host', default='localhost', help='Database host (not for SQLite)')
    restore_parser.add_argument('--port', type=int, help='Database port (optional)')
    restore_parser.add_argument('--user', help='Database username (not for SQLite)')
    restore_parser.add_argument('--password', help='Database password (optional)')
    restore_parser.add_argument('--db-name', required=True, help='Target database name or file path for SQLite')
    restore_parser.add_argument('--input-file', required=True, help='Path to the backup file to restore from.')


    args = parser.parse_args()

    if args.command == 'backup':
        logging.info(f"--- Starting backup for '{args.db_name}' ({args.db_type}) ---")
        connection_ok = test_db_connection(
             db_type=args.db_type,
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            db_name=args.db_name
        )
        if connection_ok:
            logging.info("Connection is successful. Proceeding with backup.")
            backup_success = backup_db(
                db_type=args.db_type,
                host=args.host,
                port=args.port,
                user=args.user,
                password=args.password,
                db_name=args.db_name,
                output_file=args.output_file
            )
            if backup_success:
                logging.info(f"--- Backup for '{args.db_name}' completed successfully. ---")
            else:
                   logging.error(f"--- Backup for '{args.db_name}' failed. Check logs for details. ---")
        else:
            logging.error("Backup aborted due to connection failure. Check your credentials and network settings.")
            
    elif args.command == 'restore':
        logging.info(f"--- Starting restore for '{args.db_type}' from file '{args.input_file}' ---")
        connection_ok = test_db_connection(
            db_type=args.db_type, host=args.host, port=args.port,
            user=args.user, password=args.password, db_name=args.db_name
        )
        if connection_ok:
            logging.info("Connection successful. Proceeding with restore.")
            restore_successful = restore_db(
                db_type=args.db_type, host=args.host, port=args.port,
                user=args.user, password=args.password, db_name=args.db_name,
                input_file=args.input_file
            )
            if restore_successful:
                logging.info(f"--- Restore for '{args.db_name}' completed successfully. ---")
            else:
                logging.error(f"--- Restore for '{args.db_name}' failed. Check logs. ---")
        else:
            logging.error("Restore aborted due to connection failure.")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
