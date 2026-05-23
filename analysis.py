import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="fifa_db"
)

print("Connected to MySQL!")

# Query 1 - Top 10 highest rated players
query = """
SELECT short_name, club_name, nationality_name, overall, potential, wage_eur, value_eur
FROM players
ORDER BY overall DESC
LIMIT 10
"""

top_players = pd.read_sql(query, conn)
print(top_players)

# Visualize top 10 players
sns.set_style("darkgrid")
plt.figure(figsize=(12, 6))
sns.barplot(data=top_players, x="short_name", y="overall", palette="viridis")
plt.title("Top 10 Highest Rated Players in FIFA 22", fontsize=16)
plt.xlabel("Player")
plt.ylabel("Overall Rating")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
