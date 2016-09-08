from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/halloffame')
def hall_of_fame():
    '''
    Returns top 5 best players ranked by score

    Returns- dict
    '''
    result = {
        "message":"Nothing to show here",
        "error":"None"
    }
    return jsonify(result)

def process(data):
    result  = '''
    "message":"submission successful",
    "data": {
            "name":data['name'],
            "text":data['text']
    },
    "error":"None"''
    '''
    status = 201
    return result, status

@app.route('/play', methods=['POST'])
def play():

    # get data from request
    data = json.loads(request.data)

    print "Received- ", data

    result, status = process(data)

    return jsonify(data), status