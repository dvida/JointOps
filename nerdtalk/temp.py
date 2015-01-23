import sys
import threading
import time
import Queue

def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))

def foobar():
    input_queue = Queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    while True:

        if not input_queue.empty():
            print "\ninput:", input_queue.get()

foobar()