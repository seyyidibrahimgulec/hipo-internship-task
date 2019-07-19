# About
This project was made as an intern task for [hipolabs](https://hipolabs.com/).

## Requirements
You need to install [Docker](https://www.docker.com/) and [Docker-Compose](https://docs.docker.com/compose/).

## Installation
1. Clone this repository:`git clone git@github.com:seyyidibrahimgulec/HipoBackendTask.git`.
2. `cd` into `HipoBackendTask`
3. `docker-compose -f docker-compose.yml up`
4. Open new terminal tab.
5. `docker exec -it hipoproject_web_1 bash`
6. `python manage.py migrate`
7. `python manage.py runserver 0:8000`

## Documentation
[Documentation](https://tim-zed-31581.herokuapp.com/docs/)