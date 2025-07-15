import psycopg2

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="uqg24gau",
            user="uqg24gau",
            password="RadioYesterdayProbably82-",
            host="cmpstudb-01.cmp.uea.ac.uk",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SET search_path TO cmps_schema;")  # <== ADD THIS LINE
        conn.commit()
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None
