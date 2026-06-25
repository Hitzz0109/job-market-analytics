import os
from google import genai
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(CONNECTION_STRING)

TABLE_SCHEMA = """
Table: job_posting
Columns:
    id INTEGER, title VARCHAR, company VARCHAR, location VARCHAR,city VARCHAR,
    category VARCHAR, salary_min FLOAT, salary_max FLOAT, salary_avg FLOAT,
    has_salary INTEGER, contract_type VARCHAR, work_type VARCHAR (Remote/Hybrid/On-site), 
    post_date DATE, post_month VARCHAR, description TEXT,
    search_term VARCHAR, skills_found TEXT
"""

def generate_sql(question):
    prompt = f"""You are a SQL expert. Given this PostgreSQL table schema:
    
{TABLE_SCHEMA}

Convert this question into a single valid PostgreSQL SELECT query.
Only return the SQL query, nothing else. No explanation, no markdown formatting, no backticks.

Question: {question}
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    sql = response.text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def run_query(sql):
    try:
        with engine.connect() as conn:
            result = pd.read_sql(text(sql), conn)
        return result
    except Exception as e:
        return f"Query Error: {e}"
    
def generate_answer(question, sql, result_df):
    if isinstance(result_df, str):  
        return f"Sorry, I couldn't process that - {result_df}"
    
    data_preview = result_df.to_string(index=False) if len(result_df) > 0 else "No results found."

    prompt = f"""The user asked: "{question}"

I ran the SQL query: "{sql}"

Result:
{data_preview}

Write a clear, friendly, natural-language answer to the user's question based on this data.
Keep it concise - 2.4 sentences. Include specific numbers from the data.
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text.strip()

def chat():
    print("=" * 60)
    print("Job Market AI Chatbot (powered by Gemini) — ask away!")
    print("Type 'exit' to quit")
    print("=" * 60)

    while True:
        question = input("\nYou: ")
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        print("Thinking...")
        sql = generate_sql(question)
        print(f"[Generated SQL: {sql}]")

        result = run_query(sql)
        answer = generate_answer(question, sql, result)

        print(f"\nBot: {answer}")

if __name__ == "__main__":
    chat()