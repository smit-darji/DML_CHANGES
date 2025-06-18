import snowflake.connector
import sys
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def get_connection():
    """
    Establishes and returns a Snowflake database connection using environment variables.
    """
    user = os.getenv("SNOWFLAKE_USERNAME")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    account = "LKGVJUZ-WS14116"
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


def create_student_table(conn):
    """Create a student table in demo_db.public"""
    create_table_sql = """
    CREATE OR REPLACE TABLE demo_db.public.student (
        student_id INT PRIMARY KEY,
        first_name STRING,
        last_name STRING,
        enrollment_date DATE
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute("USE DATABASE demo_db;")
            cur.execute("USE SCHEMA public;")
            cur.execute(create_table_sql)
            logging.info("✅ Table demo_db.public.student created successfully.")
    except Exception as e:
        logging.error(f"❌ Failed to create table: {e}")
    finally:
        conn.close()
        logging.info("🔒 Connection closed.")

