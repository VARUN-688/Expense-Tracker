from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import pandas as pd
import os


class AddBankDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super(AddBankDetailsScreen, self).__init__(**kwargs)
        # Layout for form inputs (same as before)
        user=open('current_user.txt','r')

        self.current_user=user.read()
        print(self.current_user)
        user.close()
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Form inputs (same as before)
        self.bank_name_input = TextInput(hint_text="Bank Name", multiline=False)
        self.branch_name_input = TextInput(hint_text="Branch Name", multiline=False)
        self.opening_balance_input = TextInput(hint_text="Opening Balance", multiline=False)
        self.account_number_input = TextInput(hint_text="Account Number (last 4 digits)", multiline=False)

        self.layout.add_widget(Label(text="Enter Bank Details"))
        self.layout.add_widget(self.bank_name_input)
        self.layout.add_widget(self.branch_name_input)
        self.layout.add_widget(self.opening_balance_input)
        self.layout.add_widget(self.account_number_input)

        # Save Button (same as before)
        save_button = Button(text="Save", size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_bank_details)
        self.layout.add_widget(save_button)

        # Back Button (same as before)
        back_button = Button(text="Back to Main Menu", size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def save_bank_details(self, instance):
        # Dictionary to store bank details
        self.bank_details = pd.DataFrame([{
            "User":open('current_user.txt','r').read(),
            "Bank Name": self.bank_name_input.text,
            "Branch Name": self.branch_name_input.text,
            "Balance": float(self.opening_balance_input.text),
            "Account Number": self.account_number_input.text
        }])

        # Path to CSV file
        csv_file = 'bank_details.csv'

        # If the CSV file exists and is not empty, append to it
        if os.path.exists(csv_file):
            # Load existing CSV
            df_existing = pd.read_csv(csv_file)

            # Concatenate the new data with existing data
            df_combined = pd.concat([df_existing, self.bank_details], ignore_index=True)

            # Write the combined DataFrame back to the CSV
            df_combined.to_csv(csv_file, index=False)
        else:
            # If CSV does not exist, write the new DataFrame directly
            self.bank_details.to_csv(csv_file, index=False)

        print("Bank Details Saved:", self.bank_details)
        self.clear_inputs()
        self.manager.current = 'main'

    def clear_inputs(self):
        # Clear input fields after saving
        self.bank_name_input.text = ''
        self.branch_name_input.text = ''
        self.opening_balance_input.text = ''
        self.account_number_input.text = ''

    def go_back(self, instance):
        self.clear_inputs()
        self.manager.current = 'main'
# Reload the UI
