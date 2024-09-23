import os
import json
from server import Server
from anvil import tables
from anvil.tables import app_tables
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import anvil.server
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.tab import MDTabs, MDTabsLabel, MDTabsBase
anvil.server.connect("server_MQU7VM2VS3ZSCQL3SRGX3EZA-J25NXHNSQOR7LIWH")


class HomeScreen(Screen):

    def on_enter(self):
        # Fetch today's appointments when the screen is entered
        self.fetch_todays_appointments()

    def fetch_todays_appointments(self):
        # Fetch the latest appointment details from the 'oxi_book_slot' table
        appointments = app_tables.oxi_book_slot.search(
            tables.order_by('oxi_book_date', ascending=False)
        )
        # Clear the existing appointments in the MDList
        self.ids.today_appointments_list.clear_widgets()

        # Populate the appointments in the list
        for appointment in appointments:
            self.add_appointment_card(appointment)

    def add_appointment_card(self, appointment):
        # Extract appointment details
        doctor_name = appointment['oxi_username']
        book_date = appointment['oxi_book_date']
        book_time = appointment['oxi_book_time']
        location = appointment['oxi_location']

        # Access theme_cls from the running MDApp instance
        theme_cls = MDApp.get_running_app().theme_cls

        # Create a new card with the appointment details
        card = MDCard(
            orientation='vertical',
            padding=dp(10),
            size_hint=(None, None),
            size=(dp(320), dp(140)),
            md_bg_color=theme_cls.primary_color,  # Use theme color
            pos_hint={"center_x": 0.5}
        )

        # Create a box layout to hold the card content
        card_layout = MDBoxLayout(
            orientation='horizontal',
            padding=dp(6),
            spacing=dp(10)
        )

        # Create a layout for the doctor's image
        image_box = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(50), dp(50))
        )
        image = FitImage(source="images/profile.jpg")
        size_hint = (None, None),  # Disable size hints
        size = (dp(50), dp(50)),  # Set desired width and height
        # Placeholder for doctor's image
        image_box.add_widget(image)

        # Create a layout for the doctor's details
        info_box = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )

        # Doctor's name label
        name_label = MDLabel(
            text=doctor_name,
            font_style="Subtitle1",
            halign='left',
            color=(1, 1, 1, 1)
        )

        # Layout for location with icon
        location_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(5)
        )
        location_icon = MDIcon(
            icon='map-marker',
            size_hint=(None, None),
            size=(dp(20), dp(20)),
            halign='left',
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        location_label = MDLabel(
            text=f" {location}",
            font_style="Caption",
            halign='left',
            color=(1, 1, 1, 1)
        )
        location_layout.add_widget(location_icon)
        location_layout.add_widget(location_label)

        # Layout for date and time with icons
        date_time_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10)
        )

        # Date icon and label
        date_icon = MDIcon(
            icon='calendar',
            size_hint=(None, None),
            size=(dp(20), dp(20)),
            halign='left',
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        date_label = MDLabel(
            text=f"{book_date}",
            font_style="Caption",
            halign='left',
            theme_text_color="Custom",
            color=(1, 1, 1, 1)
        )

        # Time icon and label
        time_icon = MDIcon(
            icon='clock-outline',
            size_hint=(None, None),
            size=(dp(20), dp(20)),
            halign='left',
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        time_label = MDLabel(
            text=f"{book_time}",
            font_style="Caption",
            halign='left',
            color=(1, 1, 1, 1),
            text_color=(1, 1, 1, 1)
        )

        # Add date and time icons/labels to layout
        date_time_layout.add_widget(date_icon)
        date_time_layout.add_widget(date_label)
        date_time_layout.add_widget(time_icon)
        date_time_layout.add_widget(time_label)

        # Add name, location, and date-time layouts to the info box
        info_box.add_widget(name_label)
        info_box.add_widget(location_layout)
        info_box.add_widget(date_time_layout)

        # Add the image and info boxes to the card layout
        card_layout.add_widget(image_box)
        card_layout.add_widget(info_box)

        # Add the layout to the card
        card.add_widget(card_layout)

        # Add the card to the MDList
        self.ids.today_appointments_list.add_widget(card)

        # Add spacing between this card and the next one
        self.ids.today_appointments_list.add_widget(Widget(size_hint_y=None, height=dp(10)))

    def show_appointment_details(self, doctor_name, book_date, book_time, location):
        # Switch to AppointmentDetailScreen and update the details
        self.manager.current = 'AppointmentDetailScreen'

        # Access the AppointmentDetailScreen and update the fields
        detail_screen = self.manager.get_screen('AppointmentDetailScreen')
        detail_screen.ids.doctor_name.text = doctor_name
        detail_screen.ids.appointment_time.text = f"Time: {book_time}"
        detail_screen.ids.appointment_location.text = f"Location: {location}"


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
            # The card creation logic
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

            # Image layout
            image_layout = BoxLayout(
                orientation='vertical',
                size_hint_x=None,
                width='50dp',
                padding='5dp',
                pos_hint={'center_y': 0.5}  # Center align the image vertically
            )
            image_layout.add_widget(
                FitImage(
                    source="2.png",  # Use actual path to image
                    size_hint=(None, None),
                    size=("50dp", "50dp"),
                    radius=[dp(50)]  # Circular Image
                )
            )

            # Text layout
            text_layout = BoxLayout(
                orientation='vertical',
                padding='8dp'
            )

            # Username label
            text_layout.add_widget(
                MDLabel(
                    text=f"{appointment['username']}",
                    font_style="Subtitle1",
                    halign="left",
                    size_hint_y=None,
                    height='30dp',
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1)  # White text
                )
            )

            # Service type label
            text_layout.add_widget(
                MDLabel(
                    text=f"{appointment['service_type']}",
                    font_style="Caption",
                    halign="left",
                    size_hint_y=None,
                    height='20dp',
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1)  # White text
                )
            )

            # Date layout
            date_layout = BoxLayout(
                orientation='horizontal',
                spacing='5dp',
                size_hint_y=None,
                height='20dp'
            )

            date_layout.add_widget(
                MDIcon(icon="calendar", size_hint_x=None, width='20dp', theme_text_color="Custom",
                       text_color=(1, 1, 1, 1))
            )
            date_layout.add_widget(
                MDLabel(
                    text=f"{appointment['date_time']}, {appointment['book_time']}",
                    font_style="Caption",
                    halign="left",
                    size_hint_y=None,
                    height='20dp',
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1)  # White text
                )
            )

            text_layout.add_widget(date_layout)

            # Add image and text to the card
            card.add_widget(image_layout)
            card.add_widget(text_layout)

            # Add card to the container
            card_container.add_widget(card)
            card_container.add_widget(
                Widget(size_hint_y=None, height='5dp')  # Spacer to avoid overlap
            )

            # Add container to the appointment list
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
    def back_button(self):
        # Navigate back to the previous screen
        self.manager.current = 'home'



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


