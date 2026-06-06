from fastapi import FastAPI, Query
from nbp_service import fetch_rates
import psycopg2
from fastapi.middleware.cors import CORSMiddleware
import time
from typing import Optional
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_conn():
    for i in range(10):
        try:
            return psycopg2.connect(
                host="waluty-db",
                database="waluty",
                user="postgres",
                password="postgres"
            )
        except Exception as e:
            print("db not ready, retrying", e)
            time.sleep(2)

    raise Exception("Database not available")

@app.on_event("startup")
def startup():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id SERIAL PRIMARY KEY,
            currency_code VARCHAR(10),
            currency_name VARCHAR(100),
            rate NUMERIC,
            rate_date DATE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    
@app.post("/waluty/fetch")
def fetch():

    data = fetch_rates()
    rates = data[0]["rates"]

    conn = get_conn()
    cur = conn.cursor()

    for jz in rates:
        cur.execute("""
            INSERT INTO exchange_rates
            (currency_code, currency_name, rate, rate_date)
            VALUES (%s, %s, %s, CURRENT_DATE)
        """, (jz["code"], jz["currency"], jz["mid"]))

    conn.commit()
    cur.close()
    conn.close()

    return {"ok": True, "count": len(rates)}

@app.get("/waluty")
def get_all(
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    day: Optional[int] = Query(None)
):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT currency_code, currency_name, rate, rate_date
        FROM exchange_rates
        WHERE 1=1
    """

    params = []

    if year:
        sql += " AND EXTRACT(YEAR FROM rate_date) = %s"
        params.append(year)

    if month:
        sql += " AND EXTRACT(MONTH FROM rate_date) = %s"
        params.append(month)

    if day:
        sql += " AND EXTRACT(DAY FROM rate_date) = %s"
        params.append(day)

    cur.execute(sql, params)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows