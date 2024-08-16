import json
import os
import bcrypt
import re
from anvil.tables import app_tables
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.spinner import MDSpinner
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button


class Settings(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading_dialog = None
        Window.bind(on_keyboard=self.on_keyboard)

        # Bind on_text event for real-time validation in the __init__ method
        Clock.schedule_interval(self.auto_validate, 0.5)

    def auto_validate(self, *args):
        self.password_valid = bool(
            self.ids.new_password.text and self.validate_password(self.ids.new_password.text)[
                0])

    def on_password_change(self, instance, value):
        self.password_valid, hint_text = self.validate_password(value)
        if not self.password_valid:
            self.ids.new_password.error = True
            self.ids.new_password.helper_text = hint_text
        else:
            self.ids.new_password.error = False
            self.ids.new_password.helper_text = ""

    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            self.back_screen()
            return True
        return False

    def back_screen(self):
        self.manager.current = 'client_services'

    # def validate_and_reset_password(self):
    #     old_password = self.ids.old_password.text
    #     new_password = self.ids.new_password.text
    #     confirm_password = self.ids.confirm_password.text
    #
    #     script_dir = os.path.dirname(os.path.abspath(__file__))
    #     json_user_file_path = os.path.join(script_dir, "user_data.json")
    #     with open(json_user_file_path, 'r') as file:
    #         user_info = json.load(file)
    #
    #     if not old_password or not new_password or not confirm_password:
    #         self.show_dialog("Error", "All fields are required!")
    #         return
    #
    #     if not bcrypt.checkpw(old_password.encode('utf-8'), user_info['password'].encode('utf-8')):
    #         self.show_dialog("Error", "Old Password is incorrect")
    #         return
    #
    #     if new_password != confirm_password:
    #         self.show_dialog("Error", "New passwords do not match!")
    #         return
    #
    #     # Show loading animation
    #     self.show_loading_animation()
    #
    #     # Hash the new password
    #     hash_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    #
    #     # Update the user's password in the Anvil Data Table
    #     user_row = app_tables.oxi_users.get(oxi_id=user_info['id'])
    #     if user_row:
    #         user_row['oxi_password'] = hash_password
    #
    #     # Clear the text fields
    #     self.ids.old_password.text = ""
    #     self.ids.new_password.text = ""
    #     self.ids.confirm_password.text = ""
    #
    #     # Show success animation after 2 seconds
    #     Clock.schedule_once(lambda dt: self.show_success_animation(), 2)

    def validate_and_reset_password(self):
        old_password = self.ids.old_password.text
        new_password = self.ids.new_password.text
        confirm_password = self.ids.confirm_password.text

        # Check if any field is empty
        if not old_password or not new_password or not confirm_password:
            self.show_popup("Error", "Some fields are empty!")
            return

        # Load user data from JSON file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_user_file_path = os.path.join(script_dir, "user_data.json")
        with open(json_user_file_path, 'r') as file:
            user_info = json.load(file)

        # Initialize user_row to None
        user_row = None

        # If password is missing in the JSON file, fetch it from the database
        if 'password' not in user_info:
            user_row = app_tables.oxi_users.get(oxi_id=user_info['id'])
            if user_row:
                db_password = user_row['oxi_password']
            else:
                self.show_popup("Error", "User data not found!")
                return
        else:
            db_password = user_info['password']

        # Check if the old password matches the database password
        if not bcrypt.checkpw(old_password.encode('utf-8'), db_password.encode('utf-8')):
            self.show_popup("Error", "Old password is incorrect!")
            return

        # Check if new password and confirm password match
        if new_password != confirm_password:
            self.show_popup("Error", "New passwords do not match!")
            return

        # Show loading animation
        self.show_loading_animation()

        # Hash the new password
        hash_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Update the user's password in the database
        user_row = app_tables.oxi_users.get(oxi_id=user_info['id'])
        if user_row:
            user_row['oxi_password'] = hash_password

        # Clear the text fields
        self.ids.old_password.text = ""
        self.ids.new_password.text = ""
        self.ids.confirm_password.text = ""

        # Show success animation after 2 seconds
        Clock.schedule_once(lambda dt: self.show_success_animation(), 2)

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        message_label = Label(
            font_size=25,
            text=message,
            text_size=(0.8 * Window.width, None),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        message_label.bind(size=message_label.setter('text_size'))

        ok_button = Button(
            text="OK",
            font_size=dp(25),
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(1, 0, 0, 1),  # Red color
            color=(1, 1, 1, 1),
            on_release=lambda x: popup.dismiss()
        )

        popup_content.add_widget(message_label)
        popup_content.add_widget(ok_button)

        popup = Popup(
            title=title,
            title_color=(0, 0, 0, 1),  # Black title
            content=popup_content,
            size_hint=(0.8, 0.3),
            background='white',
            auto_dismiss=False  # Prevent dismissal without pressing OK
        )
        popup.open()

    def show_loading_animation(self):
        layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            size=(dp(300), dp(200)),
        )

        spinner = MDSpinner(size_hint=(None, None), size=(dp(46), dp(46)))
        layout.add_widget(spinner)
        layout.add_widget(MDLabel(text="Resetting Password...", halign="center"))

        self.loading_dialog = MDDialog(
            type="custom",
            content_cls=layout,
        )
        self.loading_dialog.open()

    def show_success_animation(self):
        # Close the loading dialog first
        if hasattr(self, 'loading_dialog'):
            self.loading_dialog.dismiss()

        layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            size=(dp(300), dp(200)),
        )

        checkmark = MDLabel(text="[size=100]✓[/size]", markup=True, halign="center")
        layout.add_widget(checkmark)
        layout.add_widget(MDLabel(text="Password Reset Successfully!", halign="center"))

        self.success_dialog = MDDialog(
            type="custom",
            content_cls=layout,
        )
        self.success_dialog.open()

        # Automatically dismiss the success dialog after 2 seconds
        Clock.schedule_once(lambda dt: self.success_dialog.dismiss(), 2)
        self.manager.push_replacement("login")

    def validate_password(self, password):
        # Check if the password is not empty
        if not password:
            return False, "Password cannot be empty"
        # Check if the password has at least 6 characters
        if len(password) < 6:
            return False, "Password must have at least 6 characters"
        # Check if the password contains both uppercase and lowercase letters
        if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
            return False, "Password must contain uppercase, lowercase"
        # Check if the password contains at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        # Check if the password contains at least one special character
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]"
        if not re.search(special_characters, password):
            return False, "Password must contain a special character"
        # All checks passed; the password is valid
        return True, "Password is valid"
