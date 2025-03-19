from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
import pandas as pd
import re
import os


class SignUp(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 📌 Background Image Setup
        with self.canvas.before:
            self.bg = Rectangle(source="background.png", pos=self.pos, size=self.size)
        self.bind(size=self.update_bg, pos=self.update_bg)

        # 📌 Main Layout (Shifted Up)
        main_layout = BoxLayout(orientation='vertical', padding=[30, 80, 30, 30], spacing=15)

        # 📌 Title
        title = Label(text="Expense Tracker", font_size=50, bold=True, color=(1, 1, 1, 1), size_hint_y=None, height=60)
        main_layout.add_widget(title)

        # 📌 Sign-up Section (Split Layout)
        sign_layout = BoxLayout(orientation='horizontal', padding=10, spacing=30, size_hint_y=None, height=400)

        # 📌 Left Layout (Form)
        left_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_x=0.5)
        self.right_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_x=0.5)

        # 📌 Input Fields (Larger Font Size)
        left_layout.add_widget(Label(text="Sign Up", font_size=35, color=(1, 1, 1, 1)))

        left_layout.add_widget(Label(text="Username", color=(1, 1, 1, 1)))
        self.username = TextInput(hint_text="Enter Username", font_size=22, size_hint_x=0.9, height=50)
        left_layout.add_widget(self.username)

        left_layout.add_widget(Label(text="Password", color=(1, 1, 1, 1)))
        self.pwd = TextInput(hint_text="Enter Password", font_size=22, password=True, size_hint_x=0.9, height=50)
        left_layout.add_widget(self.pwd)

        left_layout.add_widget(Label(text="Re-Enter Password", color=(1, 1, 1, 1)))
        self.repwd = TextInput(hint_text="Enter Password Again", font_size=22, password=True, size_hint_x=0.9, height=50)
        left_layout.add_widget(self.repwd)

        # 📌 Check Button
        check_btn = Button(text="Check", size_hint_x=0.6, height=50, background_color=(0, 0.6, 1, 1))
        check_btn.bind(on_press=self.check)
        left_layout.add_widget(check_btn)
        back_button = Button(text="Back", font_size=22, size_hint=(None, None), size=(200, 50),
                             background_color=(0.8, 0, 0, 1))
        back_button.bind(on_press=self.go_back)
        sign_layout.add_widget(left_layout)
        sign_layout.add_widget(self.right_layout)
        main_layout.add_widget(sign_layout)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def update_bg(self, *args):
        """ 🖼 Update background image when window resizes """
        self.bg.pos = self.pos
        self.bg.size = self.size

    def check(self, instance):
        """ ✅ Validate inputs and display results neatly """
        self.right_layout.clear_widgets()

        filename = "users.csv"
        if not os.path.exists(filename):
            df = pd.DataFrame(columns=["username", "password"])
            df.to_csv(filename, index=False)
        else:
            df = pd.read_csv(filename)

        # 📌 Regex Patterns
        un = re.compile("^[A-Z][A-Za-z]+$")
        pwd1 = re.compile("[A-Z]+")
        pwd2 = re.compile("[a-z]+")
        pwd3 = re.compile("[0-9]+")
        pwd4 = re.compile("[\!\@\#\$\%\^\&\*\-]")

        usn = self.username.text
        pswd = self.pwd.text
        re_pswd = self.repwd.text

        username_taken = usn in df["username"].values
        valid_username = len(usn) >= 8 and un.match(usn) and not username_taken
        valid_password = (
            len(pswd) >= 8 and
            pwd1.search(pswd) and
            pwd2.search(pswd) and
            pwd3.search(pswd) and
            pwd4.search(pswd)
        )
        passwords_match = pswd == re_pswd

        # 📌 Username Validation
        username_layout = BoxLayout(orientation='horizontal', spacing=10)
        username_label_text = "✅ Username available" if not username_taken else "❌ Username taken"
        username_layout.add_widget(Label(text=username_label_text, color=(1, 1, 1, 1)))
        username_checkbox = CheckBox(active=valid_username)
        username_layout.add_widget(username_checkbox)
        self.right_layout.add_widget(username_layout)

        # 📌 Password Validation
        password_layout = BoxLayout(orientation='horizontal', spacing=10)
        password_layout.add_widget(Label(text="✅ Password valid" if valid_password else "❌ Password weak", color=(1, 1, 1, 1)))
        password_checkbox = CheckBox(active=valid_password)
        password_layout.add_widget(password_checkbox)
        self.right_layout.add_widget(password_layout)

        # 📌 Re-Entered Password Validation
        repwd_layout = BoxLayout(orientation='horizontal', spacing=10)
        repwd_layout.add_widget(Label(text="✅ Passwords match" if passwords_match else "❌ Passwords don't match", color=(1, 1, 1, 1)))
        repwd_checkbox = CheckBox(active=passwords_match)
        repwd_layout.add_widget(repwd_checkbox)
        self.right_layout.add_widget(repwd_layout)

        # 📌 "Sign Up" Button if All Conditions Are Met
        if valid_username and valid_password and passwords_match:
            signup_button = Button(text="Sign Up", size_hint_x=0.6, height=50, background_color=(0, 1, 0.5, 1))
            self.right_layout.add_widget(signup_button)
            signup_button.bind(on_press=self.create_account)

    def create_account(self, instance):
        """ 📦 Create user account and save to CSV """

        filename = "users.csv"
        new_user = pd.DataFrame([[self.username.text, self.pwd.text]], columns=["username", "password"])
        new_user.to_csv(filename, mode='a', header=False, index=False)

        print(f"🎉 User {self.username.text} added successfully!")
        self.manager.current = 'main'
        r = open("current_user.txt", mode='w')
        r.write(self.username.text)
        r.close()
    def go_back(self, instance):
        """Navigates back to the main screen"""
        self.manager.current = "homescreen"
