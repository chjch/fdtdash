from flask import render_template, request, jsonify
from flask import current_app as app


@app.route('/')
def home():
    return render_template('index.html', base_url=request.base_url)


@app.route('/jtdash/selection', methods=['POST'])
def handle_selections():
    if request.method == 'POST':
        request_body = request.get_json()
        # Process the selections data as needed
        print(f"Received selection: {request_body}")

        # Return a nicely formatted JSON response
        return app.response_class(
            response=jsonify({"status": "success", "selection": request_body}).get_data(as_text=True),
            status=200,
            mimetype='application/json',
            headers={'Content-Type': 'application/json'}
        )