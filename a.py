import snowflake.connector

# Snowflake connection parameters
conn = snowflake.connector.connect(
    user='yogeshmakwana',
    password='myz3YHnLdqbx8YW',
    account='LKGVJUZ-WS14116',
    warehouse='COMPUTE_WH'
)

# Create a cursor object
cur = conn.cursor()

try:
    # Create database if it doesn't exist
    cur.execute("CREATE DATABASE IF NOT EXISTS demo_DB;")
    print("Database 'demo_DB' ensured.")

    # Create schema if it doesn't exist
    cur.execute("CREATE SCHEMA IF NOT EXISTS demo_DB.public;")
    print("Schema 'public' ensured in database 'demo_DB'.")

    # Use the created database and schema
    cur.execute("USE DATABASE demo_DB;")
    cur.execute("USE SCHEMA public;")

    # Create table
    create_table_sql = """
    CREATE OR REPLACE TABLE example_table (
        id INT AUTOINCREMENT,
        name STRING,
        created_at TIMESTAMP
    );
    """
    cur.execute(create_table_sql)
    print("Table 'example_table' created successfully.")

finally:
    cur.close()
    conn.close()
