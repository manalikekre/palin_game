from flask import Flask, jsonify, request
import json
import re
# setup redis
import redis
redis_hndlr = redis.Redis(host='localhost', port=6379, db=0)
# setup flask
app = Flask(__name__)

def delete_data():
    """
    Deletes users dict from redis
    """
    try:
        redis_hndlr.delete('users')
    except Exception as e:
        print "Error occured while deleting users data"
        print e

def delete_hits():
    """
    Deletes hits dict from redis
    """
    try:
        redis_hndlr.delete('hits')
    except Exception as e:
        print "Error occured while deleting hits data"
        print e

def incr_hits(api):
    """
    increases hits count for an api
    :param api: string
    """
    try:
        redis_hndlr.hincrby('hits', api, 1)
    except Exception as e:
        print 'error in incr_hits'
        print e

@app.before_first_request
def reset_data():
    """
    Reset user score data, and hits count data
    """
    print 'only once'
    delete_data()
    delete_hits()
    
def get_score(text):
    '''
    Computes the score corresponding to given text
    If the input is a palindrome then score is half of the size of the palindrome size
    otherwise zero.
    :param text: string
    :return: integer

    '''
    text = re.sub('[^A-Za-z0-9]','',text)
    text = text.lower()
    print text
    score = 0
    if text == text[::-1]:
        score = len(text)/2.0
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
    try:
        if user == 'all':
            return redis_hndlr.hgetall('users'), "Fetched data for all users"
        else:
            return {user:redis_hndlr.hget('users', user)}, "Fetched data"
    except Exception as e:
        print "Error occured while fetching data"
        print e
        return None, "Error while fetching data"

def put_data(data):
    '''
    Updates data from redis in-memory data and increases score

    Returns updated data for input user success/failure message
    Eg: {name:"Mohan" text: "Madam I'm Adam"}
    :param name: dict 
    :return: tuple
    '''
    print 'inside put_data'
    print 'data- ', data

    try:
        redis_hndlr.hincrbyfloat('users', data['name'], get_score(data['text']))
        current_count = get_data(user=data['name'])
        print 'current_count- ', current_count
        return {
        data['name']:current_count
        }, "Data updated Successufuly"
    except Exception as e:
        print "Error occured while updating data"
        print e
        return None, "Error while updating data"
    

@app.route('/halloffame')
def hall_of_fame():
    '''
    Returns top 5 best players ranked by score
    :return :json, int
    '''
    incr_hits('halloffame')
    print 'inside hall_of_fame'
    try:
        all_data, msg = get_data(user='all')
        top_five = sorted(all_data.items(), key=all_data.get, reverse=True)
        result, status = process(top_five, msg)
        return jsonify(result), status
    except Exception as e:
        print "Error in halloffame"
        print e
        result, status = process(None, msg)
        return jsonify(result), status

    
    
    #return jsonify(top_five)

@app.route('/all')
def get_all():
    '''
    Returns complete user data
    '''
    incr_hits('all')
    print 'inside get_all'
    try:
        val, msg = get_data(user='all')
    except Exception, e:
        print "Error in get_all"
        print e
    result, status = process(val, msg)
    return jsonify(result), status
    #return jsonify({data: get_data(user='all')})

@app.route('/user/<username>')
def get_user(username):
    '''
    Returns specified user data
    '''
    incr_hits('user')
    print 'inside get_user'
    try:
        val, msg = get_data(username)
        
    except Exception as e:
        "Error in get_user"
        print e
         
        
    result, status = process(val, msg)
    return jsonify(result), status

def process(data,msg):
    """
    process the data to return
    """

    result  = {
    "message":msg,
    "data": data,
    "error":"None"''
    }
    status = 201
    return result, status

@app.route('/play', methods=['POST'])
def play():
    """
    Lets user submit name and text
    """
    incr_hits('play')
    data = json.loads(request.data)

    # take care of trailing/leading spaces in name
    data["name"] = data["name"].strip()

    print "Received- ", data

    try:
        val, msg = put_data(data)
        
    except Exception as e:
        print "Error in play"
        print e
        
    result, status = process(val,msg)
    return jsonify(result), status

if __name__ == '__main__':
    app.run(
        threaded=True,
        host='0.0.0.0',
        port=5000,
        debug=False
    )
