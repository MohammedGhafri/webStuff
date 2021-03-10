import socket,sys
from thread import *

def main():
    global listen_port, buffer_size, max_conn
    try:
        listen_port = int(raw_input("Enter a Listening port:"))
    except KeyboardInterrupt:
        sys.exit(0)
    max_conn = 5
    buffer_size = 8192

    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(('',listen_port))
        s.listen(max_conn)
        print("[*] Initializing socket... Done.")
        print("[*] Socket binded successfully...")
    except Exception as e:
        print(e)
        sys.exit(2)

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            start_new_thread(conn_string, (conn,data,addr))
        except KeyboardInterrupt:
            s.close()
            print("\n[*] Shutting down...")
            sys.exit(1)

    s.close()

def conn_string(conn,data,addr):
    print("Conn_string",conn,data,addr)
    try:
        first_line = data.split("\n")[0]
        url = first_line(" ")[1]
        print(40)
        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else: temp = url[(http_pos + 3):1]
        print(45)
        port_pos = temp.find(":")
        
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        print(53)
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver_pos = temp[:webserver_pos]
        
        print(webserver)

        proxy_server(webserver, port, conn, addr)
    except Exception as e:
        print(e)

def proxy_server(webserver, port, conn, addr):
    print("Proxy_server")
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((webserver,port))
        s.send(data)

        while True:
            reply = s.recv(buffer_size)

            if len(reply) > 0:
                conn.send(reply)

                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "{}.3s".fornat(dar)
                print("[*] Request done: {} => {} <= {}".format(addr[0], dar, webserver))
            
            else:
                break
        s.close()
        conn.close()

    except socket.error as e:
        s.close()
        conn.close()
        sys.exit(1)




if __name__ =="__main__":
    main()
