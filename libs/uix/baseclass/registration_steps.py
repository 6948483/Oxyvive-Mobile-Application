from kivy.lang import Builder
from kivymd.uix.screen import MDScreen


class RegistrationSteps(MDScreen):

    items = [
        {"text": "Clinic License", "status": "Recommended next step"},
        {"text": "Profile Photo", "status": "Pending"},
        {"text": "Aadhaar Card", "status": "Pending"},
        {"text": "PAN Card", "status": "Pending"},
        {"text": "Building Certificate", "status": "Pending"},
        {"text": "Insurance", "status": "Pending"},
        {"text": "Clinic Permit", "status": "Pending"}
    ]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_service=''

    def on_enter(self):
        # Clear the list container and add items
        self.ids.list_container.clear_widgets()
        for item in self.items:
            status = item['status']
            secondary_text_color = self.get_status_color(status)
            self.add_list_item(item['text'], status, secondary_text_color)

        # Check if all items are completed and switch screens if true
        if all(item['status'] == "Completed" for item in self.items):
            self.switch_to_service_dashboard()

    def update_item_status(self, current_item_name):
        # Find the current item and set its status to "Completed"
        for item in self.items:
            if item['text'] == current_item_name:
                item['status'] = "Completed"
                break

        # Check if any item already has "Recommended next step" status
        recommended_item_found = any(item['status'] == "Recommended next step" for item in self.items)

        # If no "Recommended next step" exists, set it to the next "Pending" item
        if not recommended_item_found:
            for item in self.items:
                if item['status'] == "Pending":
                    item['status'] = "Recommended next step"
                    break

        # Refresh the list to reflect status changes
        self.on_enter()

    def get_status_color(self, status):
        # Define color mapping based on status
        if status == "Completed":
            return 0, 1, 0, 1  # Green for completed
        elif status == "Recommended next step":
            return 0, 0, 1, 1  # Blue for recommended
        elif status == "Pending":
            return 1, 1, 1, 1  # White for pending

    def add_list_item(self, text, status, secondary_text_color):
        # Create a TwoLineRightIconListItem dynamically and adjust based on the status
        if status == "Completed":
            # No icon or on_release action for completed items
            item = Builder.load_string(f'''
TwoLineRightIconListItem:
    text: "{text}"
    secondary_text: "{status}"
    secondary_theme_text_color: "Custom"
    secondary_text_color: {secondary_text_color[0]}, {secondary_text_color[1]}, {secondary_text_color[2]}, {secondary_text_color[3]}
    secondary_font_style: "Caption"
    on_release: None  # Disable on_release functionality for completed items
    ''')
        else:
        # Add icon and on_release action for non-completed items
            item = Builder.load_string(f'''
TwoLineRightIconListItem:
    text: "{text}"
    secondary_text: "{status}"
    secondary_theme_text_color: "Custom"
    secondary_text_color: {secondary_text_color[0]}, {secondary_text_color[1]}, {secondary_text_color[2]}, {secondary_text_color[3]}
    secondary_font_style: "Caption"
    on_release: app.get_running_app().root.current_screen.show_details("{text}")
    IconRightWidget:
        icon: "chevron-right"
        on_release: app.get_running_app().root.current_screen.show_details("{text}")
    ''')

        # Add the item to the list container
        self.ids.list_container.add_widget(item)

    def show_details(self, item_name):
        # Switch to the appropriate document screen
        if item_name == "Profile Photo":
            self.manager.push_replacement('take_photo')
            screen = self.manager.get_screen('take_photo')
            screen.item_name = item_name
            screen.on_enter()
        else:
            self.manager.push_replacement('Clinic License')

            # After the screen is switched, set the item_name dynamically
            screen = self.manager.get_screen('Clinic License')
            screen.item_name = item_name
            screen.on_enter()  # Call the on_enter to refresh the UI based on the new item_name

    def open_help(self):
        print("Help button clicked")

    def switch_to_service_dashboard(self):
        # Add the card ID to the registered_card list
        screen = self.manager.get_screen('service_dashboard')
        screen.registered_card.append(self.selected_service)

        # Switch to the service_dashboard screen
        self.manager.push_replacement( 'service_dashboard')
