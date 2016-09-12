from multiprocessing.dummy import Pool as ThreadPool
import client
import time
import random
import main

def test_get_user():
    '''Tests if a user's score persists & is retrievable'''
    pass

def test_play():
    '''Tests if a user's score is incremented properly'''
    pass

def test_halloffame():
    '''Tests if halloffame correctly returns top5 users'''
    pass

def test_threadsafety_for_play():
    '''Tests if score is consistent if multiple clients
    hit the server at the same time'''

    print '\nTesting Threadsafety'

    # reset data on redis database for testing
    main.reset_data()

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

    user_names = [item['name'] for item in sample_data]
    counts = [50, 100, 200, 500]
    scores = [len(item["text"])/2.0 for item in sample_data]

    expected_scores = [count*score for count, score in zip(counts, scores)]

    data = []
    for i in range(4):
        for count in range(counts[i]):
            data.append(sample_data[i])
    random.shuffle(data)

    # Make the Pool of workers
    no_of_workers = 4
    pool = ThreadPool(no_of_workers)

    start_time = time.time()
    # Open the urls in their own workers
    # and return the results
    print '\nInitiating ', no_of_workers,' threads to hit the server ', sum(counts), ' times...'
    results = pool.map(client.play, data)

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()
    end_time = time.time()

    print '\nTook- ', round((end_time - start_time),3), ' seconds\n'
    #print 'user_names- ', user_names
    #print 'counts- ', counts
    #print 'scores- ', scores
    #print 'expected_scores- ', expected_scores
    received_scores = [float(client.get_user(user)['data']["score"]) for user in user_names]

    #print 'received_scores- ', received_scores

    if received_scores == expected_scores:
        print 'TEST SUCCESSFUL- Data is consistent!\n'
    else:
        print 'TEST FAILED- Data is inconsistent!\n'

if __name__ == '__main__':
    test_threadsafety_for_play()


