from flask import render_template, request, jsonify, json
from flask import current_app as app


@app.route('/')
def home():
    return render_template('index.html', base_url=request.base_url)

#local storage
@app.route('/jtdash/selection', methods=['POST'])
def handle_selections():
    if request.method == 'POST':
        request_body = request.get_json()

        # Process the selections data as needed
        print(f"Received selection: {request_body}")

        # Initialize dictionaries to store the data for each chart category
        doruc_data = {}
        effyrblt_data = {}
        totlvgarea_data = {}
        jv_data = {}

        # Group data by each category
        for entry in request_body.get("buildings", []):
            try:
                # Process each field as described
                doruc_code = entry["DORUC"]
                doruc_data[doruc_code] = doruc_data.get(doruc_code, 0) + 1

                effyrblt_year = entry["EFFYRBLT"]
                if effyrblt_year is not None:
                    if effyrblt_year < 1950:
                        effyrblt_data['<1950'] = effyrblt_data.get('<1950', 0) + 1
                    elif 1950 <= effyrblt_year < 1975:
                        effyrblt_data['1950-1975'] = effyrblt_data.get('1950-1975', 0) + 1
                    elif 1975 <= effyrblt_year < 2000:
                        effyrblt_data['1975-2000'] = effyrblt_data.get('1975-2000', 0) + 1
                    else:
                        effyrblt_data['>2000'] = effyrblt_data.get('>2000', 0) + 1

                totlvgarea = entry["TOTLVGAREA"]
                if totlvgarea is not None:
                    if totlvgarea < 1000:
                        totlvgarea_data['<1000 sq ft'] = totlvgarea_data.get('<1000 sq ft', 0) + 1
                    elif 1000 <= totlvgarea < 2000:
                        totlvgarea_data['1000-2000 sq ft'] = totlvgarea_data.get('1000-2000 sq ft', 0) + 1
                    elif 2000 <= totlvgarea < 3000:
                        totlvgarea_data['2000-3000 sq ft'] = totlvgarea_data.get('2000-3000 sq ft', 0) + 1
                    else:
                        totlvgarea_data['>3000 sq ft'] = totlvgarea_data.get('>3000 sq ft', 0) + 1

                jv_value = entry["JV"]
                if jv_value is not None:
                    if jv_value < 100000:
                        jv_data['<$100k'] = jv_data.get('<$100k', 0) + 1
                    elif 100000 <= jv_value < 500000:
                        jv_data['$100k-$500k'] = jv_data.get('$100k-$500k', 0) + 1
                    elif 500000 <= jv_value < 1000000:
                        jv_data['$500k-$1M'] = jv_data.get('$500k-$1M', 0) + 1
                    else:
                        jv_data['>$1M'] = jv_data.get('>$1M', 0) + 1

            except (KeyError, ValueError) as e:
                return app.response_class(
                    response=json.dumps({"error": f"Error processing entry: {str(e)}"}),
                    status=400,
                    mimetype='application/json',
                    headers={'Content-Type': 'application/json'}
                )

        formatted_data = {
            "doruc_chart": {
                "labels": list(doruc_data.keys()),
                "values": list(doruc_data.values())
            },
            "effyrblt_chart": {
                "labels": list(effyrblt_data.keys()),
                "values": list(effyrblt_data.values())
            },
            "totlvgarea_chart": {
                "labels": list(totlvgarea_data.keys()),
                "values": list(totlvgarea_data.values())
            },
            "jv_chart": {
                "labels": list(jv_data.keys()),
                "values": list(jv_data.values())
            }
        }

        # Return formatted data
        return app.response_class(
            response=jsonify({"status": "success", "selection": formatted_data}).get_data(as_text=True),
            status=200,
            mimetype='application/json',
            headers={'Content-Type': 'application/json'}
        )

