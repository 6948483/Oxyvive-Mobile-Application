import json
import os
from kivy.utils import platform
from kivy.app import App
from kivy.core.window import Window
from kivymd.app import MDApp
from libs.uix.root import Root

class ShotApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Shot"
        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Red'
        self.root = Root()
        self.root.push("main_sc")
        self.request_all_permissions()

    def on_start(self):
        with open("logged_in_data.json", "r") as json_file:
            logged_in_data = json.load(json_file)
        if logged_in_data["logged_in"]:
            self.root.load_screen("client_services")
            self.root.current = "client_services"
        else:
            self.root.load_screen("main_sc")
            self.root.current = "main_sc"

    def request_all_permissions(self):
        if platform == 'android':
            from jnius import autoclass, cast
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            PackageManager = autoclass('android.content.pm.PackageManager')

            permissions = [
                'android.permission.ACCESS_FINE_LOCATION',
                'android.permission.READ_CONTACTS',
                'android.permission.READ_EXTERNAL_STORAGE',
                'android.permission.WRITE_EXTERNAL_STORAGE',
                'android.permission.SEND_SMS',
                'android.permission.CALL_PHONE'
            ]

            granted_permissions = [
                permission for permission in permissions
                if PythonActivity.mActivity.checkSelfPermission(permission) == PackageManager.PERMISSION_GRANTED
            ]

            if len(granted_permissions) != len(permissions):
                PythonActivity.mActivity.requestPermissions(permissions, 1)
            else:
                print("All permissions already granted!")

# Run the app
if __name__ == '__main__':
    ShotApp().run()
