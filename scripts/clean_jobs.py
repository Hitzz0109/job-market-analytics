import pandas as pd
import re
import os

df=pd.read_csv("data/raw_jobs.csv")

print("=== RAW DATA INFO ===")
print(f"Shape: {df.shape}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nData Types:\n{df.dtypes}")

# 1. Clean Column: title
df['title'] = df['title'].str.strip().str.title()

# 2. Clean Column: company
df['company'] = df['company'].str.strip()
df['company'] = df['company'].fillna('Unknown')

# 3. Clean Column: location
df['location'] = df['location'].str.strip()
df['location'] = df['location'].fillna('Unknown')

# Extract city (first part before comma)
df["city"] = df["location"].apply(
    lambda x: x.split(",")[0].strip() if pd.notnull(x) else "Unknown"
)

# 4. Clean Column: salary
# Fill missing salaries with NaN (keep as-is for now, handle in EDA)
df['salary_min'] = pd.to_numeric(df['salary_min'], errors='coerce')
df['salary_max'] = pd.to_numeric(df['salary_max'], errors='coerce') 

# Create salary_avg where both exist
df['salary_avg'] = df[['salary_min', 'salary_max']].mean(axis=1)

# Flag rows with salary info
df['has_salary'] = df["salary_avg"].notna().astype(int)

# 5. Clean Column: contract_type
df['contract_type'] = df['contract_type'].str.strip()
df['contract_type'] = df['contract_type'].replace("", 'Unknown')
df['contract_type'] = df['contract_type'].fillna('Unknown')

# 6. Clean Column: created (date)
df['created'] = pd.to_datetime(df['created'], errors='coerce', utc=True)
df['created'] = df['created'].dt.tz_localize(None) # remove timezone
df["post_date"] = df["created"].dt.date
df['post_month'] = df['created'].dt.to_period('M').astype(str)

# 7. Clean Column: description (remove HTML tags)
def clean_html(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"<[^>]+>", "", text)  # Remove HTML tags
    text = re.sub(r"\s+", " ", text)  # collapse whitespace
    return text.strip()

df['description'] = df['description'].apply(clean_html)

# 8. Classify remote vs on-site
def classify_remote(row):
    text = (str(row['title']) + " " + str(row['description'])).lower()
    if "remote" in text or "work from home" in text or "wfh" in text:
        return "Remote"
    elif "hybrid" in text:
        return "Hybrid"
    else:
        return "On-site"
    
df['work_type'] = df.apply(classify_remote, axis=1)

# 9. Extract key skills from description
SKILLS = [
    "python", "sql", "excel","power bi", "tableau", "r",
    "machine learning", "deep learning", "spark", "hadoop",
    "aws", "azure", "gcp", "docker", "kubernetes",
    "pandas", "numpy", "scikit-learn", "tensorflow", "Pytorch",
    "java", "scala", "airflow", "dbt", "snowflake"
]

def extract_skills(text):
    if pd.isna(text):
        return []
    text = text.lower()
    found = [skill for skill in SKILLS if skill in text]
    return ", ".join(found)

df['skills_found'] = df['description'].apply(extract_skills)

# 10. Drop columns we no longer need
df.drop(columns=['created', 'redirect_url'], inplace=True)

# 11. Final check
print("\n=== CLEANED DATA INFO ===")
print(f"Shape: {df.shape}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nWork Type Distribution:\n{df['work_type'].value_counts()}")
print(f"\nTop 10 cities:\n{df['city'].value_counts().head(10)}")
print(f"\nSalary coverage: {df['has_salary'].sum()} out of {len(df)} jobs have salary data")

# 12. Save cleaned data
output_path = os.path.join("data", "cleaned_jobs.csv")
df.to_csv(output_path, index=False)
print(f"\nCleaned data saved to: {output_path}")
