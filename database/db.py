import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"  # o tu servidor
        "DATABASE=PriceMonitor;"
        "Trusted_Connection=yes;"
    )
    return conn


def insert_data(df):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO price_history (product_name, price, rating, date)
            VALUES (?, ?, ?, ?)
        """, row["name"], row["price"], row["rating"], row["date"])

    conn.commit()
    conn.close()