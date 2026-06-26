\# 📊 Job Market Analytics Platform



An end-to-end data analytics platform that collects, cleans, stores, analyzes, and visualizes live job market data — combining \*\*Python, SQL, Power BI, and a Generative AI chatbot\*\* into a single working pipeline.



Built as a 2026 portfolio project to demonstrate the full data lifecycle: from raw API ingestion to an AI agent that can answer natural-language questions about the job market in real time.



\---



\## 🎯 Project Overview



This project answers a simple question: \*\*what does the current job market actually look like?\*\*



It pulls real, live job postings (UK tech \& data roles via the Adzuna API), cleans and engineers features from them, loads them into a relational database, analyzes them for trends, visualizes the results in an interactive dashboard, and finally — lets a user just \*ask\* questions about the data in plain English and get an AI-generated answer backed by real SQL queries.



\---



\## 🏗️ Architecture



┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌───────────────┐



│  Adzuna API │ ──▶ │ Python (ETL) │ ──▶ │  PostgreSQL │ ──▶ │   Power BI    │



│ (raw jobs)  │     │ clean + EDA  │     │  (job\_posting)│     │  Dashboard    │



└─────────────┘     └──────────────┘     └──────┬──────┘     └───────────────┘



│



▼



┌───────────────────┐



│  Gemini AI Chatbot │



│  (NL → SQL → NL)   │



└───────────────────┘



\---



\## ✨ Features



\- \*\*Automated data collection\*\* — Python script pulls live job postings across 8 in-demand roles (Data Analyst, Data Scientist, ML Engineer, etc.) via the Adzuna public API

\- \*\*Data cleaning \& feature engineering\*\* — standardizes locations, parses salaries, classifies remote/hybrid/on-site work, and extracts in-demand skills from raw job descriptions using keyword matching

\- \*\*Relational database\*\* — clean, query-ready PostgreSQL schema (`job\_posting` table) with 16 engineered columns

\- \*\*Exploratory Data Analysis\*\* — Jupyter notebook covering salary distributions, top skills, city-level hiring trends, and work-type breakdowns

\- \*\*Interactive Power BI dashboard\*\* — 6 visuals (top cities, salary by role, work-type split, top skills, postings over time) with 3 working slicers for live filtering

\- \*\*AI-powered chatbot\*\* — ask questions in plain English (e.g. \*"What's the average salary for data scientists?"\*); the assistant converts the question into a real SQL query, runs it against the live database, and returns a natural-language answer — powered by Google's \*\*Gemini 2.5 Flash\*\* API



\---



\## 🛠️ Tech Stack



| Layer | Technology |

|---|---|

| Data Collection | Python, `requests`, Adzuna Jobs API |

| Data Processing | Python, Pandas, NumPy |

| Database | PostgreSQL, SQLAlchemy |

| Analysis | Jupyter Notebook, Matplotlib, Seaborn |

| Visualization | Power BI Desktop |

| AI / NLP | Google Gemini API (`gemini-2.5-flash`) |

| Version Control | Git, GitHub |



\---



\## 📁 Project Structure



job-market-analytics/



├── data/                  # Raw \& cleaned CSVs, EDA chart exports



├── scripts/



│   ├── collect\_jobs.py    # Pulls live job data from Adzuna API



│   ├── clean\_jobs.py      # Cleans data, engineers features, extracts skills



│   ├── load\_to\_db.py      # Loads cleaned data into PostgreSQL



│   └── chatbot.py         # AI chatbot: natural language → SQL → natural language



├── notebooks/



│   └── job\_market\_eda.ipynb   # Exploratory data analysis notebook



├── dashboard/



│   └── job\_market\_dashboard.pbix   # Power BI dashboard file



├── docs/                  # Additional documentation



├── .env                   # API keys \& DB credentials (not committed)



├── .gitignore



└── README.md



\---



\## 🚀 Getting Started



\### Prerequisites

\- Python 3.11+

