import re
import config
from flask import Flask, request, jsonify

app = Flask(__name__)


def create_acronym(text):
    """
    Create acronym from any input string of words
    :param text: input string of words
    :return: output acronym string
    """
    r = re.compile(r"\b(?:[a-z]|\d+)", re.I)
    return ''.join(r.findall(text))


def format_name(text):
    """
    Format given full name string to match rfp requirements
    :param text: input full name string
    :return: formatted name string
    """
    first, last = text.split(" ", 1)
    return '%s %s' % (first[::-1], last)


def get_unformatted_output(raw_data):
    """
    Create list of dictionaries with all of data needed for listener api
        to create the csv file
    :param raw_data: user's input json
    :return: list of dictionary with requested data headers in rfp and a variable to sort by
    """
    out = []

    for entry in raw_data:
        if 'Federalist' in entry['pp']:
            continue

        out.append({
            'sort_by': entry['nm'],
            'name': format_name(entry['nm']),
            'party': create_acronym(entry['pp']),
            'term_start_date': '01-20-%s' % entry['tm'][:4]
            })

    return out


@app.route('/', methods=['POST'])
def index():
    # if not request.form or 'key' not in request.form or request.form['key'] != allvars.key_token:
    #     if not request.json or 'key' not in request.json or request.json['key'] != allvars.key_token:
    #         abort(400)
    unformatted = get_unformatted_output(request.get_json())
    return jsonify(unformatted), 200


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
