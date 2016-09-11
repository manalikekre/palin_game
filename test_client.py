from multiprocessing.dummy import Pool as ThreadPool
import client
import time
import random

NO_OF_WORKERS = 4

if __name__ == '__main__':
    no_of_workers = NO_OF_WORKERS
    # Make the Pool of workers
    pool = ThreadPool(no_of_workers)

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
    data = []
    counts = [50, 100, 200, 500]

    for i in range(4):
        for count in range(counts[i]):
            data.append(sample_data[i])

    user_names = [item['name'] for item in data]
    # randomize the data
    random.shuffle(data)
    random.shuffle(user_names)

    start_time = time.time()
    # Open the urls in their own workers
    # and return the results
    #results = pool.map(client.play, data)
    results = pool.map(client.get_user, user_names)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()
    end_time = time.time()

    print '\nworkers- ', no_of_workers
    print '\ntook- ', (end_time - start_time), ' seconds\n'
