#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust, 2021 Meilin Lyu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

# Citation:
# stolen from Adam Smith https://stackoverflow.com/users/3058609/adam-smith
# From Stackoverflow
# https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3
# "result = urlencode(payload, quote_via=quote_plus)" I learnt how to use urlencode
# and used in line 44, 148, 156

# stolen from stwhite https://stackoverflow.com/users/415763/stwhite
# From Stackoverflow
# https://stackoverflow.com/questions/10115126/python-requests-close-http-connection
# "r = requests.post(url=url, data=body, headers={'Connection':'close'})" I learnt how to use "connection:close"
# and used in line 126, 164

# refer to https://docs.python.org/3/library/urllib.parse.html
# "urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)"
#  used in line 44, 60, 71
#  Example of http GET and POST Request Message is from 
#  https://www.tutorialspoint.com/http/http_requests.htm#:~:text=The%20GET%20method%20is%20used,other%20effect%20on%20the%20data. 

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        ''' This function is used to get host name and port
        from the url '''
        # default port
        port = 80
        parse_url = urlparse(url)
        host = parse_url.hostname
        # if url contains the port, then get the port
        if parse_url.port:
            port = parse_url.port
        return host,port
        
    def get_path(self,url):
        '''This function is used to get the path from url'''
        # default path
        path = "/"
        parse_url = urlparse(url)
        # if url contains the path, then get the path
        if parse_url.path:
            path = parse_url.path
        return path

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def get_code(self, data):
        # The code is obtained in the first line of header
        header = self.get_headers(data)
        code = int(header.split()[1])
        return code

    def get_headers(self,data):
        # get the header from data
        header = data.split('\r\n\r\n')[0]
        return header
        
    def get_body(self, data):
        # get body from data
        body = data.split('\r\n\r\n')[1]
        return body

    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')
   
    def GET(self, url, args=None):
        # get the host and port from url
        host,port = self.get_host_port(url)
        # get the path from url
        path = self.get_path(url)
        # connect to socket
        self.connect(host,port)
        # format the payload
        payload = "GET " +path+ " HTTP/1.1\r\n"
        payload += "Host: " +host+ "\r\n"
        # to reduce running time
        payload += "Connection: close"+"\r\n\r\n"
        self.sendall(payload)
        # get the data
        full_data = self.recvall(self.socket)
        self.close()
        # get code from data received
        code = self.get_code(full_data)
        # get body from data received
        body = self.get_body(full_data)
        # print out the result for user
        print("url: ",url)
        print("code: ",code)
        print("port: ",port)
        print("body: ",body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # get the host and port from url
        host,port = self.get_host_port(url)
        # get the path from url
        path = self.get_path(url)
        # Initialize the content,content_length,content_type
        content = urlencode("")
        content_length = 0
        content_type = "application/x-www-form-urlencoded"
        # connent to socket
        self.connect(host,port)
        # if the content is not empty
        # get the content and content length
        if args:
            content = urlencode(args)
            content_length = len(content)
        # format the payload
        payload = "POST " +path+ " HTTP/1.1\r\n"
        payload += "Host: " +host+ "\r\n"
        payload += "Content-Type:" +content_type+ "\r\n"
        payload += "Content-Length: "+ str(content_length)+ "\r\n"
        # to reduce running time
        payload += "Connection: close"+"\r\n\r\n"
        # add the content to payload
        payload += content+ "\r\n\r\n"  
        self.sendall(payload)
        # get the data
        full_data = self.recvall(self.socket)
        self.close()
        code = self.get_code(full_data)
        body = self.get_body(full_data)
        print("url: ",url)
        print("code: ",code)
        print("port: ",port)
        print("body: ",body)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
