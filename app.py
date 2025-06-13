import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("IMDb_2024_Movies.csv")

# Clean Votes and Rating columns
df['Votes'] = df['Votes'].astype(str).str.replace(',', '').str.extract('(\d+)')
df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Drop rows where Genre is missing
df = df.dropna(subset=['Genre'])

# Title
st.title("IMDb 2024 Movie Dashboard")

# Filters
genre = st.selectbox("Select Genre", df['Genre'].dropna().unique())
min_rating = st.slider("Minimum Rating", 0.0, 10.0, 6.0)
min_votes = st.number_input("Minimum Votes", value=1000)

# Apply filters
filtered = df[(df['Genre'] == genre) &
              (df['Rating'] >= min_rating) &
              (df['Votes'] >= min_votes)]

# Show filtered table
st.write(f"Showing {len(filtered)} movies")
st.dataframe(filtered)

# Rating Distribution
st.subheader("Rating Distribution")
if not filtered['Rating'].dropna().empty:
    fig1, ax1 = plt.subplots()
    sns.histplot(filtered['Rating'], bins=10, kde=True, ax=ax1)
    ax1.set_xlabel("Rating")
    ax1.set_ylabel("Count")
    st.pyplot(fig1)
else:
    st.warning("No rating data available for the selected filters.")

# Genre vs Average Votes
st.subheader("Genre vs Average Votes")
valid_votes = df.dropna(subset=['Votes'])
if not valid_votes.empty:
    fig2, ax2 = plt.subplots()
    valid_votes.groupby('Genre')['Votes'].mean().sort_values().plot(kind='barh', ax=ax2)
    ax2.set_xlabel("Average Votes")
    ax2.set_ylabel("Genre")
    st.pyplot(fig2)
else:
    st.warning("No vote data available to plot genre-wise averages.")

