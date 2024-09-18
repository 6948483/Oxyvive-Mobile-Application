from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen


class LicenseDoc(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Customize UI based on document type passed
        self.item_name = ""
        self.submitted_forms = []

    def animate_hint_text(self, text_field, focused):
        if focused:
            # Animate hint text when the text field is focused
            text_field.set_pos_hint_text(y=0.2)  # Move hint text upwards (Y-axis)
            text_field.set_hint_text_font_size(12)  # Reduce font size when focused
        else:
            # Animate hint text back when not focused
            text_field.set_pos_hint_text(y=0.5)  # Return to normal position (center Y)
            text_field.set_hint_text_font_size(6)  # Return to normal font size

    def on_enter(self):
        # Customize fields based on item_name (document type)
        if self.item_name == "Clinic License":
            self.update_fields(
                "Enter your clinic license number and date of birth",
                "Clinic License Number",
                "Clinic license number",
                "clinic_license_image.png",
                show_dob=True,
                default_text="CL000000000"
            )

        elif self.item_name == "PAN Card":
            self.update_fields(
                "Enter your PAN number",
                "PAN Card Number",
                "Enter your PAN card number",
                "pan_image_path.png",
                show_dob=False,
                default_text="ABCDE1234F"
            )

        elif self.item_name == "Aadhaar Card":
            self.update_fields(
                "Enter your Aadhaar number",
                "Aadhaar Card Number",
                "Aadhaar number",
                "aadhaar_image_path.png",
                show_dob=False,
                default_text="1234 5678 9012"
            )

        elif self.item_name == "Building Certificate":
            self.update_fields(
                "Enter your building certificate number",
                "Building Certificate Number",
                "Building certificate number",
                "building_certificate_image.png",
                show_dob=False,
                default_text="BC000000"
            )

        elif self.item_name == "Insurance":
            self.update_fields(
                "Enter your insurance policy number and date of birth",
                "Insurance Policy Number",
                "Insurance policy number",
                "insurance_image_path.png",
                show_dob=True,
                default_text="IN000000"
            )

        elif self.item_name == "Clinic Permit":
            self.update_fields(
                "Enter your clinic permit number",
                "Clinic Permit Number",
                "Clinic permit number",
                "clinic_permit_image_path.png",
                show_dob=False,
                default_text="CP000000"
            )

    def update_fields(self, instruction_text, label_text, hint_text, image_path, show_dob, default_text=""):
        # Update instruction label and image
        self.ids.instruction_label.text = instruction_text
        self.ids.license_image.source = image_path

        # Show and update the License Number label and field
        self.ids.license_label.text = label_text  # Update label text
        self.ids.license_field.hint_text = hint_text  # Update hint text
        self.ids.license_field.text = default_text  # Set the default text (can be empty)

        # Show or hide DOB field
        if show_dob:
            self.ids.dob_label.opacity = 1
            self.ids.dob_label.disabled = False
            self.ids.dob_field.opacity = 1
            self.ids.dob_field.disabled = False
        else:
            self.ids.dob_label.opacity = 0
            self.ids.dob_label.disabled = True
            self.ids.dob_field.opacity = 0
            self.ids.dob_field.disabled = True

    def submit_form(self):
        # Dictionary to store form details
        form_data = {}

        # Handle form submission logic based on document type
        if self.item_name == "Clinic License":
            form_data = {
                "document_type": "Clinic License",
                "license_number": self.ids.license_field.text,
                "dob": self.ids.dob_field.text,
            }
        elif self.item_name == "PAN Card":
            form_data = {
                "document_type": "PAN Card",
                "pan_number": self.ids.license_field.text,
            }
        elif self.item_name == "Aadhaar Card":
            form_data = {
                "document_type": "Aadhaar Card",
                "aadhaar_number": self.ids.license_field.text,

            }
        elif self.item_name == "Building Certificate":
            form_data = {
                "document_type": "Building Certificate",
                "certificate_number": self.ids.license_field.text,
            }
        elif self.item_name == "Insurance":
            form_data = {
                "document_type": "Insurance",
                "policy_number": self.ids.license_field.text,
                "dob": self.ids.dob_field.text
            }
        elif self.item_name == "Clinic Permit":
            form_data = {
                "document_type": "Clinic Permit",
                "permit_number": self.ids.license_field.text,
            }

        # Append the form data to the list of submitted forms
        self.submitted_forms.append(form_data)

        # After submission, update the registration step status
        registration_screen = self.manager.get_screen('registration_steps')
        registration_screen.update_item_status(self.item_name)

        self.manager.push_replacement('registration_steps')

        print(f"Current list of submitted forms: {self.submitted_forms}")

    def upload_document(self):
        print(f"Upload document for {self.item_name}")
        # Logic for uploading a document
        print("Redirecting to upload document page")
        self.manager.push_replacement('take_photo')
        # After the screen is switched, set the item_name dynamically
        screen = self.manager.get_screen('take_photo')
        screen.item_name = self.item_name
        screen.on_enter()

    def go_back(self):
            # Logic for back arrow
            print("Going back to the previous page")
            self.manager.push_replacement('registration_steps')

    def open_help(self):
        # Logic for help action
        print("Opening help section")

    def show_date_picker(self):
        # Show the MDDatePicker when date of birth field is clicked
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_dob, on_cancel=self.on_cancel)
        date_dialog.open()

    def set_dob(self, instance, value, date_range):
        # Set the selected date in the dob text field
        self.ids.dob_field.text = value.strftime('%d/%m/%Y')

    def on_cancel(self, instance, value):
        # Handle cancel event (optional)
        print("Date picker canceled")

    def on_focus(self, text_field, focused):
        # Call the animate_hint_text method based on focus
        self.animate_hint_text(text_field, focused)
