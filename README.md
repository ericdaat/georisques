# Georisques

Python web application for scrapping [georisques.gouv.fr](http://www.georisques.gouv.fr).
Given a latitude and a longitude, return the list of risks impacting the area.

## Installation

Create a virtual environment and install the dependencies:

``` text
source venv/bin/activate;
pip install -r requirements.txt
```

You will also need to install `redis` and `chromedriver`.
If you are on macos, run the following:

``` text
brew cask install chromedriver;
brew install redis;
brew services start redis;
```

## Run the app

Run the app in `DEBUG` mode on port `5000`:

``` text
FLASK_APP=src/application FLASK_DEBUG=True flask run
```

Run the app for production on port `8080`:

``` text
export PYTHONPATH=src:$PYTHONPATH
python src/application/wsgi.py
```

The app should launch, asking you for latitude and longitude values.
Once provided, you shall see something like this:

![preview](preview.png)
