import snowflake.connector
import os

def get_connection():
    """
    Establish and return a Snowflake connection using environment variables and key-pair auth.
    """
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USERNAME"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role="ACCOUNTADMIN",
        authenticator="SNOWFLAKE_JWT",
        private_key_file=os.getenv("SNOWFLAKE_PRIVATE_KEY_FILE"),
        private_key_password=os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSWORD")
    )

# Connect and run queries
conn = get_connection()
cur = conn.cursor()

try:
    # Create database and schema
    cur.execute("CREATE DATABASE IF NOT EXISTS demo_DB;")
    print("Database 'demo_DB' ensured.")

    cur.execute("CREATE SCHEMA IF NOT EXISTS demo_DB.public;")
    print("Schema 'public' ensured in database 'demo_DB'.")

    # Set context
    cur.execute("USE DATABASE demo_DB;")
    cur.execute("USE SCHEMA public;")

    # Create table
    cur.execute("""
        CREATE OR REPLACE TABLE DEMO (
            id INT AUTOINCREMENT,
            name STRING,
            created_at TIMESTAMP
        );
    """)
    print("Table 'DEMO' created successfully.")

finally:
    cur.close()
    conn.close()
