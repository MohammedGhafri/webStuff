# import socket
# import select
# import time
# import sys

# # Changing the buffer_size and delay, you can improve the speed and bandwidth.
# # But when buffer get to high or delay go too down, you can broke things
# buffer_size = 4096
# delay = 0.0001
# forward_to = ('ncbi.nlm.nih.gov', 80)


# class Forward:
#     def __init__(self):
#         self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     def start(self, host, port):
#         try:
#             self.forward.connect((host, port))
#             return self.forward
#         except Exception as e:
#             print(e)
#             return False


# class TheServer:
#     input_list = []
#     channel = {}

#     def __init__(self, host, port):
#         self.s = None
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.server.bind((host, port))
#         self.server.listen(200)

#     def main_loop(self):
#         self.input_list.append(self.server)
#         while 1:
#             time.sleep(delay)
#             ss = select.select
#             inputready, outputready, exceptready = ss(self.input_list, [], [])
#             for self.s in inputready:
#                 if self.s == self.server:
#                     self.on_accept()
#                     break

#                 self.data = self.s.recv(buffer_size)
#                 if len(self.data) == 0:
#                     self.on_close()
#                     break
#                 else:
#                     self.on_recv()

#     def on_accept(self):
#         forward = Forward().start(forward_to[0], forward_to[1])
#         clientsock, clientaddr = self.server.accept()
#         if forward:
#             print(clientaddr, "has connected")
#             self.input_list.append(clientsock)
#             self.input_list.append(forward)
#             self.channel[clientsock] = forward
#             self.channel[forward] = clientsock
#         else:
#             print("Can't establish connection with remote server.", end=' ')
#             print("Closing connection with client side", clientaddr)
#             clientsock.close()

#     def on_close(self):
#         print(self.s.getpeername(), "has disconnected")
#         # remove objects from input_list
#         self.input_list.remove(self.s)
#         self.input_list.remove(self.channel[self.s])
#         out = self.channel[self.s]
#         # close the connection with client
#         self.channel[out].close()  # equivalent to do self.s.close()
#         # close the connection with remote server
#         self.channel[self.s].close()
#         # delete both objects from channel dict
#         del self.channel[out]
#         del self.channel[self.s]

#     def on_recv(self):
#         data = self.data
#         # here we can parse and/or modify the data before send forward
#         print(data)
#         self.channel[self.s].send(data)


# if __name__ == '__main__':
#     server = TheServer('localhost', 33333)
#     try:
#         server.main_loop()
#     except KeyboardInterrupt:
#         print("Ctrl C - Stopping server")
#         sys.exit(1)





##############################################################################################################################################


import os,sys,thread,socket

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = False           # set to True to see the debug msgs

#********* MAIN PROGRAM ***************
def main():

  # check the length of command running
  if (len(sys.argv) < 2):
    print "usage: proxy <port>"
    return sys.stdout

  # host and port info.
  host = ''               # blank for localhost
  port = int(sys.argv[1]) # port from argument

  try:
    # create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # associate the socket to host and port
    s.bind((host, port))

    # listenning
    s.listen(BACKLOG)

  except socket.error, (value, message):
    if s:
        s.close()
    print "Could not open socket:", message
    sys.exit(1)

  # get the connection from client
  while 1:
    conn, client_addr = s.accept()

    # create a thread to handle request
    thread.start_new_thread(proxy_thread, (conn, client_addr))

  s.close()



def proxy_thread(conn, client_addr):

  # get the request from browser
  request = conn.recv(MAX_DATA_RECV)

  # parse the first line
  first_line = request.split('n')[0]

  # get url
  url = first_line.split(' ')[1]

  if (DEBUG):
    print first_line
    print
    print "URL:", url
    print

  # find the webserver and port
  http_pos = url.find("://")          # find pos of ://
  if (http_pos==-1):
    temp = url
  else:
    temp = url[(http_pos+3):]       # get the rest of url

  port_pos = temp.find(":")           # find the port pos (if any)

  # find end of web server
  webserver_pos = temp.find("/")
  if webserver_pos == -1:
    webserver_pos = len(temp)

  webserver = ""
  port = -1
  if (port_pos==-1 or webserver_pos < port_pos):      # default port
    port = 80
    webserver = temp[:webserver_pos]
  else:       # specific port
    port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
    webserver = temp[:port_pos]

  print "Connect to:", webserver, port

  try:
    # create a socket to connect to the web server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((webserver, port))
    s.send(request)         # send request to webserver

    while 1:
      # receive data from web server
      data = s.recv(MAX_DATA_RECV)

      if (len(data) > 0):
        # send to browser
        conn.send(data)
      else:
        break
    s.close()
    conn.close()
  except socket.error, (value, message):
    if s:
      s.close()
    if conn:
      conn.close()
    print "Runtime Error:", message
    sys.exit(1)

if __name__ == '__main__':
  main()