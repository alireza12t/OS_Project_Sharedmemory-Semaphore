 import threading


class ServiceAccess:
    a: list = None
    def __init__(self):
        self.a = []

    def acquire(self):
        lock = threading.Lock()
        lock.acquire()
        self.a.append(lock)

    def release(self):
        lock = self.a.pop()
        lock.release()


resourceAc = threading.Semaphore()
readCountAc = threading.Semaphore()
serviceAc = ServiceAccess()

numberOfReaders = 0
shared_resource = 0




def write(i):
    global shared_resource

    serviceAc.acquire()
    with resourceAc:
        shared_resource = threading.current_thread().ident
        print("Writer " + str(i+1) + " => Writes  " + str(shared_resource))
        serviceAc.release()



def read(i):
    global numberOfReaders
    global shared_resource

    serviceAc.acquire()
    with readCountAc:

        if numberOfReaders == 1:
            resourceAc.acquire()
        numberOfReaders += 1
        serviceAc.release()
    print("Reader " + str(i+1) + " => Reads  " + str(shared_resource))

    with readCountAc:
        numberOfReaders -= 1
        if numberOfReaders == 0:
            resourceAc.release()

threads = []

for func in [write, read]:
    for i in range(4):
        threads.append(threading.Thread(target=func,args=(i,)))
        # threads[-1].start()


for thread in threads:
    thread.start()

for thread in threads:
    thread.join()



