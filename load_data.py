import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost", user="root", password="Exalted.143", database="fifa_db"
)

print("Connected to MySQL successfully!")

# Load the FIFA CSV
df = pd.read_csv("players_22.csv", low_memory=False)
print(f"Loaded {len(df)} players from CSV")

# Write to MySQL
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:Exalted.143@localhost/fifa_db")
df.to_sql("players", engine, if_exists="replace", index=False)

print("Data loaded into MySQL successfully!")
