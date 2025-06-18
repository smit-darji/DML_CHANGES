import snowflake.connector
import sys
import logging
import os
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def get_connection(args):
    """
    Establish and return a Snowflake database connection.
    """
    user = args.user or os.getenv("SNOWFLAKE_USERNAME")
    account = args.account or os.getenv("SNOWFLAKE_ACCOUNT")
    warehouse = args.warehouse or os.getenv("SNOWFLAKE_WAREHOUSE")
    private_key_file = args.private_key_file or os.getenv("SNOWFLAKE_PRIVATE_KEY_FILE")

    if not all([user, account, warehouse, private_key_file]):
        logging.error("❌ Missing required connection parameters.")
        sys.exit(1)

    return snowflake.connector.connect(
        user=user,
        account="LKGVJUZ-WS14116",
        warehouse=warehouse,
        role="ACOUNTADMIN",
        authenticator="SNOWFLAKE_JWT",
        private_key_file=private_key_file
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


def parse_args():
    parser = argparse.ArgumentParser(description="Create student table in Snowflake")
    parser.add_argument("--user", help="Snowflake username")
    parser.add_argument("--account", help="Snowflake account name")
    parser.add_argument("--warehouse", help="Warehouse name")
    parser.add_argument("--private-key-file", help="Path to private key in PEM format (unencrypted)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    conn = get_connection(args)
    create_student_table(conn)
