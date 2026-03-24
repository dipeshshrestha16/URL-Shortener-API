# URL-Shortener-API
A full-stack URL shortener built using Flask , with analytics, rate-limiting and click tracking. 

---
## Project overview
This project includes:
* URL shortener that generates 6 character codes.
* Rate limiting (5 request per minute).
* Click tracking for shortened URLs.
* Analytical dashboard for precision click track record past 7 days.
---
## Tech stack used
* Backend: Flask(Python)
* Frontend: Vanilla JS
* Middleware: CORS
* Database: MongoDB
* Deployment: Docker
* API Testing: Postman
---
## Deploy the project
1. Clone Git Repo (VS Code terminal):
* git clone https://github.com/dipeshshrestha16/URL-Shortener-API
* cd URL-Shortener-API

2. Running with docker:
* docker-compose up --build
* docker-compose stop (for stopping deployement)
* docker-compose down (to start the docker deployement)

3. Accessing the localhost:
* Frontend: https://localhost/5500
* Backend: https://localhost/5000

