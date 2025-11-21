#!/bin/bash

# Backup script for SQLite database
# Usage: ./backup.sh [backup_name]

BACKUP_DIR="./backups"
DB_PATH="../service/data/urlshort.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME=${1:-"urlshort_backup_${TIMESTAMP}.db"}

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if database exists
if [ ! -f "$DB_PATH" ]; then
    echo "Error: Database file not found at $DB_PATH"
    exit 1
fi

# Create backup
cp "$DB_PATH" "$BACKUP_DIR/$BACKUP_NAME"

if [ $? -eq 0 ]; then
    echo "Backup created successfully: $BACKUP_DIR/$BACKUP_NAME"
    echo "Database size: $(du -h "$DB_PATH" | cut -f1)"
    echo "Backup size: $(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)"
else
    echo "Error: Backup failed"
    exit 1
fi

