from flask import render_template, request
from flask import current_app as app


@app.route('/')
def home():
    return render_template('index.html', base_url=request.base_url)

@app.route('/selections',  methods=['POST'])
def handle_selections():
     if request.method == 'POST':
        request_body = request.get_json()
        selections = request_body[selections]
        return '''<h1>Building Selections: {}</h1>'''.format(selections)