from predict.runner import Prediction
from flask import Flask

if __name__ == '__main__':
    app = Flask(__name__)  
    trashure_backend = Prediction(app)  # Pass the app instance to the App constructor
    trashure_backend.run()  # Call the run method on the App instance