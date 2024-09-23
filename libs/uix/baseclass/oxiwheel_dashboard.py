import datetime
import json
import os

from PIL.ImageChops import screen
from anvil import tables
from anvil.tables import app_tables
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

class TodayAppointment(BoxLayout):
    doctor_name = StringProperty("")
    book_date = StringProperty("")
    book_time = StringProperty("")
    location = StringProperty("")

    def __init__(self, doctor_name=None, book_date=None, book_time=None, location=None, **kwargs):
        super(TodayAppointment, self).__init__(**kwargs)
        self.doctor_name = doctor_name if doctor_name is not None else ""
        self.book_date = book_date if book_date is not None else ""
        self.book_time = book_time if book_time is not None else ""
        self.location = location if location is not None else ""

class OxiwheelServiceDashboard(MDScreen):
    selected_card = None
    registered_card = ['OxiClinic', 'OxiGym']

    def on_navigation(self, page):
        print(f"Navigation to {page}")

    def on_complete_steps(self):
        try:
            # Access the BottomNavigation widget and switch to 'service' tab
            bottom_nav = self.ids.bottom_nav
            bottom_nav.switch_tab('service')
        except Exception as e:
            print(f"Error: {e}")

    def on_help_click(self):
        print("Help clicked")

    def on_enter(self):
        self.fetch_todays_appointments()

        # doctors = [
        #     {"name": "Joshua Simorangkir", "specialty": "jsi@gmail.com", "rating": "13/09/2024",
        #      "image": "images/profile.jpg"},
        #     {"name": "Amelia Watson", "specialty": "ameliaw@gmail.com", "rating": "14/09/2024",
        #      "image": "images/profile.jpg"},
        #     {"name": "Joshua Simorangkir", "specialty": "jsi@gmail.com", "rating": "13/09/2024",
        #      "image": "images/profile.jpg"},
        #     {"name": "Amelia Watson", "specialty": "ameliaw@gmail.com", "rating": "14/09/2024",
        #      "image": "images/profile.jpg"},
        #     {"name": "Joshua Simorangkir", "specialty": "jsi@gmail.com", "rating": "13/09/2024",
        #      "image": "images/profile.jpg"},
        #     {"name": "Amelia Watson", "specialty": "ameliaw@gmail.com", "rating": "14/09/2024",
        #      "image": "images/profile.jpg"},
        # ]
        #
        # for doctor in doctors:
        #     self.add_doctor_card(doctor)

    def add_doctor_card(self, appointment):
        doctor_name = appointment['oxi_username']
        book_date = appointment['oxi_book_date'].strftime("%Y-%m-%d")  # Format date as string
        location = appointment['oxi_location']
        # Create the card

        card = MDCard(
            orientation='horizontal',
            padding=(dp(10), dp(10)),
            size_hint_y=None,
            height=dp(80),
            elevation=1
        )

        # Create the box for the image
        image_box = BoxLayout(
            size_hint=(None, None),
            size=(dp(50), dp(50))
        )

        # Add the image (assuming it's a local image or a URL with AsyncImage)
        image = AsyncImage(
            source="images/profile.jpg",
            allow_stretch=True,
            keep_ratio=True
        )
        image_box.add_widget(image)

        # Create the box for the doctor's information
        info_box = BoxLayout(
            orientation='vertical'
        )

        # Add the doctor's name, specialty, and rating labels
        name_label = MDLabel(
            text=doctor_name,
            font_style="Subtitle2",
            halign='left'
        )
        specialty_label = MDLabel(
            text=location,
            font_style="Caption",
            halign='left'
        )
        rating_label = MDLabel(
            text=book_date,
            font_style="Caption",
            halign='left'
        )

        info_box.add_widget(name_label)
        info_box.add_widget(specialty_label)
        info_box.add_widget(rating_label)

        # Add the image and info boxes to the card
        card.add_widget(image_box)
        card.add_widget(info_box)

        # Add the card to the list
        self.ids.doctor_list.add_widget(card)

    def see_all_appointments(self):
        print("See All Appointments Clicked!")

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

    def convert_time_to_datetime(self, time_str):
        """
        Converts a time string in 'H AM/PM' or 'H:MM AM/PM' format to a datetime.time object.
        """
        return datetime.datetime.strptime(time_str, '%I%p').time()

    def fetch_todays_appointments(self):
        servicer_id = "OW01234"  # Replace this with the actual servicer ID logic

        # Fetch the latest appointment details based on servicer ID
        appointments = app_tables.oxi_book_slot.search(
            tables.order_by('oxi_book_date', ascending=True),
            oxi_servicer_id=servicer_id
        )

        # Get today's date and current time
        today = datetime.datetime.now().date()
        current_time = datetime.datetime.now().time()

        # Separate appointments into two categories
        today_appointments = []
        future_appointments = []
        print(appointments)
        for appointment in appointments:
            print(appointment)
            appointment_date = appointment['oxi_book_date']

            # Parse the oxi_book_time string (e.g., '11am - 1pm')
            appointment_time_range = appointment['oxi_book_time']
            try:
                # Debugging: Check time range string
                print(f"Appointment time range: {appointment_time_range}")

                # Split into start and end times
                start_time_str, end_time_str = appointment_time_range.split(' - ')
                start_time_24 = self.convert_time_to_datetime(start_time_str.strip())
                end_time_24 = self.convert_time_to_datetime(end_time_str.strip())

                # Debugging: Print converted times
                print(f"Start time (24-hour format): {start_time_24}, End time (24-hour format): {end_time_24}")
            except ValueError as e:
                # If parsing fails, skip this appointment or handle the error
                print(f"Error parsing time range for appointment: {e}")
                continue

            if appointment_date == today:
                # Check if current time is within the appointment time range
                if start_time_24>= current_time :
                    today_appointments.append(appointment)  # It's today's and within the time range
            elif appointment_date > today:
                future_appointments.append(appointment)  # Anything from tomorrow onwards

        # Clear the existing list in the UI
        self.ids.today_appointments_list.clear_widgets()

        # Now populate today's and upcoming appointments
        for appointment in today_appointments:
            self.add_appointment_card(appointment)  # Today’s gang ⏳

        self.ids.doctor_list.clear_widgets()
        for appointment in future_appointments:
            self.add_doctor_card(appointment)  # Future dates gang 🚀

        print(today_appointments)
        print(future_appointments)


    def add_appointment_card(self, appointment):
        # Extract appointment details
        doctor_name = appointment['oxi_username']
        # doctor_email = appointment['oxi_email']  # Assuming there's an email field
        book_date = appointment['oxi_book_date'].strftime("%Y-%m-%d")  # Format date as string
        book_time = appointment['oxi_book_time']  # Format time as string
        location = appointment['oxi_location']

        # Create an instance of TodayAppointment
        appointment_card = TodayAppointment(
            doctor_name=doctor_name,
            book_date=book_date,
            book_time=book_time,
            location=location
        )

        # Add the new card to the appointment list
        self.ids.today_appointments_list.add_widget(appointment_card)

