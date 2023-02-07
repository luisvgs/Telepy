import socket, threading, json
s = socket.socket()
host = "localhost"
port = 5000
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(5)
client_sockets = []

def handle_client(conn):
	while True:
		try:
			data = json.loads(conn.recv(512))
			msg_type = data["msg_type"]
			if msg_type == "broadcast":
				template = {}
				template["msg_type"] = "broadcast"
				template["msg"] = data["msg"]
				template["from"] = data["from"]
				for i in client_sockets:
					try:
						i.send(json.dump(template))
					except Exception as error:
						print("Ha ocurrido un error: ", error)
		except:
			pass
print "Waiting for a connection..."

while True:
	conn, addr = s.accept()
	client_sockets.append(conn)
	conn.send("Saludos")
	print "Connection from ", addr[0], "on port", addr[1]
	threading.Thread(target = handle_client, args = (conn,)).start()
