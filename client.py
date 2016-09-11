import requests

def talk_to_server(url, data, method):
    print 'url- ', url
    print 'data- ', data
    print 'method- ', method

    response = None
    # hit the server here
    # process here
    return response

def get_all():
    url = "http://localhost:5000/all"
    method = 'GET'
    result = talk_to_server(
            url=url,
            data=None,
            method=method
    )
    return result

def hall_of_fame():
    url = "http://localhost:5000/halloffame"
    method = 'GET'
    result = talk_to_server(
        url=url,
        data=None,
        method=method
    )
    return result

def get_user(user):
    url = "http://localhost:5000/user/" + user
    method = 'GET'
    result = talk_to_server(
        url=url,
        data=None,
        method=method
    )
    return result

def play(name, text):
    print 'name- ', name
    print 'text- ', text
    result = talk_to_server(
        url=url,
        data=None,
        method=method
    )
    return result
