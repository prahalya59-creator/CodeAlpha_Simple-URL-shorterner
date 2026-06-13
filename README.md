# Simple URL Shortener

A URL shortening service built using Flask, SQLite, and SQLAlchemy.

## Features

* URL Shortening
* Custom Short URLs
* URL Validation
* Click Tracking
* Analytics Endpoint
* Redirect to Original URL

## Tech Stack

* Python
* Flask
* SQLite
* SQLAlchemy

## API Endpoints

### Create Short URL

POST /shorten

### Redirect to Original URL

GET /<code>

### View Analytics

GET /stats/<code>

## Example Analytics Response

{
"original_url": "https://google.com",
"short_code": "WaJTHe",
"clicks": 3
}

## Project Structure

URL_Shortener_Project/

1. app.py
2. models.py

3. database.db

4. requirements.txt

5. README.md
