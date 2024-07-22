#!/bin/bash

# Database credentials
USER="root"
PASSWORD="qazwsxedc"
HOST="localhost"
DB_NAME="bible-concord"

# Connect to the database and truncate tables
mysql -u $USER -p$PASSWORD -h $HOST $DB_NAME <<EOF
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE word_appearance;
TRUNCATE TABLE word;
TRUNCATE TABLE chapter;
TRUNCATE TABLE book;
TRUNCATE TABLE \`group\`; # Use backticks to escape the table name
TRUNCATE TABLE word_in_group;
SET FOREIGN_KEY_CHECKS = 1;
EOF

echo "Tables truncated successfully."