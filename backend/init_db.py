from database import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS exchange_rates(

    id SERIAL PRIMARY KEY,

    currency_code VARCHAR(10),

    currency_name VARCHAR(100),

    rate NUMERIC,

    rate_date DATE
)
""")

conn.commit()

cursor.close()

conn.close()