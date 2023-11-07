# Imports from MainUI.py
from MainUI import MainScr_widgets
from MainUI import ScrManager
from MainUI import Emojis
from MainUI import MenuHeader
from MainUI import OffImg

# Imports from SettingsUI.py
from SettingsUI import SettingsScr_widgets
from SettingsUI import ToggleSwitch

# For Emoji picker
from kivymd.uix.menu import MDDropdownMenu
# For pop-up box
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# Runs our application
from kivymd.app import MDApp
# Loads .kv files
from kivy.lang import Builder

Builder.load_file("D:/Adwait/Adw_apps/miniCONDAPython/OpenCV course (yml file)/Gesture_software/MainApp/MainUI.kv")
Builder.load_file("D:/Adwait/Adw_apps/miniCONDAPython/OpenCV course (yml file)/Gesture_software/MainApp/SettingsUI.kv")

class KivyMD(MDApp):

    def build(self):
        # Adding "main" screen and "settings" screen to Screen manager
        self.WindowManage = ScrManager() 
        self.WindowManage.add_widget(MainScr_widgets(name = "main"))
        self.WindowManage.add_widget(SettingsScr_widgets(name = "settings"))
        
        # Emoji picker code
        self.menu = MDDropdownMenu(header_cls = MenuHeader(), 
                                   caller = self.WindowManage.get_screen("main").ids.iconbutton, 
                                   items = self.WindowManage.get_screen("main").menu_items, 
                                   width_mult = 2.9)

        self.offimg = OffImg()
        self.WindowManage.get_screen("main").ids["Float"].add_widget(self.offimg)
        return self.WindowManage
    

    def Change_imgs(self, togglebtnOne, togglebtnTwo):
        if togglebtnOne.active == True and togglebtnTwo.active == False:
            self.WindowManage.get_screen("main").ids["Float"].remove_widget(self.offimg)
            self.WindowManage.get_screen("main").camera_support(togglebtnOne, togglebtnTwo)
            
        elif togglebtnOne.active == True and togglebtnTwo.active == True:
            self.WindowManage.get_screen("main").camera_support(togglebtnOne, togglebtnTwo)
                    
        elif togglebtnOne.active == False and togglebtnTwo.active == True:
            togglebtnTwo.active = False
            self.WindowManage.get_screen("main").camera_support(togglebtnOne, togglebtnTwo)
            self.WindowManage.get_screen("main").ids["Float"].add_widget(self.offimg)
            
        elif togglebtnOne.active == False and togglebtnTwo.active == False:
            self.WindowManage.get_screen("main").camera_support(togglebtnOne, togglebtnTwo)
            self.WindowManage.get_screen("main").ids["Float"].add_widget(self.offimg)
            
            
    def popup(self):
        OKbtn = MDFlatButton(text = "OK", theme_text_color = 'Custom', text_color = (255/255, 255/255, 255/255, 1), 
                             md_bg_color = (74/255, 20/255, 140/255, 1), on_release = self.popdown)
        
        self.Pop = MDDialog(title = "Enable webcam", text = "Webcam must be enabled by the user to allow app to detect the user's hand gestures.", 
                            buttons = [OKbtn])
        self.Pop.open() 
        
    
    def check_Shutter(self, togbtnOne, togbtnTwo):
        if togbtnOne.active == True:
            if togbtnTwo.active == True:
                self.Change_imgs(togbtnOne, togbtnTwo)
        
        elif togbtnOne.active == False:
            if togbtnTwo.active == True:
                self.popup()
                togbtnTwo.active = False
                
        elif togbtnOne.active == True:
            if togbtnTwo.active == False:
                self.WindowManage.get_screen("main").ids["Float"].add_widget(self.offimg)
                self.Change_imgs(togbtnOne, togbtnTwo)
                

    def popdown(self, obj):
        self.Pop.dismiss()
        
        
    def ScrChange1(self):
        self.WindowManage.current = "settings"
        self.WindowManage.transition.direction = "left"
        
        
    def ScrChange2(self):
        self.WindowManage.current = "main"
        self.WindowManage.transition.direction = "right"
        
        
    def Theme_change(self):     
        if self.theme_cls.theme_style == "Light":         
            self.theme_cls.theme_style = "Dark"
            self.WindowManage.get_screen("main").ids["txtBoxlayout"].md_bg_color = (38/255, 50/255, 56/255, 1)
            self.WindowManage.get_screen("main").ids["txtCard"].md_bg_color = (97/255, 97/255, 97/255, 1)
            self.WindowManage.get_screen("main").ids["textin"].cursor_color = (238/255, 238/255, 238/255, 1)
            self.WindowManage.get_screen("main").ids["scrlv"].bar_color = (245/255, 245/255, 245/255, 1)
            self.WindowManage.get_screen("main").ids["textin"].foreground_color = (1, 1, 1, 1)
    
        else: 
            self.theme_cls.theme_style = "Light"
            self.WindowManage.get_screen("main").ids["txtBoxlayout"].md_bg_color = self.theme_cls.bg_normal
            self.WindowManage.get_screen("main").ids["txtCard"].md_bg_color = (189/255, 189/255, 189/255, 1) 
            self.WindowManage.get_screen("main").ids["textin"].cursor_color = (97/255, 97/255, 97/255, 1)
            self.WindowManage.get_screen("main").ids["scrlv"].bar_color = (117/255, 117/255, 117/255, 1)
            self.WindowManage.get_screen("main").ids["textin"].foreground_color = (0, 0, 0, 1)
            
 
        
if __name__ == "__main__":
    KivyMD().run()