from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.selectioncontrol import MDSwitch

from kivy.uix.screenmanager import Screen


class SettingsScr_widgets(Screen):

    def Switch(self, toggle):
        if toggle.active:
            toggle.active = False
        else:
            toggle.active = True

    
class ToggleSwitch(IRightBodyTouch, MDSwitch):
    pass

