import pandas as pd
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import re
class AddFixedDepositScreen(Screen):

    def __init__(self, **kwargs):
        super(AddFixedDepositScreen, self).__init__(**kwargs)

        self.load_ui()
    def load_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        csv_file='fixed_deposit.csv'
        add_fd = Button(text="Add Fixed Deposit", size_hint=(1, 0.2))
        add_fd.bind(on_press=self.add_fixed_deposit)
        self.layout.add_widget(add_fd)
        if os.path.exists(csv_file):
            print("found")
            fd=pd.read_csv('fixed_deposit.csv')
            if fd.empty:
                self.layout.add_widget(Label(text="No Fixed Deposit so please add FD first"))

            else:
                for index, row in fd.iterrows():
                    row_layout = BoxLayout(orientation='horizontal', spacing=10)

                    bank_detail_label = Label(
                        text="",size_hint=(0.8, 1)
                    )
                    row_layout.add_widget(bank_detail_label)

        else:
            self.layout.add_widget(Label(text="No Fixed Deposit so add first."))



        self.add_widget(self.layout)
    def add_fixed_deposit(self,instance):
        self.layout.clear_widgets()
        csv_file = 'bank_details.csv'
        if os.path.exists(csv_file):
            df_banks = pd.read_csv(csv_file)
        self.bank_spinner = Spinner(
            text="Select Bank",
            values=[f"{row['Bank Name']}-{row['Branch Name']} ({row['Account Number']})" for index, row in
                    df_banks.iterrows()],
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(Label(text="Select Bank:"))
        self.layout.add_widget(self.bank_spinner)
        self.amount=TextInput(hint_text="Enter Amount")
        self.maturity_years=TextInput(hint_text="Enter Maturity Years")
        self.interest= TextInput(hint_text="Enter Interest Per Year")
        self.start_month = Spinner(
            text='Select Month',
            values=tuple(str(month) for month in range(1, 13))
        )

        # Spinner for selecting the year (you can customize the range as needed)
        self.start_year = Spinner(
            text='Select Year',
            values=tuple(str(year) for year in range(1990, 2051))
        )




        self.layout.add_widget(self.amount)
        self.layout.add_widget(self.start_month)
        self.layout.add_widget(self.start_year)
        self.layout.add_widget(self.interest)
        self.layout.add_widget(self.maturity_years)
        save_button = Button(
            text="Save Details",
            background_color=(0, 1, 0, 1),  # Green background
            color=(1, 1, 1, 1),  # White text
            font_size='20sp'  # Font size
        )
        save_button.bind(on_press=self.save_details)
        clear_button = Button(
            text="Clear Inputs",
            background_color=(1, 0, 0, 1),  # Red background
            color=(1, 1, 1, 1),  # White text
            font_size='18sp'  # Font size
        )
        clear_button.bind(on_press=self.clear_inputs)
        back_button = Button(
            text="Back to Main Menu",
            background_color=(0, 0, 1, 1),  # Blue background
            color=(1, 1, 1, 1),  # White text
            font_size='18sp'  # Font size
        )
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(save_button)
        self.layout.add_widget(clear_button)
        self.layout.add_widget(back_button)
    def save_details(self,instance):
        x = re.compile('([A-Za-z]*)\-([A-Za-z]*)\s\(([0-9]{4})\)')
        det = x.search(self.bank_spinner.text).groups()

        df = pd.DataFrame({
            "User":open('current_user.txt','r').read(),
            'Bank': det[0],  # Ensure det[0] is iterable (e.g., list)
            'Branch': det[1],  # Ensure det[1] is iterable (e.g., list)
            'Acct_no': det[2],  # Ensure det[2] is iterable (e.g., list)
            'Amount': [float(self.amount.text)],  # Convert to list
            'Start_month':[int(self.start_month.text)],
            'Start_year':[int(self.start_year.text)],

            'Interest': [float(self.interest.text)],  # Convert to list
            'Maturity_months': [int(self.maturity_years.text)]  # Convert to list
        })
        csv_file='fixed_deposit.csv'
        if os.path.exists(csv_file):
            fd=pd.read_csv(csv_file)
            fd=pd.concat([fd,df],ignore_index=True)
            fd.to_csv(csv_file,index=False)
        else:
            df.to_csv(csv_file,index=True)
        self.clear_inputs()






    def clear_inputs(self):
        self.bank_spinner.text="Select Bank"
        self.amount.text=""
        self.maturity_years.text=""
        self.interest.text=""
    def go_back(self,instance):
        self.clear_widgets()
        self.manager.current='main'
    def on_pre_enter(self, *args):
        # Reset the UI when the screen is about to be displayed
        self.layout.clear_widgets()  # Clear any existing widgets
        self.load_ui()  # Reload the UI



