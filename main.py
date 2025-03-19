from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from add_bank_details import AddBankDetailsScreen
from view_bank_details import ViewBankDetailsScreen
from credit_details import AddCreditedTransactionScreen
from debit_details import AddDebitedTransactionScreen
from fixed_deposit_details import AddFixedDepositScreen
from lic_details import AddLICScreen
from sign_up import SignUp
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from login_page import LoginScreen
from dashoboard import ExpenseDashboard

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background Image
        with self.canvas.before:
            self.bg = Rectangle(source="background.png", pos=self.pos, size=self.size)

        self.bind(size=self.update_bg)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        # Transparent Spacer for Centering
        layout.add_widget(Widget(size_hint_y=0.5))

        # Heading Label
        title = Label(
            text="Expense Tracker",
            font_size=50,
            bold=True,
            color=(1, 1, 1, 1)  # White Color
        )
        layout.add_widget(title)

        # Signup Button
        signup_btn = Button(
            text="Sign Up",
            size_hint=(None, None),
            size=(250, 60),
            background_color=(0, 0.6, 1, 1),  # Blue Color
            font_size=20,
            bold=True
        )
        signup_btn.bind(on_press=lambda instance: setattr(self.manager, 'current', 'signup'))
        layout.add_widget(signup_btn)

        # Login Button
        login_btn = Button(
            text="Login",
            size_hint=(None, None),
            size=(250, 60),
            background_color=(0.1, 0.8, 0.2, 1),  # Green Color
            font_size=20,
            bold=True
        )
        login_btn.bind(on_press=lambda instance: setattr(self.manager, 'current', 'login'))
        layout.add_widget(login_btn)

        # Spacer for Centering
        layout.add_widget(Widget(size_hint_y=0.5))

        self.add_widget(layout)

    def update_bg(self, *args):
        """ Update background image when window resizes """
        self.bg.pos = self.pos
        self.bg.size = self.size
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Background image
        self.bg = Image(source='background.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg)

        # Main layout (BoxLayout for overlaying on the background)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title label (Stretching across the top)
        title = Button(
            text="Expense Tracker",
            font_size=50,
            bold=True,
            size_hint=(1, 0.2),
            background_color=(0, 0, 0, 0),  # Transparent
            color=(1, 1, 1, 1)  # White text
        )
        main_layout.add_widget(title)

        # Grid layout for buttons (Adjusted for full-page coverage)
        button_grid = GridLayout(cols=3, padding=10, spacing=15, size_hint=(1, 0.8))

        # Button labels
        button_names = [
            "Add Bank Details", "View Bank Details", "Credit",
            "Debit", "Investment", "Fixed Deposit",
            "Recurring Deposit", "LIC", "EMI","Dashboard"
        ]

        # Add buttons dynamically
        for name in button_names:
            button = Button(
                text=name,
                font_size=22,
                size_hint=(1, 1),  # Each button stretches to fill available space
                background_color=(0.2, 0.6, 1, 1),  # Blue color
                color=(1, 1, 1, 1)  # White text
            )
            button.bind(on_press=self.on_button_click)
            button_grid.add_widget(button)

        # Add the grid layout to main layout
        main_layout.add_widget(button_grid)

        # Overlay layouts on the screen
        self.add_widget(main_layout)

    def on_button_click(self, instance):
        screen_map = {
            "View Bank Details": "view_bank_details",
            "Add Bank Details": "add_bank_details",
            "Credit": "credited_details",
            "Debit": "debited_details",
            "Investment": "investment_details",
            "Fixed Deposit": "fixed_deposit",
            "Recurring Deposit": "recurring_deposit",
            "LIC": "lic_details",
            "EMI": "emi_details",
            "Dashboard":"expense_dashboard"
        }

        if instance.text in screen_map:
            self.manager.current = screen_map[instance.text]


class ExpenseTrackerApp(App):
    def build(self):
        # Create ScreenManager
        temp=open("current_user.txt","w")
        temp.write("")
        temp.close()
        sm = ScreenManager()

        # Add screens
        sm.add_widget(HomeScreen(name="homescreen"))
        sm.add_widget(SignUp(name="signup"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AddBankDetailsScreen(name='add_bank_details'))
        sm.add_widget(ViewBankDetailsScreen(name='view_bank_details'))
        sm.add_widget(AddCreditedTransactionScreen(name='credited_details'))
        sm.add_widget(AddDebitedTransactionScreen(name='debited_details'))
        sm.add_widget(AddFixedDepositScreen(name='fixed_deposit'))
        sm.add_widget(AddLICScreen(name="lic_details"))
        sm.add_widget(ExpenseDashboard(name="expense_dashboard"))
        return sm



# Run the app
if __name__ == '__main__':
    ExpenseTrackerApp().run()
