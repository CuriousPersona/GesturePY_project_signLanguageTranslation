from SettingsUI import SettingsScr_widgets
from SettingsUI import ToggleSwitch

# For working with multiple screens of app
from kivy.uix.screenmanager import Screen, ScreenManager

# For working with Messaging part & Emoji picker
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty, StringProperty
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.animation import Animation

# For working with OpenCV camera 
import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.label import MDLabel

import mediapipe as mp


class MainScr_widgets(Screen):
    
    messages = ListProperty()
    
    emoj = ["emoticon-angry", "emoticon-confused", "emoticon-cry", "emoticon-dead", "emoticon-devil", "emoticon-neutral", "emoticon-happy", "emoticon-lol", 
            "emoticon-wink"]
    
    menu_items = [{ "viewclass": "Emojis", "height": dp(63), "left_icon": emoj[0], "center_icon": emoj[1], "right_icon": emoj[2], 
                       "on_release": lambda x: app.callback(x)}, 
                  { "viewclass": "Emojis", "height": dp(63), "left_icon": emoj[3], "center_icon": emoj[4], "right_icon": emoj[5], 
                       "on_release": lambda x: app.callback(x) }, 
                  { "viewclass": "Emojis", "height": dp(63), "left_icon": emoj[6], "center_icon": emoj[7], "right_icon": emoj[8], 
                       "on_release": lambda x: app.callback(x) }]

            
    def camera_support(self, togbtnone, togbtntwo): 
        
        # Uses the webcam and captures video frame from real time
        self.webcam = cv2.VideoCapture(0+cv2.CAP_DSHOW)
        
        if togbtnone.active == True and togbtntwo.active == False:
            if self.ids["img"].texture is not None:
                self.ids["img"].texture = None
                self.webcam.release()
                self.webcam = cv2.VideoCapture(0+cv2.CAP_DSHOW)

            Clock.schedule_interval(self.load_video, 1.0/30.0)
            
        elif togbtnone.active == True and togbtntwo.active == True:
            self.ids["img"].texture = None
            self.webcam.release()   
            self.camera_support_detection(togbtnone, togbtntwo)

            
        elif togbtnone.active == False and togbtntwo.active == False:
            self.ids["img"].texture = None
            self.webcam.release()

    def camera_support_detection(self, togbtnone, togbtntwo):          
        self.webcam = cv2.VideoCapture(0+cv2.CAP_DSHOW)
        Clock.schedule_interval(self.load_video_detectn, 1.0/30.0)
        
        
    def load_video(self, *args):   
        buffer = None
        texture = None
        working, frame = self.webcam.read()
        if working:
            buffer = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt = "bgr")
            texture.blit_buffer(buffer, colorfmt = "bgr", bufferfmt = "ubyte")
            # Main line that shows output inside "Image" widget
            self.ids["img"].texture = texture
            
    
    def load_video_detectn(self, *args):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands
        
        buffer = None
        texture = None 
        working, frame = self.webcam.read()
        with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            
            if working:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame.flags.writeable = False
                results = hands.process(frame)
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, 
                                                  mp_drawing_styles.get_default_hand_landmarks_style(), 
                                                  mp_drawing_styles.get_default_hand_connections_style())
                buffer = cv2.flip(frame, 0).tostring()
                texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt = "bgr")
                texture.blit_buffer(buffer, colorfmt = "bgr", bufferfmt = "ubyte")
                # Main line that shows output inside "Image" widget
                self.ids["img"].texture = texture
   
 
    def addMsg(self, text, side):
        self.messages.append( { "text": text, "side": side, "text_size": (None, None), } )

###########################################################################        
    #def updateMsgSize(self, mes_id, texture_S, max_width):    
        
        #if max_width == 0:
            #return
        
        #one_line = dp(50)

        #if texture_S[0] >= max_width * 2 / 3:
            #self.messages[mes_id] = { **self.messages[mes_id], "text_size": (max_width * 2 / 3, None), }
        
        #elif texture_S[0] < max_width * 2 / 3 and texture_S[1] > one_line:
            #self.messages[mes_id] = { **self.messages[mes_id], "text_size": (max_width * 2 / 3, None), "_size": texture_S, }
            
        #else:
            #self.messages[mes_id] = { **self.messages[mes_id], "_size": texture_S, } SS
            
############################################################################            
    
    def sendMsg(self, textinput): # From MainGUI.kv file, the TextInput object is passed here      
        if textinput.text == "":
            self.textinputFocus(textinput)
            self.scrollBottom()
            return
        
        else:
            Text = textinput.text
            textinput.text = ""
            self.textinputFocus(textinput)
            self.addMsg(Text, 'right')
            self.scrollBottom()
            
    
    @staticmethod
    def textinputFocus(textinput):
        textinput.focus = True
        
        
    def scrollBottom(self):   
        rv = self.ids["RV"]
        box = self.ids["Box"]    
        if rv.height < box.height:
            Animation.cancel_all(rv, 'scroll_y')
            Animation(scroll_y=0, t='out_quad', d=0.5).start(rv)
            
            
class ScrManager(ScreenManager):
    pass


class Emojis(MDBoxLayout):
    left_icon = StringProperty()
    center_icon = StringProperty()
    right_icon = StringProperty()
    
            
class MenuHeader(MDBoxLayout):
    pass           


class OffImg(Image):
    pass   



    
    