#Kivy imports
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import Config
Config.set("graphics","multisamples","0")
from kivy.utils import get_color_from_hex
#Python modules: Sockets and threading for Connection purposes.
import socket, threading
global s
#configuracion de  sockets y puertos de escucha.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
global name
name = "luis"



#GUI del chat.
Builder.load_string("""
<Chat>:
    GridLayout:
        rows: 2

        GridLayout:
            cols: 1
            rows: 0
            ScrollView:
                size: self.size
                do_scroll_x: False
                Label:
                    id: msg_log 
                    text_size: self.width,None
                    size_hint_y: None
                    height: self.texture_size[1]
                    font_size: root.height / 20
        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 15

        TextInput:
            id:message
            hint_text:"Write a message..."
            multiline:False
            on_text_validate:root.send_message(message.text)
""")

class Chat(Screen):
    global s
    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)
        #Hereda configuraciones de Chat?
        self.msg_log = self.ids["msg_log"] 
    def on_enter(self):
        """ Al presionar enter.."""
     
#Se ejecuta conexion recibiendo el host y el puerto.            
        s.connect((host,port)) 
        #Handshake. Se crea buffer de 512 bytes
        welcome = s.recv(512) 
        #Conversion a strings de bytes recibidos (Parsing de mensaje)
        self.msg_log.text += str(welcome + "\n")    
        threading.Thread(target=self.handle_messages).start()
     
    def send_message(self,to_send_out):
        try:
            s.send(name + " : "+to_send_out)
        except Exception as e:
            print("An error has ocurred:", e)

    def handle_messages(self):
        while True:
            try:
                data = s.recv(1024)
                self.msg_log.text+=data+"\n"
            except Exception as e:
                print(e)
class Talkie(App):
    def build(self):
        return sm

sm = ScreenManager()
sm.add_widget(Chat(name="main_screen"))
if __name__ == "__main__":
    Talkie().run()
