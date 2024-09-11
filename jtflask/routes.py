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

@app.route('/jtdash/eff-year-built', methods=['POST'])
def handle_eff_year_built():
    if request.method == 'POST':
        request_body = request.get_json()
        # Process the selections data as needed (in this case, for Effective Year Built)
        print(f"Received Effective Year Built selection: {request_body}")

        # Return a nicely formatted JSON response
        return app.response_class(
            response=jsonify({"status": "success", "selection": request_body}).get_data(as_text=True),
            status=200,
            mimetype='application/json',
            headers={'Content-Type': 'application/json'}
        )

@app.route('/jtdash/living-area', methods=['POST'])
def handle_living_area():
    if request.method == 'POST':
        request_body = request.get_json()
        # Process the selections data as needed (in this case, for Total Living Area)
        print(f"Received Living Area selection: {request_body}")

        return app.response_class(
            response=jsonify({"status": "success", "selection": request_body}).get_data(as_text=True),
            status=200,
            mimetype='application/json',
            headers={'Content-Type': 'application/json'}
        )

@app.route('/jtdash/just-value', methods=['POST'])
def handle_just_value():
    if request.method == 'POST':
        request_body = request.get_json()
        # Process the selections data as needed (in this case, for Just Value)
        print(f"Received Just Value selection: {request_body}")

        return app.response_class(
            response=jsonify({"status": "success", "selection": request_body}).get_data(as_text=True),
            status=200,
            mimetype='application/json',
            headers={'Content-Type': 'application/json'}
        )

@app.route('/jtdash/update-building-stats', methods=['POST'])
def update_building_stats():
    if request.method == 'POST':
        request_body = request.get_json()
        # Process the building stats data (DORUC, EFFYRBLT, TOTLVGAREA, JV)
        print(f"Received Building Stats: {request_body}")

        # Return a success response
        return jsonify({"status": "success", "received_data": request_body})