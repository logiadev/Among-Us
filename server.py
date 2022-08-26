import os
os.system("pip3 install requests")
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import flask
from simple_websocket_server import WebSocketServer, WebSocket
import random
import json

class Turbowap(WebSocket):        
    def handle(self):
        global client_players
        global clients
        global rooms
        print(self.data)
        if "TO_HOST" in str(self.data):
            request_id = str(self.data).split(".")[1].split("?")[0]
            
            if "playerid=null" in str(self.data):
                print(request_id)
                player_id = str(random.randint(0,1000000))
                client_players[self] = player_id
                
                self.send_message(json.dumps({"method":"set","project_id":"701819238","name":"☁ TO_HOST","value":player_id+"?id="+request_id}))
            
            if "?newroom" in str(self.data):

                if len(list(rooms.keys())) > 30:
                    self.send_message(json.dumps({"method":"set","project_id":"701819238","name":"☁ TO_HOST","value":"!full"+"?id="+request_id}))
                    return
                    
                room_id = str(random.randint(0,1000000))
                hostname = str(self.data).split("hostname=")[1].split("&")[0]
                playerid = str(self.data).split("playerid=")[1].split("&")[0]
        
                rooms[room_id] = {"hostname":hostname,"playerdata":{playerid:""},"status":1,"private":False}
                self.send_message(json.dumps({"method":"set","project_id":"701819238","name":"☁ TO_HOST","value":room_id+"?id="+request_id}))
        else:
            try:
                playerid = str(self.data).split("playerid=")[1].split("&")[0]
                roomid = str(self.data).split("roomid=")[1].split("&")[0]
                hostname = str(self.data).split("hostname=")[1].split("&")[0]

                rooms[roomid]["hostname"] = hostname
                rooms[roomid]["playerdata"][playerid] = str(self.data).split('value":"')[0].split('"')[0]
                print(rooms[roomid]["playerdata"][playerid])
            except Exception as e:
                print(e)
                
    def connected(self):
        global client_players
        global clients        
        print(self.address, 'connected')
        clients.append(self)

    def handle_close(self):
        global client_players
        global clients
        clients.remove(self)
        client_players.pop(self)
        print(self.address, 'closed')


clients = []
client_players = {}
rooms = {}

server = WebSocketServer('', 8000, Turbowap)
server.serve_forever()

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://among-us-online.logiadev.repl.co</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Server is online.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

server_line.go = "Get main.server = = connect to wss://among-us-online.logiadev.repl.co"
connecting = "Connected to server"
print(connecting)
