import argparse

def main():
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
    restore_parser = subparsers.add_parser('restore',help='Restore a database from a backup')

    args = parser.parse_args()

    if args.command == 'backup':
        print('Backup command')
    elif args.command == 'restore':
        print('Restore')
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
