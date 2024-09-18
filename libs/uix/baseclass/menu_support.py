import json
import os
from kivy.core.window import Window
from plyer import filechooser
from anvil import BlobMedia
from anvil.tables import app_tables
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen


class Thank_You(MDScreen):
    def go_back(self):
        self.clear_widgets()
        details = SupportPage(manager=self.manager)
        self.add_widget(details)

    def go_home(self):
        self.manager.push_replacement("client_services")



class Contact_Us(MDScreen):
    screenshot_file_path = StringProperty('')
    def go_back(self):
        self.clear_widgets()
        details = SupportPage(manager=self.manager)
        self.add_widget(details)
    def send_message(self):
        name = self.ids.name_field.text
        email = self.ids.email_field.text
        message = self.ids.message_field.text
        screenshot_file_path = self.screenshot_file_path

        if not (name and email and message):
            self.show_validation_dialog("All fields must be filled in.")
            return

        if not screenshot_file_path:
            self.show_validation_dialog("Please attach a screenshot before sending.")
            return

        # Load user info
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_user_file_path = os.path.join(script_dir, "user_data.json")
        with open(json_user_file_path, 'r') as file:
            user_info = json.load(file)

        # Check for existing user data
        data = app_tables.oxi_users.get(oxi_email=email)
        if data:
            # Handle the uploaded file
            try:
                with open(screenshot_file_path, 'rb') as img_file:
                    image_data = img_file.read()
                    image_media = BlobMedia('image/png', image_data, name=os.path.basename(screenshot_file_path))

                print(f"File successfully read and converted to BlobMedia")
            except Exception as e:
                print(f"Error reading file: {e}")
                self.show_validation_dialog("Error handling the file. Please try again.")
                return

            # Add data to oxi_supports table with the BlobMedia object
            new_row = app_tables.oxi_supports.add_row(
                oxi_client_id=user_info.get('id'),
                oxi_email=user_info.get('email'),
                oxi_username=user_info.get('username'),
                oxi_message=message,
                oxi_media=image_media  # Save the BlobMedia object
            )

            self.clear_widgets()
            details = Thank_You(manager=self.manager)
            self.add_widget(details)
        else:
            self.ids.email_field.helper_text = "Enter registered email id"
    def upload_photo(self):
        # Open the file chooser with filters for image files
        filters = ["*.jpg", "*.jpeg", "*.png"]
        filechooser.open_file(filters=filters, on_selection=self.handle_selection)

    def handle_selection(self, selection):
        if not selection:
            print("No file selected")
            self.show_validation_dialog("No file selected. Please select a file.")
            return

        selected_file = selection[0]
        print("Selected file path:", selected_file)

        # Ensure that the selected file path is a string
        if not isinstance(selected_file, str):
            print("Invalid file path type:", type(selected_file))
            self.show_validation_dialog("Invalid file path. Please select a different file.")
            return

        # Check if the file exists and is accessible
        if os.path.exists(selected_file):
            try:
                # Update the label with the file name
                file_name = os.path.basename(selected_file)
                self.ids.screenshot_file_name.text = file_name

                # Store the file path for later use (e.g., sending)
                self.screenshot_file_path = selected_file

                print("File successfully selected:", file_name)
            except Exception as e:
                print("Error processing the file:", e)
                self.show_validation_dialog("Error processing the file. Please select a different file.")
        else:
            print("File does not exist or is not accessible")
            self.show_validation_dialog("File does not exist or is not accessible. Please select a different file.")

    def show_validation_dialog(self, message):
        # Display a dialog with the given message (implementation of dialog is assumed to be elsewhere)
        print(f"Validation: {message}")
    def helper(self):
        self.ids.email_field.helper_text = ""
