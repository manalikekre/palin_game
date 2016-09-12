from flask import Flask, jsonify, request, url_for
import json
import re
import urllib
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
            return redis_hndlr.hgetall('users'), "Fetched data for all users", 200
        else:
            return {user:redis_hndlr.hget('users', user)}, "Fetched data for user "+user, 200
    except Exception as e:
        print "Error occured while fetching data"
        print e
        return "None", "Error while fetching data", 503

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
        if redis_hndlr.hget('users', data['name']) is None:
            status = 201
            msg = "created new player"
        else:
            status = 200
            msg = "updated player score"

        redis_hndlr.hincrbyfloat('users', data['name'], get_score(data['text']))
        current_count, mesg, stat = get_data(user=data['name'])
        print 'current_count- ', current_count[data['name']]
        return {
            "name" : data['name'],
            "score" : current_count[data['name']]
        }, msg, status
    except Exception as e:
        print "Error occured while updating data"
        print e
        return "None", "Error while updating data", 503
    

@app.route('/halloffame')
def hall_of_fame():
    '''
    Returns top 5 best players ranked by score
    :return :json, int
    '''
    incr_hits('halloffame')
    print 'inside hall_of_fame'
    status = 404
    try:
        all_data, msg, status = get_data(user='all')
        print all_data
        top_five = sorted(all_data.items(), key = lambda item :float(item[1]), reverse=True)[:5]
        print top_five
        data_to_send = [{'name': item[0], 'score': item[1]} for item in top_five]
        result= format_data(data_to_send, msg, status)
        return jsonify(result), status
    except Exception as e:
        print "Error in halloffame"
        print e
        result = format_data("None", msg, status)
        return jsonify(result), status

    
    
    #return jsonify(top_five)

@app.route('/all')
def get_all():
    '''
    Returns complete player data
    '''
    incr_hits('all')
    print 'inside get_all'
    data_to_send = "None"
    status = 404
    try:
        val, msg, status = get_data(user='all')
        print val
        data_to_send = [{'name': k, 'score':v} for k,v in val.items()]
    except Exception, e:
        print "Error in get_all"
        print e
    result = format_data(data_to_send, msg, status)
    return jsonify(result), status
    #return jsonify({data: get_data(user='all')})

@app.route('/user/<username>')
def get_user(username):
    '''
    Returns specified player score
    '''
    status = 404
    incr_hits('user')
    print 'inside get_user'
    data_to_send = "None"
    try:
        val, msg, status = get_data(username)
        data_to_send = {'name': username, 'score':val[username]}
    except Exception as e:
        "Error in get_user"
        print e
         
        
    result = format_data(data_to_send, msg, status)
    return jsonify(result), status

def format_data(data, msg, status):
    """
    format_data the data to return
    """

    result  = {
    "message":msg,
    "data": data,
    "error": "None",
    "status" : status   
    }
    #status = 201
    return result


@app.route('/play', methods=['POST'])
def play():
    """
    Lets a player submit username and text.
    adds score corresponding to the text entered.
    accepts data {"name" : String, "text": String}

    sample: {"name" : "John Doe", "text": "Madam I'm Adam!"}
    response:{"data" : { "name": "John Doe", "score": '5.5'}, error: "None", "message": "Data updated Successufuly" }
    """
    status = 404
    incr_hits('play')
    data = json.loads(request.data)

    # take care of trailing/leading spaces in name
    data["name"] = data["name"].strip()

    print "Received- ", data
    val = "None"

    try:
        val, msg, status = put_data(data)
        
    except Exception as e:
        print "Error in play"
        print e
        
    result = format_data(val,msg, status)
    return jsonify(result), status


@app.route('/')
def list_routes():
    """
    lists all urls available for this app
    """
    output = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':

            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            #line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append({'url': url, 'methods': methods, 'doc':eval(rule.endpoint).__doc__.strip()})
    
    for line in sorted(output):
        print line
    return jsonify({'data':output}), 200

@app.errorhandler(404)
def page_not_found(error):
    print 'inside page not found'
    return jsonify(format_data('None', 'Page Not Found, visit / to check available routes.', 404)), 404
    

if __name__ == '__main__':
    app.run(
        threaded=True,
        host='0.0.0.0',
        port=5000,
        debug=False
    )
