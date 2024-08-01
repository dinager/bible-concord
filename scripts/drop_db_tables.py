import mysql.connector


def drop_all_tables(db_config):
    try:
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor()

        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Fetch all table names
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Drop each table
        for (table_name,) in tables:
            if (table_name) == "group":
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
                print(f"Dropped table {table_name}")
            else:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"Dropped table {table_name}")

        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        # Commit changes
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'qazwsxedc',
    'database': 'bible-concord'
}

# Call the function to drop all tables
drop_all_tables(db_config)