class ExpandableMDCard(MDCard):
    expanded = BooleanProperty(False)
    tips = ListProperty([])
    original_icon = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(50)  # Set default height or any appropriate size

    def toggle(self):
        """Toggle the card between expanded and collapsed states."""
        self.expanded = not self.expanded

        if self.expanded:
            if not self.original_icon:
                self.original_icon = self.ids.icon.icon

            self.ids.tips_box.clear_widgets()

            for tip in self.tips:
                tip_label = MDLabel(
                    text=tip,
                    size_hint_y=None,
                    height=dp(30),
                    halign='left',
                    valign='middle',
                    font_size=dp(14),
                    theme_text_color='Custom',
                    text_color=(1, 1, 1, 1)
                )
                self.ids.tips_box.add_widget(tip_label)

            self.ids.tips_box.height = len(self.tips) * dp(30) + dp(10)
            self.height = self.ids.header.height + self.ids.tips_box.height + dp(10)
        else:
            self.ids.tips_box.clear_widgets()
            self.ids.tips_box.height = 0
            self.height = dp(50)

        self.ids.icon.icon = self.original_icon

class SupportPage(Screen):
    search_query = StringProperty("")

    def __init__(self, **kwargs):
        super(SupportPage, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)
        self.help_items = [
            {'text': 'Login Issues', 'icon': 'account', 'tips': [
                "Tip 1: Check your internet connection.",
                "Tip 2: Make sure your email is correct.",
                "Tip 3: Try resetting your password.",
                "Tip 4: Ensure your account isn't locked due to multiple failed attempts."
            ]},
            {'text': 'Signup Issues', 'icon': 'account', 'tips': [
                "Tip 1: Use a valid email.",
                "Tip 2: Check your spam folder for verification email.",
                "Tip 3: Make sure your password meets the complexity requirements.",
                "Tip 4: Try using a different browser or clearing your cache.",
                "Tip 5: Ensure the email hasn't already been used for an account."
            ]},
            {'text': 'Reports Information', 'icon': 'file-document', 'tips': [
                "Tip 1: Ensure all data is correct before generating a report.",
                "Tip 2: Use the 'Preview' option to check the report before finalizing.",
                "Tip 3: Save your reports regularly to avoid data loss.",
                "Tip 4: Export reports in multiple formats for flexibility."
            ]},
            {'text': 'Booking Nearby Services', 'icon': 'map-marker', 'tips': [
                "Tip 1: Enable GPS for better accuracy.",
                "Tip 2: Double-check the service location before confirming.",
                "Tip 3: Book during off-peak hours for quicker service.",
                "Tip 4: Verify the service provider's credentials before booking."
            ]},
            {'text': 'Making Payments', 'icon': 'credit-card', 'tips': [
                "Tip 1: Check your card details.",
                "Tip 2: Ensure you have sufficient balance.",
                "Tip 3: Use secure payment methods only.",
                "Tip 4: Save your receipt for future reference.",
                "Tip 5: Contact support if your payment fails."
            ]}
        ]
        self.populate_help_list()

    def on_keyboard(self, instance, key, scancode, codepoint, modifier):
        if key == 27:  # Keycode for the back button on Android
            self.go_back()
            return True
        return False

    def go_back(self):
        self.manager.push_replacement("client_services", "right")

    def populate_help_list(self):
        """Populate the help list with all items initially."""
        self.ids.help_list.clear_widgets()
        for item in self.help_items:
            card = ExpandableMDCard()
            card.ids.icon.icon = item['icon']
            card.ids.label.text = item['text']
            card.tips = item['tips']
            self.ids.help_list.add_widget(card)

    def filter_help_list(self, query):
        """Filter the help list based on the search query and expand the matching item."""
        self.ids.help_list.clear_widgets()

        # If the search query is empty, populate the list without expanding any cards
        if not query.strip():
            self.populate_help_list()
            return

        # If there is a query, filter and expand the matching items
        for item in self.help_items:
            if query.lower() in item['text'].lower():
                card = ExpandableMDCard()
                card.ids.icon.icon = item['icon']
                card.ids.label.text = item['text']
                card.tips = item['tips']
                self.ids.help_list.add_widget(card)
                card.toggle()  # Automatically expand the card

    def on_query_change(self, instance, value):
        self.search_query = value
        self.filter_help_list(value)

    def contact_us(self):
        self.clear_widgets()
        details = Contact_Us(manager=self.manager)
        self.add_widget(details)
