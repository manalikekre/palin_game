from flask import Flask, jsonify, request
import json
import re
# setup redis
import redis
redis_hndlr = redis.Redis(host='localhost', port=6379, db=0)

def delete_data():
    redis_hndlr.delete('users')

# setup flask
app = Flask(__name__)

@app.before_first_request
def reset_data():
    """
    Reset user score
    """
    print 'only once'
    delete_data()

def get_score(text):
    '''
    Computes the score corresponding to given text

    TBD, implement is_palindrome logic here
    :param text: string
    :return: integer

    '''
    text = re.sub('[^A-Za-z0-9]','',text)
    text = text.lower()
    print text
    score = 0
    if text == text[::-1]:
        score = len(text)/2
    print 'score ',score
    return score

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
        return {user:redis_hndlr.hget('users', user)}

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
    result, status = process(top_five, "Top 5")
    return jsonify(result), status
    #return jsonify(top_five)

@app.route('/all')
def get_all():
    '''
    Returns complete user data
    '''
    print 'inside get_all'
    result, status = process(get_data(user='all'), "all scores")
    return jsonify(result), status
    #return jsonify({data: get_data(user='all')})

@app.route('/user/<username>')
def get_user(username):
    '''
    Returns particular user data
    '''
    print 'inside get_user'
    result, status = process(get_data(username), "user data")
    return jsonify(result), status

def process(data,msg):

    #temp_result = put_data(data)

    result  = {
    "message":msg,
    "data": data,
    "error":"None"''
    }
    status = 201
    return result, status

@app.route('/play', methods=['POST'])
def play():

    # get data from request
    data = json.loads(request.data)

    print "Received- ", data

    result, status = process(put_data(data),"score added")

    return jsonify(result), status