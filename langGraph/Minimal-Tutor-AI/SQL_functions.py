import psycopg2
db_params = {
    "host": "dpg-cpi3g4kf7o1s73bbfuag-a.oregon-postgres.render.com",
    "database": "aitutordb_inkl",
    "user": "saynt",
    "password": "hdTLAB7fHjzHOfeC5u5LYp7F7CUL0Zsr",
    "port": 5432
}

def execute_select_query(sql_query):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        # Create a cursor object
        cur = conn.cursor()
        # Execute the SQL query
        cur.execute(sql_query)
        # Fetch all rows from the result
        rows = cur.fetchall()
        # Print the result
        return rows
        # Close the cursor and the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def execute_insert_query(sql_query):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        # Create a cursor object
        cur = conn.cursor()
        # Execute the SQL query
        cur.execute(sql_query)
        # Commit the transaction
        conn.commit()
        print("Insert query executed successfully.")
        # Close the cursor and the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def execute_update_query(sql_query):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        # Create a cursor object
        cur = conn.cursor()
        # Execute the SQL query
        cur.execute(sql_query)
        # Commit the transaction
        conn.commit()
        print("Update query executed successfully.")
        # Close the cursor and the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def execute_delete_query(sql_query):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        # Create a cursor object
        cur = conn.cursor()
        # Execute the SQL query
        cur.execute(sql_query)
        # Commit the transaction
        conn.commit()
        print("Delete query executed successfully.")
        # Close the cursor and the connection
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")



print(execute_select_query("SELECT text FROM chapters where chapter_id = 1"))