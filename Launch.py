import os
import time
import multiprocessing


thisFolder = os.path.dirname(os.path.realpath(__file__))
serverApp = os.path.join(thisFolder, 'FlaskDiarySvr.py')
clientApp = os.path.join(thisFolder, 'cUrlClient.py')


def startServer():
    print('Server')
    os.system(serverApp)

def startClient():
    print('Client')
    os.system(clientApp)


if __name__ == '__main__':
    multiprocessing.Process(target=startServer).start()
    time.sleep(5)
    print('\r\n\r\n')
    multiprocessing.Process(target=startClient).start()
