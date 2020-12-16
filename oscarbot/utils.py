import time

times = {'s':1, 'S':1, 'm':60, 'M':60, 'h':3600, 'H':3600, 'd':3600*24, 'D':3600*24, 'w':3600*24*7, 'W':3600*24*7}

def separate(*args):
    tr = " ".join(args[0])
    tr = tr.split(" ")
    if "-t" in tr:
        t = int(tr[tr.index("-t")+1][:-1]) * times[tr[tr.index("-t")+1][-1]]
    
    if "-t" not in tr:
        t = "indefinitely."
       
    if "-r" in tr:
        if "-t" in tr:
            if tr.index("-r") < tr.index("-t"):
                r = " ".join(tr[tr.index("-r")+1:tr.index("-t")])
            else:
                r = " ".join(tr[tr.index("-r")+1:])
        else:
            r = " ".join(tr[tr.index("-r")+1:])

    if "-r" not in tr:
        r = "no reason specified."

    return t, r

class Timer:
    elapsed_time = None

    def stop(self):
        Timer.elapsed_time = None

    def start(self, end):
        Timer.elapsed_time = 0
        while Timer.elapsed_time != None:
            time.sleep(1)
            Timer.elapsed_time += 1
            if Timer.elapsed_time == end:
                self.stop()
                