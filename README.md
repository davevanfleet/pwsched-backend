# PWSched Backend

This is the backend RESTful API for the PWSched shift scheduling app.  Front end can be found [here](https://github.com/davevanfleet/pwsched-frontend).  

This app is built to provide an easy means of scheduling public witnessing activities. Volunteers create an account and are associated with only their congregation. The app is designed to make it easy for volunteers to request shifts.
1. Service Overseers or other admins create a shift
2. Volunteers request the shifts they would like
3. Admin assigns shifts as appropriate and volunteers are notified via email.

This app is currently under development, and is being refactored from a full-stack Ruby on Rails app (found at https://github.com/dvfleet413/PWSched) during the COVID-19 pandemic, while ther's no need for it in production!  The refactored app will be written with a much cleaner, more scalable, more performant codebase.

## Technologies Used

- Flask
- MongoDB

## Installing

- Fork and Clone this repo
- set up virvual environment with `$ python3 -m venv venv` in project directory
- start venv with `$ . venv/bin/activate`
- install dependencies with `$ pip install -r requirements.txt`
- run with `$ flask run`

## Tests

Tests can be found in `./Tests`  
Test suite is written with `pytest` and can be run using `$ pytest` in project directory.

## Documentation

Swagger docs can be found by installing and running the app, then navigating to `/api/docs`  
Or you can view the static swagger docs at `./static/json`

## Contributing

Contributions are always welcome.  Please check for any open issues when submitting PRs.  If you find a bug or have a feature request please submit it as a new issue. Please also include tests an documentation as appropriate.