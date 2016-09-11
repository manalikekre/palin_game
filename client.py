import requests, json

def talk_to_server(url, data, method):
    '''
    talks to server sends & recieves data.
    :param url: string
    :param data: dict
    :param method: string
    :return: dict
    '''
    print 'url- ', url
    print 'data- ', data
    print 'method- ', method
    headers = {"Content-Type": "application/json"}
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
    url = "http://localhost:5000/all"
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
    url = "http://localhost:5000/halloffame"
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
    url = "http://localhost:5000/user/" + user
    method = 'GET'
    result = talk_to_server(
        url=url,
        data=None,
        method=method
    )
    return result

def play(name, text):
    '''
    submits user name and user input
    :param name: string
    :param text: string
    return: dict
    '''
    url = "http://localhost:5000/play"
    method = 'POST'
    print 'name- ', name
    print 'text- ', text
    result = talk_to_server(
        url=url,
        data={'name':name, 'text':text},
        method=method
    )
    return result
