from predict import App
from flask import Flask

if __name__ == '__main__':
    app = Flask(__name__)  
    trashure_backend = App(app)  # Pass the app instance to the App constructor
    trashure_backend.run()  # Call the run method on the App instance
