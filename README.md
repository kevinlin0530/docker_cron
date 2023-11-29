# Cron Dockerized Web Scraper

This Dockerized web scraper is designed to run a web scraping job at regular intervals and store the results in a database.

## Getting Started

Make sure you have Docker installed on your machine.

- [Docker](https://docs.docker.com/get-docker/)

## Build the Docker Image

Open a terminal and navigate to the project directory.

```bash
docker build -t cron .
```
## Run the Docker Container

Execute the following command to run the Docker container in detached mode.

docker run --name cron -d cron

## Schedule the Web Scraper
The web scraper is set to run every hour and fetch data from the web. The results will be stored in the database.

## Maintenance
To stop the running container, use the following command:

```bash
docker stop cron
```

To remove the container, run:

```bash
docker rm cron
```

Configuration
The web scraping job frequency and other configurations can be adjusted in the cron configuration file (hello-cron). Refer to the cron syntax for setting the desired schedule.
