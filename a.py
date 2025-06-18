import snowflake.connector
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def get_connection(user, account, warehouse, private_key_path, private_key_password):
    """Connect to Snowflake using private key auth."""
    try:
        with open(private_key_path, "rb") as key_file:
            private_key = key_file.read()

        connection = snowflake.connector.connect(
            user=user,
            account=account,
            warehouse=warehouse,
            private_key=private_key,
            private_key_password=private_key_password
        )

        logging.info("✅ Connected to Snowflake.")
        return connection
    except Exception as e:
        logging.error(f"❌ Connection failed: {e}")
        sys.exit(1)


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


def main():
    if len(sys.argv) != 7:
        logging.error("Usage: python a.py <ENV> <USER> <PASSWORD> <PRIVATE_KEY_PATH> <PRIVATE_KEY_PASSWORD> <WAREHOUSE>")
        sys.exit(1)

    _, env, user, password, private_key_path, private_key_password, warehouse = sys.argv
    account = "LKGVJUZ-WS14116"  # Replace with your Snowflake account identifier

    conn = get_connection(user, account, warehouse, private_key_path, private_key_password)
    create_student_table(conn)


if __name__ == "__main__":
    main()
