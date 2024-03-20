# app.py
from predict import App
from flask import Flask

if __name__ == '__main__':
    app = Flask(__name__)  # Create the Flask app instance
    my_app = App(app)  # Pass the app instance to the App constructor
    my_app.run()  # Call the run method on the App instance
