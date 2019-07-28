import socket
import select
import errno
import sys

headerLength = 10

ip = '192.168.1.10'
port = 1237

my_username = input("Username :")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip,port))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{headerLength}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
	message = input(f"{my_username} > ")

	if message != '':
		message = message.encode("utf-8")
		message_header = f"{len(message):<{headerLength}}".encode("utf-8")
		client_socket.send(message_header + message)
	else:
		sys.stdout.write("\033[F")

	try:
		while True:
			#receive things
			username_header = client_socket.recv(headerLength)
			if not len(username_header):
				print("Connection closed by the server")
				sys.exit()
			username_length = int(username_header.decode("utf-8").strip())
			username = client_socket.recv(username_length).decode("utf-8")

			message_header = client_socket.recv(headerLength)
			message_length = int(message_header.decode("utf-8").strip())
			message = client_socket.recv(message_length).decode("utf-8")

			print(f"{username} > {message}")

	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error', str(e))
			sys.exit()
		continue

	except Exception as e:
		print(str(e))
		sys.exit()













