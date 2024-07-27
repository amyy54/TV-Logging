# TV Logging
This is a simple repository for logging TV shows, with influence from projects such as [Letterboxd](https://letterboxd.com).

## Installation
The project was made using Python 3.12, though 3.9 and above will probably work.

This project uses a custom [django-invitations](https://github.com/amyy54/django-invitations). As such, as is best practice with most projects, a virtual environment is recommended.

A [requirements.txt](requirements.txt) file is provided in the repository. After that, the project can be started just like any Django website with `python manage.py runserver`. Doing this will start it in debug mode with all the static files and everything referencing the local project area. Further customization is available with environment variables.

A `Dockerfile` is included within the root of the project for use with Docker. Running this on its own will work successfully, but static files will require another component like an nginx server to start. It's primary purpose is to run as a component of a docker compose. Should one wish to run it through docker run like any normal project, the CMD line can be replaced with `python3 manage.py runserver`, and then the port can be exposed with the `-p` argument in `docker run`.

## About
This project was initially made for an advanced web development course. Hence why earlier commits are by day, not by feature. Commit fb5de9ec371802ba1f6ce4ef41f171acccee8c52 is what was demonstrated in the course.

## License
MIT