# dcc.Store() version
# @app.route('/jtdash/selection', methods=['POST'])
# def handle_selections():
#     if request.method == 'POST':
#         request_body = request.get_json()
#
#         # Process the selections data as needed
#         print(f"Received selection: {request_body}")
#
#         # Initialize dictionaries to store the data for each chart category
#         doruc_data = {}
#         effyrblt_data = {}
#         totlvgarea_data = {}
#         jv_data = {}
#
#         # Group data by each category
#         for entry in request_body.get("buildings", []):
#             try:
#                 # Convert DORUC to integer
#                 doruc_code = entry["DORUC"]
#                 doruc_data[doruc_code] = doruc_data.get(doruc_code, 0) + 1
#
#                 # EFFYRBLT chart: Group by Effective Year Built, and count occurrences per year range
#                 effyrblt_year = entry["EFFYRBLT"]
#                 if effyrblt_year is not None:
#                     if effyrblt_year < 1950:
#                         effyrblt_data['<1950'] = effyrblt_data.get('<1950', 0) + 1
#                     elif 1950 <= effyrblt_year < 1975:
#                         effyrblt_data['1950-1975'] = effyrblt_data.get('1950-1975', 0) + 1
#                     elif 1975 <= effyrblt_year < 2000:
#                         effyrblt_data['1975-2000'] = effyrblt_data.get('1975-2000', 0) + 1
#                     else:
#                         effyrblt_data['>2000'] = effyrblt_data.get('>2000', 0) + 1
#
#                 # TOTLVGAREA chart: Group by ranges of living area (square footage)
#                 totlvgarea = entry["TOTLVGAREA"]
#                 if totlvgarea is not None:
#                     if totlvgarea < 1000:
#                         totlvgarea_data['<1000 sq ft'] = totlvgarea_data.get('<1000 sq ft', 0) + 1
#                     elif 1000 <= totlvgarea < 2000:
#                         totlvgarea_data['1000-2000 sq ft'] = totlvgarea_data.get('1000-2000 sq ft', 0) + 1
#                     elif 2000 <= totlvgarea < 3000:
#                         totlvgarea_data['2000-3000 sq ft'] = totlvgarea_data.get('2000-3000 sq ft', 0) + 1
#                     else:
#                         totlvgarea_data['>3000 sq ft'] = totlvgarea_data.get('>3000 sq ft', 0) + 1
#
#                 # JV chart: Group by Just Value (JV) ranges
#                 jv_value = entry["JV"]
#                 if jv_value is not None:
#                     if jv_value < 100000:
#                         jv_data['<$100k'] = jv_data.get('<$100k', 0) + 1
#                     elif 100000 <= jv_value < 500000:
#                         jv_data['$100k-$500k'] = jv_data.get('$100k-$500k', 0) + 1
#                     elif 500000 <= jv_value < 1000000:
#                         jv_data['$500k-$1M'] = jv_data.get('$500k-$1M', 0) + 1
#                     else:
#                         jv_data['>$1M'] = jv_data.get('>$1M', 0) + 1
#
#             except (KeyError, ValueError) as e:
#                 # Handle missing keys or invalid values in entry
#                 return app.response_class(
#                     response=json.dumps({"error": f"Error processing entry: {str(e)}"}),
#                     status=400,
#                     mimetype='application/json',
#                     headers={'Content-Type': 'application/json'}
#                 )
#
#         # Prepare the formatted data for each chart
#         formatted_data = {
#             "doruc_chart": {
#                 "labels": list(doruc_data.keys()),
#                 "values": list(doruc_data.values())
#             },
#             "effyrblt_chart": {
#                 "labels": list(effyrblt_data.keys()),
#                 "values": list(effyrblt_data.values())
#             },
#             "totlvgarea_chart": {
#                 "labels": list(totlvgarea_data.keys()),
#                 "values": list(totlvgarea_data.values())
#             },
#             "jv_chart": {
#                 "labels": list(jv_data.keys()),
#                 "values": list(jv_data.values())
#             }
#         }
#
#         # Return the formatted data for each chart
#         return app.response_class(
#             response=jsonify({
#                 "status": "success",
#                 "selection": formatted_data
#             }).get_data(as_text=True),
#             status=200,
#             mimetype='application/json',
#             headers={'Content-Type': 'application/json'}
#         )


# @app.route('/jtdash/selection', methods=['POST'])
# def handle_selections():
#     if request.method == 'POST':
#         request_body = request.get_json()
#         # Process the selections data as needed
#         print(f"Received selection: {request_body}")
#
#         # Return a nicely formatted JSON response
#         return app.response_class(
#             response=jsonify({"status": "success", "selection": request_body}).get_data(as_text=True),
#             status=200,
#             mimetype='application/json',
#             headers={'Content-Type': 'application/json'}
#         )

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