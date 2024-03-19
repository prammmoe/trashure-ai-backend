from flask import Flask

app = Flask(__name__)

@app.route('/')
def __init__():
    return '<h1>Trashure-AI Backend</h1>'

if __name__ == '__main__':
    app.run(debug=True, port=8001)