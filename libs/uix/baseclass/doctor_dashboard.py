import os
import json
from anvil.tables import app_tables
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import anvil.server
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.tab import MDTabs, MDTabsLabel, MDTabsBase


class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        def on_pre_enter(self, *args):
            if os.path.exists('user_data.json'):
                with open('user_data.json', 'r') as f:
                    user_data = json.load(f)
                username = user_data.get("username", "User")
            else:
                username = "Guest"  # Default username if no user data exists
            self.ids.username_label.text = username
    def go_to_wheel(self):
        self.manager.current ="appointment"
    def go_to_gym(self):
        self.manager.current = "appointment"
    def go_to_clinic(self):
        self.manager.current = "appointment"

    def see_all_appointments(self):
        if not self.manager.has_screen("AppointmentScreen"):
            self.manager.add_widget(AppointmentScreen(name="AppointmentScreen"))
        self.manager.current = "AppointmentScreen"
class AppointmentScreen(Screen):
    doctor_oxi_id = None  # Placeholder for storing the doctor's oxi_id

    def on_enter(self):
        # Default behavior when entering the screen can be fetching all appointments
        self.load_appointments_by_status('Upcoming')

    def load_appointments_by_status(self, status):
        """
        Fetch appointments based on the booking status (Upcoming, Complete, or Cancel).
        """
        # Fetch all appointments from local Anvil DB

        status_label = {
            'Upcoming': 'Upcoming Bookings',
            'Complete': 'Completed Bookings',
            'Cancel': 'Cancelled Bookings'
        }
        self.ids.booking_status_label.text = status_label.get(status, "Upcoming Bookings")
        all_appointments = self.fetch_all_from_db()
        self.filter_appointments_by_status(all_appointments, status)

    def fetch_all_from_db(self):
        """
        Query the Anvil table directly from Python (assuming local Anvil DB is accessible).
        """
        appointments = app_tables.oxi_book_slot.search()
        return appointments

    def filter_appointments_by_status(self, all_appointments, status):
        """
        Filter appointments based on the status and doctor's oxi_id.
        """
        filtered_appointments = [
            {
                'username': appt['oxi_username'],
                'service_type': appt['oxi_service_type'],
                'date_time': appt['oxi_book_date'],
                'status': appt['oxi_booking_status'],
                'book_time': appt['oxi_book_time']
            }
            for appt in all_appointments
            if appt['oxi_id'] == 'CL90452'  # Filter by doctor ID
            and appt['oxi_booking_status'] == status  # Filter by booking status
        ]

        # Update the list view with the filtered data
        self.update_appointment_list(filtered_appointments)

    def update_appointment_list(self, appointments):
        """
        Update the UI with the filtered appointments list.
        """
        self.ids.appointment_list.clear_widgets()  # Clear existing widgets

        for appointment in appointments:
            # The card creation logic as you have it
            card_container = BoxLayout(
                orientation='vertical',
                padding='10dp',
                size_hint_y=None
            )
            card_container.bind(minimum_height=card_container.setter('height'))

            card = MDCard(
                orientation='horizontal',
                padding='8dp',
                spacing='5dp',
                size_hint=(None, None),
                size=("320dp", "120dp"),
                pos_hint={"center_x": 0.5},
                elevation=1,
                radius=[dp(15), dp(15), dp(15), dp(15)],
            )

            image_layout = BoxLayout(
                orientation='vertical',
                size_hint_x=None,
                width='50dp',
                padding='5dp',
                pos_hint={'center_y': 0.7}
            )
            image_layout.add_widget(
                FitImage(
                    source="2.png",  # Use actual path to image
                    size_hint=(None, None),
                    size=("50dp", "50dp"),
                    radius=[dp(50)]  # Circular Image
                )
            )

            text_layout = BoxLayout(
                orientation='vertical',
                padding='8dp'
            )

            text_layout.add_widget(
                MDLabel(
                    text=f"{appointment['username']}",
                    font_style="Subtitle1",
                    halign="left",
                    size_hint_y=None,
                    height='30dp',
                    theme_text_color="Primary"
                )
            )
            text_layout.add_widget(
                MDLabel(
                    text=f"{appointment['service_type']}",
                    font_style="Caption",
                    halign="left",
                    size_hint_y=None,
                    height='20dp',
                    theme_text_color="Secondary"
                )
            )

            date_layout = BoxLayout(
                orientation='horizontal',
                spacing='5dp',
                size_hint_y=None,
                height='20dp'
            )

            date_layout.add_widget(
                MDIcon(icon="calendar", size_hint_x=None, width='20dp', theme_text_color="Secondary")
            )
            date_layout.add_widget(
                MDLabel(
                    text=f"{appointment['date_time']}, {appointment['book_time']}",
                    font_style="Caption",
                    halign="left",
                    size_hint_y=None,
                    height='20dp',
                    theme_text_color="Secondary"
                )
            )

            text_layout.add_widget(date_layout)

            card.add_widget(image_layout)
            card.add_widget(text_layout)

            card_container.add_widget(card)
            card_container.add_widget(
                Widget(size_hint_y=None, height='5dp')  # Spacer to avoid overlap
            )

            self.ids.appointment_list.add_widget(card_container)


    def show_appointment_detail(self, appointment):
        """
        Navigate to the AppointmentDetailScreen and pass the appointment details.
        """
        # Access the detail screen from the manager
        detail_screen = self.manager.get_screen('appointment_detail')  # Ensure this screen is defined in your manager
        detail_screen.appointment = appointment  # Set the appointment attribute
        detail_screen.update_details(appointment)  # Update the details on the screen
        self.manager.current = 'appointment_detail'


class AppointmentDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.appointment = None  # Placeholder for appointment data

    def update_details(self, appointment):
        """Update the screen with the appointment details."""
        self.appointment = appointment
        # Update the UI elements here with the appointment data
        # For example:
        self.ids.username_label.text = appointment['username']
        self.ids.service_type_label.text = appointment['service_type']
        self.ids.date_time_label.text = f"{appointment['date_time']}, {appointment['book_time']}"

    def back_button(self):
        if not self.manager.has_screen("AppointmentScreen"):
            self.manager.add_widget(AppointmentScreen(name="AppointmentScreen"))
        self.manager.current = "AppointmentScreen"


class ProfileScreen(Screen):
    def on_enter(self):
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as json_file:
                user_info = json.load(json_file)
            # Update UI elements with user data
            self.ids.profile_image.source = user_info.get('profile', '')  # Default to an empty string if not found
            self.ids.username_label.text = user_info.get('username', 'Unknown User')
            self.ids.email_label.text = user_info.get('email', 'No Email')
            self.ids.phone_label.text = user_info.get('phone', 'No Phone Number')
        else:
            # Clear or set default values when no user data is available
            self.ids.profile_image.source = ''  # No profile image
            self.ids.username_label.text = 'Guest'
            self.ids.email_label.text = 'No Email'
            self.ids.phone_label.text = 'No Phone Number'

    def go_back(self):

        if not self.manager.has_screen("HomeScreen"):
            self.manager.add_widget(HomeScreen(name="HomeScreen"))
        self.manager.current = "HomeScreen"

    def logout(self):
        # Update logged_in_data.json to set logged_in status to False
        if os.path.exists('logged_in_data.json'):
            with open('logged_in_data.json', 'r+') as json_file:
                logged_in_data = json.load(json_file)
                logged_in_data["logged_in"] = False  # Set logged_in to False
                json_file.seek(0)  # Go to the start of the file
                json.dump(logged_in_data, json_file)  # Write the updated data
                json_file.truncate()  # Remove any leftover data

        # Delete the user_data.json file
        if os.path.exists('user_data.json'):
            os.remove('user_data.json')

        # Navigate to the login screen
        self.manager.load_screen('login')
        self.manager.current = "login"


class MyApp(Screen):
    def on_enter(self):
        self.theme_cls.primary_palette = "Red"
        # Load the correct .kv file
        Builder.load_file('doctor_dashboard.kv')

        # Initialize the ScreenManager
        sm = ScreenManager()
        # Add all screens to the ScreenManager
        sm.add_widget(HomeScreen(name='HomeScreen'))

        sm.add_widget(AppointmentScreen(name='AppointmentScreen'))
        sm.add_widget(AppointmentDetailScreen(name='AppointmentDetailScreen'))
        sm.add_widget(ProfileScreen(name='ProfileScreen'))

        return sm


