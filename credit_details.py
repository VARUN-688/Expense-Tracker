import pandas as pd
import os
import re
import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

class AddCreditedTransactionScreen(Screen):
    def __init__(self, **kwargs):
        super(AddCreditedTransactionScreen, self).__init__(**kwargs)
        self.load_ui()

    def load_ui(self):
        # Check if bank details CSV exists and is not empty
        csv_file = 'bank_details.csv'
        if os.path.exists(csv_file):
            df_banks = pd.read_csv(csv_file)

            if df_banks.empty:
                self.show_no_banks_popup()
                return
        else:
            self.show_no_banks_popup()
            return

        # Create layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Bank selection dropdown (Spinner)
        self.bank_spinner = Spinner(
            text="Select Bank",
            values=[f"{row['Bank Name']}-{row['Branch Name']} ({row['Account Number']})" for index, row in df_banks.loc[df_banks["User"]==open('current_user.txt','r').read()].iterrows()],
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(Label(text="Select Bank:"))
        self.layout.add_widget(self.bank_spinner)

        # Input for transaction amount
        self.amount_input = TextInput(hint_text="Enter Amount", multiline=False, input_filter='float')
        self.layout.add_widget(Label(text="Amount:"))
        self.layout.add_widget(self.amount_input)

        # Category dropdown (Spinner)
        self.category_spinner = Spinner(
            text="Select Category",
            values=["Rent DVG","Rent BLG","Pension", "Salary", "Freelance", "Investment", "Other"],
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(Label(text="Category:"))
        self.layout.add_widget(self.category_spinner)

        # Save button
        save_button = Button(text="Save Transaction", size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_transaction)
        self.layout.add_widget(save_button)

        # Back button
        back_button = Button(text="Back to Main Menu", size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def show_no_banks_popup(self):
        # Popup to show message when no banks are available and navigate to Add Bank Details screen
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="No banks available. Please add a bank first."))

        # Button to navigate to the Add Bank screen
        add_bank_button = Button(text="Add Bank Now", size_hint=(1, 0.3))
        content.add_widget(add_bank_button)

        popup = Popup(title='No Banks Found', content=content, size_hint=(0.8, 0.4))

        # Bind the button to switch to the Add Bank screen
        add_bank_button.bind(on_press=lambda instance: self.go_to_add_bank(popup))

        popup.open()

    def go_to_add_bank(self, popup):
        popup.dismiss()
        self.manager.current = 'add_bank_details'

    def save_transaction(self, instance):
        # Gather transaction details
        selected_bank = self.bank_spinner.text
        amount = self.amount_input.text
        category = self.category_spinner.text

        x=re.compile('([A-Za-z]*)\-([A-Za-z]*)\s\(([0-9]{4})\)')
        det=x.search(selected_bank).groups()
        # Create DataFrame to store the transaction
        transaction_data = pd.DataFrame([{
            "Date":datetime.datetime.today().date(),
            "User":open('current_user.txt','r').read(),
            "Type":"Credit",
            "Bank": det[0],
            "Branch":det[1],
            "Account":det[2],
            "Amount": amount,
            "Category": category

        }])

        # Path to CSV file
        csv_file = 'transactions.csv'

        # If transactions.csv exists, append to it
        if os.path.exists(csv_file):
            df_existing = pd.read_csv(csv_file)
            df_combined = pd.concat([df_existing, transaction_data], ignore_index=True)
            df_combined.to_csv(csv_file, index=False)
        else:
            # Otherwise, create a new CSV file
            transaction_data.to_csv(csv_file, index=False)
        df_banks = pd.read_csv('bank_details.csv')
        bank_row = df_banks.loc[(df_banks['Bank Name'] == det[0]) & (df_banks['Account Number'] == int(det[2]))].index



        if not bank_row.empty:
            # Update the opening balance by adding the credited amount
            df_banks.loc[bank_row, 'Balance'] = df_banks.loc[bank_row, 'Balance'] + float(amount)

            # Save the updated data back to the CSV
            df_banks.to_csv("bank_details.csv", index=False)
            self.show_balance_popup(selected_bank, df_banks.loc[bank_row, 'Balance'].values[0])

        print("Transaction Saved:", transaction_data)

        self.clear_inputs()

    def clear_inputs(self):
        # Clear the inputs after saving
        self.bank_spinner.text = "Select Bank"
        self.amount_input.text = ''
        self.category_spinner.text = "Select Category"

    def go_back(self, instance):
        # Switch back to the main screen
        self.manager.current = 'main'

    def show_balance_popup(self, selected_bank, updated_balance):
        if updated_balance is not None:
            # Create a message for the popup
            content = f"Balance updated for \n{selected_bank.split(' ')[0]}: \n New Balance = {updated_balance}"

            # Create a layout for the popup
            self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            self.layout.add_widget(Label(text=content))

            # Add a button to close the popup
            close_button = Button(text="Close", size_hint=(1, 0.3))
            self.layout.add_widget(close_button)

            # Create and open the popup
            popup = Popup(title='Transaction Successful', content=self.layout, size_hint=(0.8, 0.4))
            close_button.bind(on_press=popup.dismiss)
            popup.open()
    def on_pre_enter(self, *args):
        # Reset the UI when the screen is about to be displayed # Clear any existing widgets
        self.load_ui()  # Reload the UI
