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