import snowflake.connector
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def get_connection(env, user, account, private_key_file, warehouse):
    """
    Establish and return a Snowflake database connection.
    """
    if not all([env, user, account, private_key_file, warehouse]):
        logging.error("❌ Missing required connection parameters.")
        sys.exit(1)

    return snowflake.connector.connect(
        user=user,
        account=account,
        warehouse=warehouse,
        role="public",
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


if __name__ == "__main__":
    if len(sys.argv) != 6:
        logging.error("Usage: a.py <env> <user> <account> <private_key_file> <warehouse>")
        sys.exit(1)

    env, user, account, private_key_file, warehouse = sys.argv[1:]
    conn = get_connection(env, user, account, private_key_file, warehouse)
    create_student_table(conn)
