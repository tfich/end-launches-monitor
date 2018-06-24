import time, sys

def log(message=""):
    timestring = "[{}] ".format(time.strftime("%H:%M:%S"))

    finalString = "{}{}\n".format(timestring, str(message))

    sys.stdout.write(finalString)
    sys.stdout.flush()
