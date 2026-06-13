import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_table(engine):
    create_sql = """
    CREATE TABLE IF NOT EXISTS job_posting (
        id SERIAL PRIMARY KEY,
        title VARCHAR(300),
        company VARCHAR(300),
        location VARCHAR(300),
        city VARCHAR(150),
        category VARCHAR(200),
        salary_min FLOAT,
        salary_max FLOAT,
        salary_avg FLOAT,
        has_salary INTEGER,
        contract_type VARCHAR(100),
        work_type VARCHAR(50),
        post_date DATE,
        post_month VARCHAR(20),
        description TEXT,
        search_term VARCHAR(100),
        skills_found TEXT
    );
    """
    with engine.connect() as conn:
        conn.execute(text(create_sql))
        conn.commit()
        print("Table created successfully.")

def load_data(engine):
    df = pd.read_csv("data/cleaned_jobs.csv")

    # Convert post_date to proper date format
    df['post_date'] = pd.to_datetime(df['post_date'], errors='coerce').dt.date

    # Replace NaN with None for SQL compatibility
    df = df.where(pd.notna(df), None)

    df.to_sql(
        name="job_posting", 
        con=engine, 
        if_exists="replace", 
        index=False
    )
    print(f"Loaded {len(df)} rows into job_posting table.")

def verify(engine):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM job_posting"))
        count = result.scalar()
        print(f"Verification: {count} rows in database.")

        print("\nSample query - top 5 cities by job count:")
        result = conn.execute(text("""
            SELECT city, COUNT(*) as job_count
            FROM job_posting
            GROUP BY city
            ORDER BY job_count DESC
            LIMIT 5
        """))
        for row in result:
            print(f"  {row[0]}: {row[1]} jobs")

        print("\nSample query - average salary by search term:")
        result = conn.execute(text("""
            SELECT search_term, 
                    ROUND(AVG(salary_avg)::numeric, 2) as avg_salary
            FROM job_posting
            WHERE salary_avg > 0
            GROUP BY search_term
            ORDER BY avg_salary DESC
        """))
        for row in result:
            print(f"  {row[0]}: £{row[1]}")

def main():
    print("Connecting to database...")
    engine = create_engine(CONNECTION_STRING)

    print("Creating table...")
    create_table(engine)

    print("Loading data...")
    load_data(engine)

    print("Verifying data...")
    verify(engine)

    print("\nStep 4 Complete!")

if __name__ == "__main__":
    main()