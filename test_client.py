from multiprocessing.dummy import Pool as ThreadPool
import client
import time
import random
import main
import re

def clear_data():
    '''Deletes records in redis db'''
    # TBD - Use separate db for testing
    main.delete_data()

def test_get_all():
    '''Tests get all fnctionality'''

    print '\nTesting get all- ',
    # reset data on redis database for testing
    clear_data()
    sample_data = [
        {
            "name": "abcd",
            "text": "abcdeedcba"
        },
        {
            "name": "efgh",
            "text": "abcddcba"
        },
        {
            "name": "ijkl",
            "text": "abcdeffedcba"
        },
        {
            "name": "mnop",
            "text": "abba"
        },
        {
            "name": "qrst",
            "text": "123456789987654321"
        },
        {
            "name": "uvwx",
            "text": "a"
        },
    ]
    expected_get_all = {}
    for item in sample_data:
        expected_get_all[item["name"]] = expected_get_all.get(item["name"], 0) + get_score(item["text"])
    #print 'expected_get_all- ',expected_get_all

    # submit data
    for item in sample_data:
        client.play(item)

    # retrieve all user data
    recieved_get_all = { item['name']: float(item['score']) for item in client.get_all()['data']}
    #print 'recieved_get_all- ',recieved_get_all
    if recieved_get_all == expected_get_all:
        print 'PASSED!'
    else:
        print 'FAILED!'

def test_get_user():
    '''Tests if a user's score persists & is retrievable'''

    print '\nTesting get user- ',
    # reset data on redis database for testing
    clear_data()
    sample_data = [
        {
            "name": "abcd",
            "text": "abcdeedcba"
        },
        {
            "name": "abcd",
            "text": "abcdeedcba"
        },
        {
            "name": "efgh",
            "text": "abcddcba"
        },
        {
            "name": "ijkl",
            "text": "abcdeffedcba"
        },
        {
            "name": "mnop",
            "text": "abba"
        },
        {
            "name": "qrst",
            "text": "123456789987654321"
        },
        {
            "name": "uvwx",
            "text": "a"
        },
    ]
    user_names = {item['name'] for item in sample_data}
    expected_get_user = {}
    for item in sample_data:
        expected_get_user[item["name"]] = expected_get_user.get(item["name"], 0) + get_score(item["text"])
    #print 'expected_get_user- ',expected_get_user

    # submit data
    for item in sample_data:
        client.play(item)

    # retrieve user data
    recieved_get_user = { user : float(client.get_user(user)['data']['score']) for user in user_names}
    #print 'recieved_get_user- ',recieved_get_user
    if recieved_get_user == expected_get_user:
        print 'PASSED!'
    else:
        print 'FAILED!'

def test_play():
    '''Tests if a user's score is incremented properly'''
    print '\nTesting play- ',
    # reset data on redis database for testing
    clear_data()

    sample_data =  [
        {
            "name": "abcd",
            "text": "abcdeedcba"
        },
        {
            "name": "abcd",
            "text": "abcdeedcba"
        },
        {
            "name": "ijkl",
            "text": "abcdeffedcba"
        },
        {
            "name": "mnop",
            "text": "abba"
        },
        {
            "name": "qrst",
            "text": "123456789987654321"
        },
        {
            "name": "qrst",
            "text": "123456789987654321"
        },
    ]

    expected_scores_dict = {}
    for item in sample_data:
        expected_scores_dict[item["name"]] = expected_scores_dict.get(item["name"], 0) + get_score(item["text"])

    #print expected_scores_dict

    # submit data
    for item in sample_data:
        client.play(item)

    # retrieve halloffame data
    recieved_scores_dict = { item["name"]:client.get_user(item["name"])["data"]["score"] for item in sample_data}

    #print 'recieved_scores_dict- ', recieved_scores_dict
    if recieved_scores_dict == recieved_scores_dict:
        print 'PASSED!'
    else:
        print 'FAILED!'

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

    score = 0
    if text == text[::-1]:
        score = len(text)/2.0
    return score

def test_halloffame():
    '''Tests if halloffame correctly returns top5 users'''
    print '\nTesting halloffame- ',
    # reset data on redis database for testing
    clear_data()
    sample_data =  [
        {
            "name": "abcd",
            "text": "abcdeedcba"
        },
        {
            "name": "efgh",
            "text": "abcddcba"
        },
        {
            "name": "ijkl",
            "text": "abcdeffedcba"
        },
        {
            "name": "mnop",
            "text": "abba"
        },
        {
            "name": "qrst",
            "text": "123456789987654321"
        },
        {
            "name": "uvwx",
            "text": "a"
        },
    ]
    user_names = [item['name'] for item in sample_data]
    scores_dict = {item["name"]:len(item["text"])/2.0 for item in sample_data}
    expected_halloffame = sorted(user_names, key=scores_dict.get, reverse=True)[:5]

    #print 'scores_dict- ', scores_dict
    #print 'expected_halloffame- ', expected_halloffame

    # submit data
    for item in sample_data:
        client.play(item)

    # retrieve halloffame data
    recieved_halloffame = [item['name'] for item in client.hall_of_fame()['data']]

    #print 'recieved_halloffame- ', recieved_halloffame
    if recieved_halloffame == expected_halloffame:
        print 'PASSED!'
    else:
        print 'FAILED!'

def test_threadsafety_for_play():
    '''Tests if score is consistent if multiple clients
    hit the server at the same time'''

    print '\nTesting threadsafety- ',
    # reset data on redis database for testing
    clear_data()

    # prepare sample data
    # make sure all text are palindrome for test case to work
    sample_data =  [
        {
            "name": "abcd",
            "text": "abcddcba"
        },
        {
            "name": "efgh",
            "text": "abcddcba"
        },
        {
            "name": "ijkl",
            "text": "abcdeffedcba"
        },
        {
            "name": "mnop",
            "text": "abcddcba"
        },
    ]
    counts = [50, 100, 200, 500]
    user_names = [item['name'] for item in sample_data]
    scores_dict = {item["name"]:len(item["text"])/2.0 for item in sample_data}
    expected_scores = [score for play, score in scores_dict.items()]

    data = []
    for i in range(4):
        for count in range(counts[i]):
            data.append(sample_data[i])

        # update expected scores list
        expected_scores[i] = expected_scores[i]*counts[i]

    random.shuffle(data)

    # Make the Pool of workers
    no_of_workers = 4
    pool = ThreadPool(no_of_workers)

    start_time = time.time()
    # Open the urls in their own workers
    # and return the results
    # print 'Initiating ', no_of_workers,' threads to hit the server ', sum(counts), ' times...'
    results = pool.map(client.play, data)

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()

    #print 'user_names- ', user_names
    #print 'counts- ', counts
    #print 'scores- ', scores
    #print 'expected_scores- ', expected_scores
    received_scores = [float(client.get_user(user)['data']["score"]) for user in user_names]

    #print 'received_scores- ', received_scores

    if received_scores == expected_scores:
        print 'PASSED!'
    else:
        print 'FAILED!'

if __name__ == '__main__':

    start_time = time.time()
    test_threadsafety_for_play()
    test_halloffame()
    test_play()
    test_get_user()
    test_get_all()
    print '\nTook ', round((time.time() - start_time), 3), ' seconds\n'
    clear_data()

