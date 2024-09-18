import os

import cv2
from kivy.utils import platform
from kivymd.uix.screen import MDScreen
from plyer import camera
from plyer.utils import platform

# Windows-specific import (OpenCV)
if platform == 'win':
    pass

# Android-specific import (Plyer or other camera methods)
if platform == 'android':
    from android.permissions import request_permissions, Permission


class TakePhotoForDoc(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Customize UI based on document type passed
        self.item_name = ""
        self.submissions = []
        self.photo_captured = False
        self.image_path = ""



    def on_enter(self, *args):
        # Update the title, labels, and instructions based on the document name
        self.update_content(self.item_name)

    def update_content(self, document_name):
        # Dynamically update based on the document type
        if document_name == 'Clinic License':
            self.ids.title_label.text = "Take a photo of your Clinic License"
            self.ids.instructions_label.text = ("1. Upload backside of the Clinic License first, if some information is present on the backside before uploading the front side.\n"
                                                "2. Ensure that the License number, License Type, your Name, Address, D.O.B, Expiration Date, and the official logo are clearly visible.\n"
                                                "3. The photo should not be blurred.")
            self.ids.sample_image.source = 'clinic_license_sample.png'

        elif document_name == 'Profile Photo':
            self.ids.title_label.text = "Upload your Profile Photo"
            self.ids.instructions_label.text = ("1. Make sure your face is clearly visible.\n"
                                                "2. The photo should not be blurry or pixelated.\n"
                                                "3. This will be used as your official profile photo.")
            self.ids.sample_image.source = 'profile_photo_sample.png'

        elif document_name == 'Aadhaar Card':
            self.ids.title_label.text = "Take a photo of your Aadhaar Card"
            self.ids.instructions_label.text = ("1. Upload both sides of your Aadhaar Card.\n"
                                                "2. Ensure that your Aadhaar number, Name, Date of Birth, and Address are clearly visible.\n"
                                                "3. The photo should not be blurred.")
            self.ids.sample_image.source = 'aadhaar_card_sample.png'

        elif document_name == 'PAN Card':
            self.ids.title_label.text = "Take a photo of your PAN Card"
            self.ids.instructions_label.text = ("1. Ensure that the PAN number, Name, Date of Birth, and Signature are clearly visible.\n"
                                                "2. Upload the front side of your PAN Card.\n"
                                                "3. The photo should not be blurred.")
            self.ids.sample_image.source = 'pan_card_sample.png'

        elif document_name == 'Building Certificate':
            self.ids.title_label.text = "Take a photo of your Building Certificate"
            self.ids.instructions_label.text = ("1. Ensure that the Certificate details, including the building address, and ownership information, are clearly visible.\n"
                                                "2. The document should validate the eligibility of the premises for conducting business operations.\n"
                                                "3. The photo should not be blurred.")
            self.ids.sample_image.source = 'building_certificate_sample.png'

        elif document_name == 'Insurance':
            self.ids.title_label.text = "Take a photo of your Insurance Document"
            self.ids.instructions_label.text = ("1. Ensure that the Insurance Policy number, your Name, and coverage details are clearly visible.\n"
                                                "2. Upload both sides if necessary.\n"
                                                "3. The photo should not be blurred.")
            self.ids.sample_image.source = 'insurance_sample.png'

        elif document_name == 'Clinic Permit':
            self.ids.title_label.text = "Take a photo of your Clinic Permit"
            self.ids.instructions_label.text = ("1. Ensure that the Permit number, Clinic Name, and the expiration date are clearly visible.\n"
                                                "2. Ensure that the document is valid and the details are clearly readable.\n"
                                                "3. The photo should not be blurred.")
            self.ids.sample_image.source = 'clinic_permit_sample.png'

        else:
            # Default content if the document name is not recognized
            self.ids.title_label.text = "Take a photo of your document"
            self.ids.instructions_label.text = "Ensure that the details on the document are clearly visible and not blurred."
            self.ids.sample_image.source = 'default_sample.png'

    def on_back_button(self):
        # Implement back button functionality
        print("Back button pressed")
        self.manager.push_replacement('registration_steps')

    def take_photo(self):
        # Detect platform and run appropriate camera code
        if platform == 'android':
            self.capture_image_android()
        elif platform == 'win':
            self.capture_image_windows()
        else:
            print("Platform not supported for camera functionality.")

    # Android camera capture functionality
    def capture_image_android(self):
        def on_request_permissions(permissions, grant_results):
            if all(grant_results):
                self.take_photo_android()
            else:
                print("Camera permission denied")

        # Request camera permissions if required
        request_permissions([Permission.CAMERA], on_request_permissions)

    def take_photo_android(self):
        # Using Plyer or Kivy's built-in camera
        print("Opening camera on Android")
        file_name = f"{self.item_name.lower().replace(' ', '_')}_photo.jpg"
        save_dir = os.path.join(os.getenv('EXTERNAL_STORAGE'), "CapturedPhotos")
        os.makedirs(save_dir, exist_ok=True)
        self.image_path = os.path.join(save_dir, file_name)

        # Use Plyer to capture the photo
        camera.take_picture(self.image_path, self.on_android_photo_taken)

    def on_android_photo_taken(self, image_path):
        if os.path.exists(image_path):
            print(f"Photo saved at {image_path}")
            submission = {
                'document_type': self.item_name,
                'image_path': image_path
            }
            self.submissions.append(submission)
            self.photo_captured = True
            print(f"Submissions: {self.submissions}")
        else:
            print("Error: Failed to capture photo on Android.")

    # Windows camera capture functionality using OpenCV
    def capture_image_windows(self):
        # Open the webcam using OpenCV
        cap = cv2.VideoCapture(0)  # 0 is the default camera

        if not cap.isOpened():
            print("Error: Could not open the webcam.")
            return

        # Capture a frame
        ret, frame = cap.read()

        if ret:
            # Save the image locally
            file_name = f"{self.item_name.lower().replace(' ', '_')}_photo.png"
            save_dir = os.path.join(os.path.expanduser("~"), "Documents", "CapturedPhotos")
            os.makedirs(save_dir, exist_ok=True)
            self.image_path = os.path.join(save_dir, file_name)

            # Write the image to file
            cv2.imwrite(self.image_path, frame)
            self.photo_captured = True

            # Store the captured image information in the list
            submission = {
                'document_type': self.item_name,
                'image_path': self.image_path
            }
            self.submissions.append(submission)

            print(f"Photo saved at {self.image_path}")
            print(f"Submissions: {self.submissions}")

            # After submission, update the registration step status
            registration_screen = self.manager.get_screen('registration_steps')
            registration_screen.update_item_status(self.item_name)

            self.manager.push_replacement('registration_steps')
        else:
            print("Error: Could not capture image from the webcam.")

        # Release the camera and close the OpenCV window
        cap.release()
        cv2.destroyAllWindows()

    def on_back_button(self):
        # Implement back button functionality
        print("Back button pressed")
        self.manager.push_replacement('registration_steps')

    def show_help(self):
        # Implement help button functionality
        print("Help button pressed")