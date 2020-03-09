# community_api

API built to extend a mock application's backend functionality.  Built primarily with Python, Flask, SQLAlchemy, pytest, and Marshmallow.

## API Spec & Examples

[API Spec](https://documenter.getpostman.com/view/10629414/SzRxVpzW?version=latest) created with [Postman](https://www.postman.com/).

If you use Postman, you can download [the entire Collection of requests](https://www.getpostman.com/collections/a0b3e116a90bf22c8d44) for this API to easily interact with it once you have it running locally.

## Install instructions

_(Python 3.7.3 or higher is required. [Download Python](https://www.python.org/downloads/))_

From the command line:
```bash
# Clone the repository
$ git clone https://github.com/b2397/community_api

# Create the virtual environment
$ cd community_api
$ python3 -m venv venv

# Activate the virtual environment
$ source venv/bin/activate

# Install the required packages using pip
$ python3 -m pip install -r requirements.txt
```

## Run

With the virtual environment still activated from the last step:

```bash
# Set up the database
$ python setup.py

# Run the application
$ python run.py
```

- Should see a message in the terminal saying: * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
- In a web browser, visit http://127.0.0.1:5000/users/
- Should see []
- Visit the [API Spec](https://documenter.getpostman.com/view/10629414/SzRxVpzW?version=latest) to see all possible interactions with the API


## Test instructions

If the application is still running, press CTRL+C in the terminal to quit it.  Then, from the command line:

```bash
$ pytest
```

## Future Improvements

- Add API versioning
- Add SQL scripts to load the database with more robust test data, improve the test suite
- Extend the hypothetical existing application's authentication setup to this app
- Possibly adopt OpenAPI 3.0 standard with a YAML file and something like Connexion to map the YAML to the Python code
- Put the bookmarked questions and answers in the user blueprint instead of having their own endpoints
- Add pagination and limits to the GET routes