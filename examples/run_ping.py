from pymicro.services import RemoteService
from pymicro.protocols.http import HTTP

if __name__ == '__main__':
    service = RemoteService(
        protocol=HTTP(host='localhost', port=5000)
    )
    print(service.ping(delay=1))
