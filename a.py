import snowflake.connector
import os
# Snowflake connection parameters
conn = snowflake.connector.connect(
    user='yogeshmakwana',
    password='myz3YHnLdqbx8YW',
    account='LKGVJUZ-WS14116',
    warehouse='COMPUTE_WH'
)


def get_connection():
    """
    Establishes and returns a Snowflake database connection using environment variables.
    """
    user = os.getenv("SNOWFLAKE_USERNAME")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    private_key_file = os.getenv("SNOWFLAKE_PRIVATE_KEY_FILE")
    private_file_password = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSWORD")

    return snowflake.connector.connect(
        user=user,
        authenticator="SNOWFLAKE_JWT",
        private_key_file=private_key_file,
        private_key_file_pwd=private_file_password,
        account=account,
        warehouse=warehouse,
        role="SYSADMIN",
    )

conn = get_connection()


# Create a cursor object
cur = conn.cursor()

try:
    # Create database if it doesn't exist
    conn.execute("CREATE DATABASE IF NOT EXISTS demo_DB;")
    print("Database 'demo_DB' ensured.")

    # Create schema if it doesn't exist
    conn.execute("CREATE SCHEMA IF NOT EXISTS demo_DB.public;")
    print("Schema 'public' ensured in database 'demo_DB'.")

    # Use the created database and schema
    conn.execute("USE DATABASE demo_DB;")
    conn.execute("USE SCHEMA public;")

    # Create table
    create_table_sql = """
    CREATE OR REPLACE TABLE example_table1 (
        id INT AUTOINCREMENT,
        name STRING,
        created_at TIMESTAMP
    );
    """
    conn.execute(create_table_sql)
    print("Table 'example_table' created successfully.")

finally:
    conn.close()
    conn.close()
