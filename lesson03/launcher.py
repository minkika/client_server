import subprocess

PROCESS = []


while True:
    ANSWER = input('')
    if ANSWER == 'q':
        break
    elif ANSWER == 's':
        PROCESS.append(subprocess.Popen('python3 server.py', shell=True))
        for i in range(3):
            PROCESS.append(subprocess.Popen('python3 client.py', shell=True))
    elif ANSWER == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
