from flask import Flask, jsonify, request
import json

# setup redis
import redis
redis_hndlr = redis.Redis(host='localhost', port=6379, db=0)

# setup flask
app = Flask(__name__)

def get_score(text):
    '''
    Computes the score corresponding to given text

    TBD, implement is_palindrome logic here
    :param text: string
    :return: integer
    '''
    return len(text)

def get_data(user='all'):
    '''
    Retrieves data from redis in-memory data

    By default, fetches all the data, and if
    name is given, fetches score corresponding
    to that user

    :param name: string
    :return: dict
    '''
    print 'inside get_data'
    print 'user- ', user
    if user == 'all':
        return redis_hndlr.hgetall('users')
    else:
        return redis_hndlr.hget('users', user)

def put_data(data):
    print 'inside put_data'
    print 'data- ', data

    redis_hndlr.hincrby('users', data['name'], get_score(data['text']))

    current_count = get_data(user=data['name'])
    print 'current_count- ', current_count

    return {
        data['name']:current_count
    }

@app.route('/halloffame')
def hall_of_fame():
    '''
    Returns top 5 best players ranked by score
    '''
    print 'inside hall_of_fame'
    all_data = get_data(user='all')

    top_five = sorted(all_data.items(), key=all_data.get, reverse=True)
    return jsonify(top_five)

@app.route('/all')
def get_all():
    '''
    Returns complete user data
    '''
    print 'inside get_all'
    return jsonify(get_data(user='all'))

def process(data):

    temp_result = put_data(data)

    result  = {
    "message":"submission successful",
    "data": temp_result,
    "error":"None"''
    }
    status = 201
    return result, status

@app.route('/play', methods=['POST'])
def play():

    # get data from request
    data = json.loads(request.data)

    print "Received- ", data

    result, status = process(data)

    return jsonify(result), status