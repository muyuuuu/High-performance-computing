import threading, time

balance = 0
lock = threading.Lock()

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    time.sleep(2)
    balance += n
    time.sleep(2)

def run_thread(n):
    lock.acquire()
    try:
        # 放心地改吧:
        change_it(n)
    finally:
        # 改完了一定要释放锁:
        lock.release()

t1 = threading.Thread(target=run_thread, args=(1,))
t2 = threading.Thread(target=run_thread, args=(1,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)