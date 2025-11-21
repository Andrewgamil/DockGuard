#!/bin/bash

# Restore script for SQLite database


BACKUP_DIR="./backups"
DB_PATH="../service/data/urlshort.db"
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Error: Please provide a backup file name"
    echo "Usage: ./restore.sh <backup_file>"
    echo "Available backups:"
    ls -lh "$BACKUP_DIR" 2>/dev/null || echo "No backups directory found"
    exit 1
fi


if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_DIR/$BACKUP_FILE"
    exit 1
fi


mkdir -p "$(dirname "$DB_PATH")"


cp "$BACKUP_DIR/$BACKUP_FILE" "$DB_PATH"

if [ $? -eq 0 ]; then
    echo "Database restored successfully from: $BACKUP_DIR/$BACKUP_FILE"
    echo "Database size: $(du -h "$DB_PATH" | cut -f1)"
else
    echo "Error: Restore failed"
    exit 1
fi

