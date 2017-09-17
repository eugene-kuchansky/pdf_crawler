import sys
from urllib2 import urlopen, Request, URLError#, exceptions
import Queue as queue
import threading
from collections import namedtuple


HEADER_USER_AGENT = ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
THREADS_NUM = 50

ResponseResult = namedtuple('ResponseResult', 'url is_alive')


def process_page(url):
    req = Request(url)
    req.add_header(*HEADER_USER_AGENT)
    try:
        response = urlopen(req)
        is_alive = False
        if response.getcode() < 400:
            is_alive = True
        return ResponseResult(url=url, is_alive=is_alive)
    except URLError as e:
        return ResponseResult(url=url, is_alive=False)


class ThreadUrl(threading.Thread):
    def __init__(self, tasks, results):
        threading.Thread.__init__(self)
        self.tasks = tasks
        self.results = results

    def run(self):
        while True:
            url = self.tasks.get()
            if url is None:
                # got stop signal
                break
            self.results.put(process_page(url))
            self.tasks.task_done()


def validate(urls):
    # results - url and it's status
    processed_urls = {}

    # queues to exchange data with threads
    task_queue = queue.Queue()
    result_queue = queue.Queue()

    # all IO is performed by threads
    # it's faster than process links one by one
    for i in range(THREADS_NUM):
        worker = ThreadUrl(task_queue, result_queue)
        worker.setDaemon(True)
        worker.start()

    # put hte first url
    for url in urls:
        task_queue.put(url)

    # and wait to be completed
    task_queue.join()

    while not result_queue.empty():
        result = result_queue.get()
        processed_urls[result.url] = result.is_alive

    # send stop signals to all threads
    for i in range(THREADS_NUM):
        task_queue.put(None)
    
    return processed_urls
