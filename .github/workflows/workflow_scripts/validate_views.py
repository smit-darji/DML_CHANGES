import snowflake.connector
import time
import os
import logging
import sys
from multiprocessing import Pool, cpu_count

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
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
        role="public",
    )


def fetch_views(database_name, cursor):
    """
    Fetches and returns all views in the given database.
    """
    try:
        cursor.execute(f"USE DATABASE {database_name}")
    except Exception as e:
        logging.error(f"Error using database {database_name}: {e}")
        return [], 0

    try:
        query_start_time = time.time()
        views_query = f"""
        SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME
        FROM {database_name}.INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA != 'INFORMATION_SCHEMA'
        """
        cursor.execute(views_query)
        views = cursor.fetchall()
        query_end_time = time.time()
        query_duration = query_end_time - query_start_time

        view_names = [
            f"{database_name}.{schema}.{view_name}"
            for database_name, schema, view_name in views
            if database_name and schema and view_name
        ]
        return view_names, query_duration
    except Exception as e:
        logging.error(f"Error fetching views for database {database_name}: {e}")
        return [], 0


def explain_view(view_name, cursor):
    """
    Executes EXPLAIN command for a given view and returns execution time, success status, and view name.
    """
    explain_query = f"EXPLAIN USING JSON SELECT * FROM {view_name};"
    try:
        explain_start_time = time.time()
        cursor.execute(explain_query)
        result = cursor.fetchall()  # Fetch result to trigger the query execution
        explain_end_time = time.time()
        explain_duration = explain_end_time - explain_start_time
        return explain_duration, True, view_name  # Success
    except Exception as e:
        logging.error(f"Error explaining view {view_name}: {e}")
        return 0, False, view_name  # Failure


def process_database(db_name):
    """
    Processes views in a database and performs EXPLAIN commands sequentially.
    """
    conn = get_connection()
    cursor = conn.cursor()

    db_start_time = time.time()
    views, query_duration = fetch_views(db_name, cursor)
    num_views = len(views)

    # Initialize results
    total_explain_time = 0
    success_count = 0
    error_count = 0
    error_views = []  # List to store error views

    logging.info(f"Processing database: {db_name}")
    logging.info(f"\tNumber of views in {db_name}: {num_views}")
    logging.info(f"\tQuery execution time for {db_name}: {query_duration:.2f} seconds")

    if views:
        for view in views:
            explain_duration, success, view_name = explain_view(view, cursor)
            if success:
                success_count += 1
            else:
                error_count += 1
                error_views.append(view_name)
            total_explain_time += explain_duration
    else:
        logging.info(f"\tNo views found in {db_name}.")

    db_end_time = time.time()
    db_duration = db_end_time - db_start_time

    logging.info(
        f"\tTotal time taken for processing {db_name}: {db_duration:.2f} seconds"
    )
    logging.info(f"\tSuccessful EXPLAIN VIEWS: {success_count}")
    logging.info(f"\tFailed EXPLAIN VIEWS: {error_count}")

    cursor.close()
    conn.close()

    return (
        db_name,
        num_views,
        success_count,
        error_count,
        total_explain_time,
        error_views,
    )


def main():
    if len(sys.argv) < 2:
        logging.info(
            "No database names provided. Fetching all databases from Snowflake."
        )
        database_names_param = []
    else:
        database_names_param = sys.argv[1:]

    start_time = time.time()

    if not database_names_param:
        # Establish connection
        conn = get_connection()
        cur = conn.cursor()

        # Retrieve database names
        try:
            cur.execute("SHOW DATABASES")
            databases = cur.fetchall()
            database_names = [db[1] for db in databases if db[1]]
        except Exception as e:
            logging.error(f"Error fetching database names: {e}")
            return
        finally:
            cur.close()
            conn.close()
    else:
        database_names = [name for name in database_names_param]

    # Filter database names containing 'prod' or 'PROD'
    database_names = [name for name in database_names if "prod" in name.lower()]

    logging.info("Filtered Database list:")
    for name in database_names:
        logging.info(f"\t- {name}")
    logging.info(f"Total number of filtered databases: {len(database_names)}")

    # Process each database with multiprocessing
    with Pool(cpu_count()) as pool:
        results = pool.map(process_database, database_names)

    # Collect results
    total_views_count = 0
    total_success_count = 0
    total_error_count = 0
    explain_times = {}  # Dictionary to store EXPLAIN times for each database
    all_error_views = []  # List to store error views across all databases

    for result in results:
        (
            db_name,
            num_views,
            success_count,
            error_count,
            total_explain_time,
            error_views,
        ) = result
        total_views_count += num_views
        total_success_count += success_count
        total_error_count += error_count
        explain_times[db_name] = total_explain_time
        all_error_views.extend(error_views)

    # Print summary
    end_time = time.time()
    total_duration = end_time - start_time

    logging.info("================================================")
    logging.info(f"Total process completed in {total_duration:.2f} seconds")
    logging.info(f"Total number of databases: {len(database_names)}")
    logging.info(f"Total number of views across all databases: {total_views_count}")
    logging.info(f"Total successful EXPLAIN VIEWS: {total_success_count}")
    logging.info(f"Total failed EXPLAIN VIEWS: {total_error_count}")
    logging.info("================================================")

    # Print total EXPLAIN time for each database
    for db_name, total_explain_time in explain_times.items():
        logging.info(
            f"Total EXPLAIN time for database {db_name}: {total_explain_time:.2f} seconds"
        )

    # Print error views
    if all_error_views:

        logging.info("======================Error Views==========================")
        logging.info("Error Views List:")
        for error_view in all_error_views:

            logging.info(error_view)
        logging.info("===========================================================")
        sys.exit(1)
    else:
        logging.info("No error views found. Exiting with error.")


if __name__ == "__main__":
    main()
