# 🍔 Google scraper

#### Requirements
To run this project you will need a Docker engine and docker-compose \
You also need to obtain a [google custom search](https://developers.google.com/custom-search/v1/introduction) key for your google account

#### Before run
Copy **.env.example** file to **.env** file \
Assign your google custom search key to **GOOGLE_KEY** setting \
Create data volume for the app \
`docker volume create google_scraper_data`

#### Run 
`docker-compose up`

#### Test
`docker-compose run app pytest`