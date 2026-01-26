# without Threading
 
import time

def task():
    time.sleep(2)
    print("Task done")

task()
print("Main done")
 

#with Threading
import threading
import time

def task():
    time.sleep(2)
    print("Task done")

thread = threading.Thread(target=task)
thread.start()

print("Main done")
 

# with Threading and join
import threading
import time

def task():
    time.sleep(2)
    print("Task done")

t = threading.Thread(target=task)
t.start()
t.join()

print("Main done")
 

#Multiple Threads, passing arguments to threads
 
import threading

def greet(name, delay):
    import time
    time.sleep(delay)
    print(f"Hello {name}")

t1 = threading.Thread(target=greet, args=("Alice", 1))
t2 = threading.Thread(target=greet, args=("Bob", 2))

t1.start()
t2.start()

t1.join()
t2.join()
 

#Using Thread subclass
 
import threading
import time
class MyThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        time.sleep(self.delay)
        print(f"Hello {self.name}")
t1 = MyThread("Alice", 1)
t2 = MyThread("Bob", 5)
t1.start()
t2.start()
t1.join()
t2.join()
 

#Using daemon threads
 
import threading
import time
def background_task():
    while True:
        print("Background task running...")
        time.sleep(1)
t = threading.Thread(target=background_task, daemon=True)
t.start()
time.sleep(3)
print("Main done")
 

# Shared Data & Race Conditions, Using Locks
import time
import threading
counter = 0
lock = threading.Lock()
def increment():
    global counter
    for _ in range(100):
        with lock:
            counter += 1
            time.sleep(0)
            print(counter, end = " ")
t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start()
t2.start()
t1.join()
t2.join()
print(f"Final counter value: {counter}")


# RLock (Reentrant Lock)
 
import threading
import time
lock = threading.RLock()
i = 0
def outer():
    with lock:
        inner()

def inner():
    global i
    with lock:
        for _ in range(100):
            tem = i + 1
            time.sleep(0)
            i += 1
            print(i, end = " ")

t1 = threading.Thread(target=outer)
# t2 = threading.Thread(target=outer)
# t3 = threading.Thread(target=outer)
t1.start()
# t2.start()
# t3.start()
t1.join()
# t2.join()
# t3.join()

print(f"Main done {i}")
 

# Thread-safe Communication — Queue
import threading
import queue
import time

STOP = object()

def producer(q, count):
    for i in range(count):
        print(f"Producing {i}", end=" ")
        q.put(i)
        time.sleep(1)
    q.put(STOP)   # signal this producer is done

def consumer(q, producers):
    finished = 0
    while True:
        item = q.get()
        if item is STOP:
            finished += 1
            if finished == producers:
                q.task_done()
                break
        else:
            print(f"Consuming {item}", end=" ")
            q.task_done()

q = queue.Queue()

NUM_PRODUCERS = 8
ITEMS_PER_PRODUCER = 5

producers = [
    threading.Thread(target=producer, args=(q, ITEMS_PER_PRODUCER))
    for _ in range(NUM_PRODUCERS)
]

consumer_thread = threading.Thread(
    target=consumer,
    args=(q, NUM_PRODUCERS)
)

for t in producers:
    t.start()

consumer_thread.start()

for t in producers:
    t.join()

consumer_thread.join()


#Thread-local Data
import threading
thread_local_data = threading.local()
def worker(name):
    thread_local_data.name = name
    print(f"Hello {thread_local_data.name} from thread {threading.current_thread().name}")
t1 = threading.Thread(target=worker, args=("Alice",))
t2 = threading.Thread(target=worker, args=("Bob",))
t1.start()
t2.start()
t1.join()
t2.join()
 

#Using Condition Variables
import threading
condition = threading.Condition()
shared_resource = []
def producer():
    global shared_resource
    for i in range(5):
        with condition:
            shared_resource.append(i)
            print(f"Produced {i}")
            condition.notify()
def consumer():
    global shared_resource
    for _ in range(5):
        with condition:
            while not shared_resource:
                condition.wait()
            item = shared_resource.pop(0)
            print(f"Consumed {item}")
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
t1.join()
t2.join()
 

#Creating Multiple Threads in a Loop
 
import threading
import time
def task(id, delay):
    time.sleep(delay)
    print(f"Task {id} done after {delay} seconds")
threads = []
for i in range(5):
    t = threading.Thread(target=task, args=(i, i))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
print("All tasks completed")
 