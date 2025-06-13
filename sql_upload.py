import pandas as pd
from sqlalchemy import create_engine

# Load scraped data
df = pd.read_csv("IMDb_2024_Movies.csv")

# Connect to MySQL (replace with your DB password)
engine = create_engine("mysql+pymysql://root:manju@localhost/imdb_db")

# Insert data
df.to_sql(name='movies_2024', con=engine, if_exists='replace', index=False)
print("✅ Data uploaded to MySQL database.")