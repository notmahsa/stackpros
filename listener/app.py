import csv
import config
import os
from flask import Flask, request, jsonify, send_file
import requests
import time

app = Flask(__name__)
PROCESSOR_ENDPOINT = os.environ['PROCESSOR_ENDPOINT']


def get_formatted_csv(unformatted_output, filename='output.csv'):
    """
    Format output from processor api to match template from rfp
    :param unformatted_output: output list of dictionaries from processor api
        (list of dictionaries with requested data headers in rfp and a variable to sort by)
    :param filename: file name for output csv
    :return: name of created file
    """
    keys = unformatted_output[0].keys()
    keys.remove('sort_by')
    headers = keys + ['entry_timestamp', 'number']
    pres_index = 1

    with open(filename, 'w') as output_file:
        writer = csv.writer(output_file, headers)
        for item in sorted(unformatted_output, key=lambda i: i['sort_by']):
            del item['sort_by']
            writer.writerow(item.values() + [time.time(), pres_index])
            pres_index += 1

    return filename


@app.route('/', methods=['POST'])
def index():
    unformatted_data = requests.post(PROCESSOR_ENDPOINT, json=request.get_json()).json()

    if len(unformatted_data) == 0:
        return "List empty, file not created.", 200

    output_csv = get_formatted_csv(unformatted_data)

    try:
        return send_file(
            output_csv,
            as_attachment=True,
            attachment_filename=output_csv,
            mimetype="text/csv"
        ), 200

    except Exception as e:
        return str(e)


@app.route('/healthz')
def health():
    message = {
        "success": True
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
