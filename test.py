import os
from sys import argv

def main(route):
    print('curl -vX POST http://35.227.195.251/{} -d @{}.json'.format(route, route))
    os.system('curl -vX POST http://35.227.195.251/{} -d @{}.json'.format(route, route))
    print('')
    if scale == 'scale':
        while True:
            os.system('curl -vX POST http://35.227.195.251/{} -d @{}.json'.format(route, route))

if __name__ == '__main__':
    route = str(argv[1])
    if len(argv) == 3:
        scale = str(argv[2])
    else:
        scale = None
    main(route)
