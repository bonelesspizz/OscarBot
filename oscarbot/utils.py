import time

times = {'s':1, 'S':1, 'm':60, 'M':60, 'h':3600, 'H':3600, 'd':3600*24, 'D':3600*24, 'w':3600*24*7, 'W':3600*24*7}

def separate(*args):
    # Used in the mute command for seperating the time and reason if they are inputted
    tr_string = " ".join(args[0])
    tr_string = tr_string.split(" ")
    if "-t" in tr_string:
        time = int(tr_string[tr_string.index("-t")+1][:-1]) * times[tr_string[tr_string.index("-t")+1][-1]]
    
    if "-t" not in tr_string:
        time = "indefinitely."
       
    if "-r" in tr_string:
        if "-t" in tr_string:
            if tr_string.index("-r") < tr_string.index("-t"):
                reason = " ".join(tr_string[tr_string.index("-r")+1:tr_string.index("-t")])
            else:
                reason = " ".join(tr_string[tr_string.index("-r")+1:])
        else:
            reason = " ".join(tr_string[tr_string.index("-r")+1:])

    if "-r" not in tr_string:
        reason = "no reason specified."

    return time, reason

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
                