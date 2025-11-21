#!/bin/bash

# Restore script for SQLite database
# Usage: ./restore.sh <backup_file>

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

# Check if backup file exists
if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_DIR/$BACKUP_FILE"
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p "$(dirname "$DB_PATH")"

# Restore backup
cp "$BACKUP_DIR/$BACKUP_FILE" "$DB_PATH"

if [ $? -eq 0 ]; then
    echo "Database restored successfully from: $BACKUP_DIR/$BACKUP_FILE"
    echo "Database size: $(du -h "$DB_PATH" | cut -f1)"
else
    echo "Error: Restore failed"
    exit 1
fi

