from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.imdb.com/search/title/?year=2024&title_type=feature&"
driver.get(url)
time.sleep(2)

titles, genres, ratings, votes, durations = [], [], [], [], []

for _ in range(2):  
    movies = driver.find_elements(By.CLASS_NAME, 'lister-item')

    for movie in movies:
        try:
            titles.append(movie.find_element(By.TAG_NAME, 'h3').text.split('\n')[0])
        except:
            titles.append("N/A")
        try:
            genres.append(movie.find_element(By.CLASS_NAME, 'genre').text.strip())
        except:
            genres.append("N/A")
        try:
            ratings.append(movie.find_element(By.CLASS_NAME, 'ratings-imdb-rating').text.strip())
        except:
            ratings.append("N/A")
        try:
            votes.append(movie.find_element(By.XPATH, ".//span[@name='nv']").text.replace(',', ''))
        except:
            votes.append("N/A")
        try:
            durations.append(movie.find_element(By.CLASS_NAME, 'runtime').text.replace(" min", ""))
        except:
            durations.append("N/A")

    try:
        next_button = driver.find_element(By.LINK_TEXT, "Next »")
        next_button.click()
        time.sleep(2)
    except:
        break

driver.quit()

df = pd.DataFrame({
    'Movie Name': titles,
    'Genre': genres,
    'Rating': pd.to_numeric(ratings, errors='coerce'),
    'Votes': pd.to_numeric(votes, errors='coerce'),
    'Duration': pd.to_numeric(durations, errors='coerce')
})

df.to_csv("IMDb_2024_Movies.csv", index=False)
print("✅ Data saved to IMDb_2024_Movies.csv")
