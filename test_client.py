from multiprocessing.dummy import Pool as ThreadPool
import client
import time
import random
import main

def clear_data():
    '''Deletes records in redis db'''
    # TBD - Use separate db for testing
    main.delete_data()

def test_get_user():
    '''Tests if a user's score persists & is retrievable'''
    pass

def test_play():
    '''Tests if a user's score is incremented properly'''
    pass

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
    print '\nTook ', round((time.time() - start_time), 3), ' seconds\n'
    clear_data()

