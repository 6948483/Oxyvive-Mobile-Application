from PIL.ImageChops import screen
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen



class ServiceDashboard(MDScreen):
    selected_card = None
    registered_card =['OxiClinic','OxiWheel']

    def on_navigation(self, page):
        print(f"Navigation to {page}")

    def on_complete_steps(self):
        try:
            # Access the BottomNavigation widget and switch to 'service' tab
            bottom_nav = self.ids.bottom_nav
            bottom_nav.switch_tab('service')
        except Exception as e:
            print(f"Error: {e}")

    def on_card_select(self, card_id):

        # Deselect any previously selected card
        if card_id in self.registered_card:
            card = self.ids[card_id]
            for child in card.walk():
                if isinstance(child, MDLabel) and 'Oxi' in child.text:  # Adjust the logic if necessary
                    card_label = child
                    break
            card_label.text = f'[b]{card_id}[/b] [color=#097003] [size=10sp][i]Registered[/i][/size] [font=Icons]check-bold;[/font][/color]'  # Styled text in white
            card.md_bg_color = (0, 1, 0, 0.1)  # Green background for registered card
            card.line_color = (0, 1, 0, 1)  # Green outline for registered card
            continue_button = self.ids.continue_button
            continue_button.disabled = False
            return  # Do nothing further if the card is registered
        else:
            if self.selected_card:
                card = self.ids[self.selected_card]
                card.md_bg_color = (1, 1, 1, 1)  # White background when deselected
                card.line_color = (0.2, 0.2, 0.2, 0.8)  # Remove outline

            # Select the new card
            self.selected_card = card_id
            selected_card = self.ids[card_id]
            selected_card.md_bg_color = (1, 0, 0, 0.02)  # Keep background white
            selected_card.line_color = (1, 0, 0, 1)  # Red outline when selected

        # Enable the "Continue" button and change color to red
        continue_button = self.ids.continue_button
        continue_button.disabled = False
        continue_button.md_bg_color = (1, 0, 0, 1)  # Red when enabled

    def on_help_click(self):
        print("Help clicked")

    def on_continue_click(self):
        if self.selected_card:
            print(f"Selected card: {self.selected_card}")
            self.manager.load_screen('registration_steps')
            screen = self.manager.get_screen('registration_steps')
            screen.selected_service=self.selected_card
            self.manager.push_replacement('registration_steps')

        else:
            print("No option selected")

    def on_enter(self):

        self.on_card_select('OxiClinic')
        # Dynamically add doctor cards to the ScrollView's MDList

        doctors = [
            {"name": "Joshua Simorangkir", "specialty": "jsi@gmail.com", "rating": "13/09/2024",
             "image": "images/profile.jpg"},
            {"name": "Amelia Watson", "specialty": "ameliaw@gmail.com", "rating": "14/09/2024",
             "image": "images/profile.jpg"},
            {"name": "Joshua Simorangkir", "specialty": "jsi@gmail.com", "rating": "13/09/2024",
             "image": "images/profile.jpg"},
            {"name": "Amelia Watson", "specialty": "ameliaw@gmail.com", "rating": "14/09/2024",
             "image": "images/profile.jpg"},
            {"name": "Joshua Simorangkir", "specialty": "jsi@gmail.com", "rating": "13/09/2024",
             "image": "images/profile.jpg"},
            {"name": "Amelia Watson", "specialty": "ameliaw@gmail.com", "rating": "14/09/2024",
             "image": "images/profile.jpg"},
        ]

        for doctor in doctors:
            self.add_doctor_card(doctor)

    def add_doctor_card(self, doctor):
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
            source=doctor['image'],
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
            text=doctor['name'],
            font_style="Subtitle2",
            halign='left'
        )
        specialty_label = MDLabel(
            text=doctor['specialty'],
            font_style="Caption",
            halign='left'
        )
        rating_label = MDLabel(
            text=doctor['rating'],
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