\- PostgreSQL 17+

\- Power BI Desktop (Windows)

\- A free \[Adzuna API](https://developer.adzuna.com) key

\- A free \[Google Gemini API](https://aistudio.google.com/apikey) key



\### Setup



1\. \*\*Clone the repo\*\*

```bash

&#x20;  git clone https://github.com/<your-username>/job-market-analytics.git

&#x20;  cd job-market-analytics

```



2\. \*\*Create a virtual environment \& install dependencies\*\*

```bash

&#x20;  python -m venv venv

&#x20;  venv\\Scripts\\activate          # Windows

&#x20;  pip install -r requirements.txt

```



3\. \*\*Configure environment variables\*\* — create a `.env` file in the root:



ADZUNA\_APP\_ID=your\_app\_id



ADZUNA\_APP\_KEY=your\_app\_key



DB\_HOST=localhost



DB\_NAME=job\_market\_db



DB\_USER=postgres



DB\_PASSWORD=your\_db\_password



DB\_PORT=5432



GEMINI\_API\_KEY=your\_gemini\_key



4\. \*\*Run the pipeline, in order\*\*

```bash

&#x20;  python scripts/collect\_jobs.py     # fetch live job data

&#x20;  python scripts/clean\_jobs.py       # clean \& engineer features

&#x20;  python scripts/load\_to\_db.py       # load into PostgreSQL

&#x20;  python scripts/chatbot.py          # chat with your data

```



5\. \*\*Open the dashboard\*\* — launch `dashboard/job\_market\_dashboard.pbix` in Power BI Desktop and click \*\*Refresh\*\* to connect to your local database.



\---



\## 💬 Chatbot Demo



You: What is the average salary for data scientists?



Bot: Based on our job posting data, the average salary for a data



scientist is approximately $85,060. This figure provides a



general idea of compensation for the role.

You: How many remote jobs are there?



Bot: There are 31 remote jobs available, based on postings



identified with a 'Remote' work type.

You: What companies are hiring for machine learning engineer?



Bot: There are 37 companies currently hiring for Machine Learning



Engineer roles, including Deliveroo, Spotify, ASOS, and G-Research.



\---



\## 📈 Key Insights from the Data



\- \*\*London dominates\*\* the UK job market with the highest concentration of postings across all search terms

\- \*\*On-site roles still lead\*\* overall, though hybrid arrangements make up a significant share of postings

\- \*\*Python, SQL, and Power BI\*\* are among the most frequently requested skills across data roles

\- Salary ranges vary meaningfully by role, with ML Engineer and Data Scientist roles commanding the highest average compensation



\*(Full charts and breakdowns available in `notebooks/job\_market\_eda.ipynb` and the Power BI dashboard.)\*



\---



\## 🔮 Future Enhancements



\- \[ ] Deploy the database to \*\*AWS RDS\*\* and host the chatbot on \*\*AWS EC2\*\* for a fully cloud-based version

\- \[ ] Add scheduled daily/weekly data refreshes via a cron job or AWS Lambda

\- \[ ] Expand data sources (LinkedIn, Indeed, government labor statistics) for broader market coverage

\- \[ ] Add a lightweight \*\*Streamlit\*\* front-end so the chatbot can be used without the terminal

\- \[ ] Train a classification model to auto-tag job seniority level (Junior / Mid / Senior)

\- \[ ] Add salary forecasting using time-series analysis



\---



\## ⚖️ Ethical Considerations



This project only collects publicly available job posting data through an official, permitted API (Adzuna) — no scraping of restricted or personal data is performed. Company and job data is used strictly for aggregate market analysis, not for any individual profiling.



\---



\## 📝 License



This project is open-source and available for learning purposes under the MIT License.



\---



\## 🙋 Author



Built by \*\*Hitesh Dongare\*\* as a hands-on portfolio project demonstrating end-to-end data engineering, analytics, and applied AI.



\*If you found this useful, consider giving the repo a ⭐!\*

