from flask import render_template, request
from flask import current_app as app


@app.route('/')
def home():
    return render_template('index.html', base_url=request.base_url)
