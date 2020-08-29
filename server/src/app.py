from flask import Flask, render_template, url_for, make_response
import os
import time

app = Flask(__name__, static_url_path="", static_folder="../../static/", template_folder="templates/")

# index route
@app.route('/')
@app.route("/home")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
