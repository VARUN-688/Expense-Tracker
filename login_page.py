from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
import pandas as pd
import os

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Background Image
        self.bg = Image(source='background.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg)

        # Main Layout
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        # Title Label
        title = Label(text="Login", font_size=50, bold=True, size_hint=(1, 0.2), color=(1, 1, 1, 1))
        layout.add_widget(title)

        # Form Layout
        form_layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(0.6, 0.4), pos_hint={'center_x': 0.5})

        # Username Field
        form_layout.add_widget(Label(text="Username:", font_size=22, color=(1, 1, 1, 1)))
        self.username = TextInput(hint_text="Enter your username", font_size=20, multiline=False)
        form_layout.add_widget(self.username)

        # Password Field
        form_layout.add_widget(Label(text="Password:", font_size=22, color=(1, 1, 1, 1)))
        self.password = TextInput(hint_text="Enter your password", font_size=20, password=True, multiline=False)
        form_layout.add_widget(self.password)

        # Login Button
        self.login_button = Button(text="Login", font_size=22, size_hint=(1, 0.5), background_color=(0.2, 0.6, 1, 1))
        self.login_button.bind(on_press=self.check_credentials)
        form_layout.add_widget(self.login_button)

        # Error Label (Hidden initially)
        self.error_label = Label(text="", font_size=18, color=(1, 0, 0, 1))
        form_layout.add_widget(self.error_label)

        layout.add_widget(form_layout)
        temp_btn=Button(text="Default", font_size=22, size_hint=(None, None), size=(200, 50),
                             background_color=(0.8, 0, 0, 1))
        temp_btn.bind(on_press=self.fill_default)
        back_button = Button(text="Back", font_size=22, size_hint=(None, None), size=(200, 50),
                             background_color=(0.8, 0, 0, 1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        layout.add_widget(temp_btn)
        self.add_widget(layout)

    def check_credentials(self, instance):
        """Checks username and password against users.csv"""
        filename = "users.csv"

        if not os.path.exists(filename):
            self.error_label.text = "No users registered!"
            return

        df = pd.read_csv(filename)

        username_input = self.username.text.strip()
        password_input = self.password.text.strip()

        if ((df["username"] == username_input) & (df["password"] == password_input)).any():
            self.error_label.text = "Login Successful!"
            self.manager.current = "main"  # Redirect to main page
        else:
            self.error_label.text = "Invalid username or password!"
        r=open("current_user.txt",mode='w')
        r.write(self.username.text)
        r.close()
    def go_back(self, instance):
        """Navigates back to the main screen"""
        self.manager.current = "homescreen"
    def fill_default(self,instance):
        self.username.text="Varunspatil"
        self.password.text="Varun@2003"
