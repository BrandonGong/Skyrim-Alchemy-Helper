from flask import Flask
from flask import template_rendered

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return template_rendered("index.html")


if __name__ == "__main__":
    app.run()