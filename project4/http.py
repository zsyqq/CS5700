import socket
import sys

from tcp import TCPSocket


class HTTPPacket():
    def __init__(self, _url):
        def get_hostname(my_url):
            # e.g. url: http://cs5700.ccs.neu.edu/fakebook
            # hostname: cs5700.ccs.neu.edu
            hostname = my_url.split('/')[2]
            #print '[DEBUG]Host name: %s' % hostname
            return hostname

        def get_relative_path(my_url, hostname):
            start_position = my_url.find(hostname) + len(hostname)
            #print '[DEBUG] Path:' + url[start_position:]
            return my_url[start_position:]

        self.hostname = get_hostname(_url)
        self.path = get_relative_path(_url, self.hostname)

    def build_request(self):
        request = "GET " + self.path + \
                  " HTTP/1.1\r\n" + \
                  "Host: " + self.hostname + \
                  "\r\n\r\n"

        #print '[DEBUG]HTTP Request:\n' + request
        return request


class HTTPSocket:
    def __init__(self):
        self.sock = TCPSocket()

    def download(self, _url):
        def get_filename(my_url):
            # e.g. url: http://cs5700.ccs.neu.edu/fakebook
            # filename: index.html
            if my_url.endswith('/'):
                name = 'index.html'
            else:
                name = my_url.split('/')[-1]
                #print '[DEBUG]: File name' + filename
            return name

        filename = get_filename(_url)
        f = open(filename, 'wb+')
        packet = HTTPPacket(_url)
        self.send(packet)
        data = self.recv()
        f.write(data)
        f.close()

    def send(self, packet):
        try:
            request = packet.build_request()
            self.sock.send(request)
        except socket.error:
            #Send failed
            sys.exit('Send failed')

    def recv(self):
        """
        Receive data and write it to a file
        """

        def parse_header(response):
            index = response.find('\r\n\r\n') + 4
            header = response[:index]
            return header[9:12], index

        data = self.sock.recv()
        if data.startswith('HTTP/1.1'):
            status, pos = parse_header(data)
            if status != 200:
                sys.exit('The HTTP Response has an  abnormal status code.')
            pass
        else:
            pass
        return data

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Illegal Arguments.')
    url = sys.argv[1]
    sock = HTTPSocket()
    sock.download(url)
