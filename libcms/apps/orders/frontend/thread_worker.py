# -*- encoding: utf-8 -*-

import Queue
import threading
import urllib2


class ThreadResult(object):
    def __init__(self, value):
        self.value = value


# Threads form a thread-pool waiting for compute requests in the request_queue
class ComputeThread(threading.Thread):
    def __init__(self, func, arg, request_queue):
        threading.Thread.__init__(self)
        self.request_queue = request_queue
        self.func = func
        self.arg = arg

    def run(self):
        while 1:
            # block waiting for something in the queue
            req = self.request_queue.get()
            if req is None:
                # Nothing more to process; quit
                break
            value, response_queue = req
            try:
                result = self.func(self.arg)
                tr = ThreadResult(result)
                response_queue.put(tr)
            except BaseException as e:
                response_queue.put(e)


class ThreadWorker(object):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __threaded_func(self, request_queue, values):
        sum = ''
        response_queue = Queue.Queue()
        for value in values:
            request_queue.put((value, response_queue))
            # accumulate results; the response order will not be the same as the input!
        # The "_" is a convention meaning "I don't care about the actual variable name."
        results = []
        for value in values:
            results.append(response_queue.get())
        return results

    def do(self):
        request_queue = Queue.Queue()

        # Initialize the thread pool with three compute threads
        for arg in self.args:
            ComputeThread(self.func, arg, request_queue).start()

        results = self.__threaded_func(request_queue, self.args)

        #    # Send shutdown messages to all the threads in the pool
        for i in self.args:
            request_queue.put(None)

        return results


        # def compute(host):
        #    url = urllib2.urlopen(host, timeout=2)
        #    result = url.read()
        #    return result
        #
        # hosts = ["http://yahoo.com:8080", "http://google.com", "http://amazon.com",
        #         "http://ibm.com", "http://apple.com"]
        #
        # from time import time as t
        # if __name__ == "__main__":
        #    s = t()
        #    print ThreadWorker(compute, hosts).do()
        #    print 'time:', t() -s
