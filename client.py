import requests, json

HOST = "localhost"

def talk_to_server(url, data, method):
    '''
    talks to server sends & recieves data.
    :param url: string
    :param data: dict
    :param method: string
    :return: dict
    '''
    #print 'url- ', url
    #print 'data- ', data
    #print 'method- ', method
    headers = {"Content-Type": "application/json"}

    url = 'http://' + HOST + ':5000' + url
    try:
        if method == 'POST' :
            response = requests.post(url, data=json.dumps(data), headers=headers)
        else:
            response = requests.get(url)
        
        return response.json()
    except Exception as e:
        print "An error occured"
        return {
            'data' : None,
            'message': e
        }

def get_all():
    '''
    fetches all players and their scores
    return: dict
    '''
    url = "/all"
    method = 'GET'
    result = talk_to_server(
            url=url,
            data=None,
            method=method
    )
    return result

def hall_of_fame():
    '''
    fetches top 5 players
    return: dict
    '''
    url = "/halloffame"
    method = 'GET'
    result = talk_to_server(
        url=url,
        data=None,
        method=method
    )
    return result

def get_user(user):
    '''
    fetches score for input user
    :param user: string
    return: dict
    '''
    url = "/user/" + user
    method = 'GET'
    result = talk_to_server(
        url=url,
        data=None,
        method=method
    )
    return result

def play(data):
    '''
    submits data['name'] & data['text']
    :param data: dict
    return: dict
    '''
    url = "/play"
    method = 'POST'
    '''
    try:
        print 'name- ', data['name']
        print 'text- ', data['name']
    except:
        print 'bad parameter'
    '''
    result = talk_to_server(
        url=url,
        data=data,
        method=method
    )
    return result
