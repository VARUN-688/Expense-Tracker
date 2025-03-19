import pandas as pd
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
import re
class AddLICScreen(Screen):
    def __init__(self, **kwargs):
            super(AddLICScreen, self).__init__(**kwargs)
            self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            self.add_widget(self.layout)
            self.load_ui()  # Initial UI load when the screen is created

    def load_ui(self):
        # Check if bank details CSV exists and is not empty
        csv_file = 'lic_details.csv'
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="No Insurence available. Please add a bank first."))
        button=Button(text="Add insurence")
        button.bind(on_press=self.add_lic_details)
        content.add_widget(button)
        # Button to navigate to the Add Bank screen

        popup = Popup(title='No Banks Found',content=content, size_hint=(0.8, 0.4))

        # Bind the button to switch to the Add Bank screen
        if os.path.exists(csv_file):

            self.layout.clear_widgets()
            self.clear_widgets()



            df = pd.read_csv("lic_details.csv")
            col=list(df.columns)

            self.clear_widgets()
            grid_layout = GridLayout(cols=len(df.columns), padding=10, spacing=10)

            # Add column headers
            for col in df.columns:
                col_label = Label(text=f"{col}")
                grid_layout.add_widget(col_label)

            # Add data rows
            for i in range(df.shape[0]):
                for j in df.columns:
                    data_label = Label(text=str(df.loc[i, j]), size_hint=(1, 0.2))
                    grid_layout.add_widget(data_label)
            button = Button(text="Add insurence", size_hint=(1,0.2))
            button.bind(on_press=self.add_lic_details)
            self.layout.add_widget(button)
            self.layout.add_widget(Label(text="Avaliable Insurence", size_hint=(1, 0.2)))
            self.layout.add_widget(grid_layout)
            self.add_widget(self.layout)


            back_button = Button(
                text="Back to Main Menu",
                background_color=(0, 0, 1, 1),  # Blue background
                color=(1, 1, 1, 1),  # White text
                font_size='18sp'  # Font size
            )
            back_button.bind(on_press=self.go_back)
            self.layout.add_widget(back_button)



        else:
            self.layout.add_widget(popup)
    def add_lic_details(self,instance):
        self.policy_number=TextInput(hint_text="Policy Number",multiline=False)
        self.prem_amount=TextInput(hint_text="Premium Amount",multiline=False)
        self.start_month = Spinner(
            text='Select Month',
            values=tuple(str(month) for month in range(1, 13))
        )

        # Spinner for selecting the year (you can customize the range as needed)
        self.start_year = Spinner(
            text='Select Year',
            values=tuple(str(year) for year in range(1990, 2051))
        )
        self.end_year = Spinner(
            text='Select End Year',
            values=tuple(str(year) for year in range(2024,2100))
        )
        self.payment_peroid=Spinner(
            text='Select Payment Peroid',
            values=tuple(str(month) for month in range(1,13))
        )
        self.latest_payment_date=Spinner(
            text="Select Latest Payment Date",
            values = tuple(f"{month}/{year}" for year in range(2022, 2025) for month in range(1, 13))

        )
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
        self.layout.clear_widgets()

        self.layout.add_widget(self.policy_number)
        self.layout.add_widget(self.prem_amount)
        self.layout.add_widget(self.start_month)
        self.layout.add_widget(self.start_year)
        self.layout.add_widget(self.end_year)
        self.layout.add_widget(self.payment_peroid)
        self.layout.add_widget(self.latest_payment_date)
        self.layout.add_widget(save_button)
        self.layout.add_widget(clear_button)
        self.layout.add_widget(back_button)


    def save_details(self,instance):
        df = pd.DataFrame([{
            "User":open('current_user.txt','r').read(),
            'Policy Number': self.policy_number.text,
            'Premium Amount': float(self.prem_amount.text),
            'Start Month': int(self.start_month.text),
            'Start Year': int(self.start_year.text),
            'End Year': int(self.end_year.text),
            'Payment Period': int(self.payment_peroid.text),
            'Latest Payment': self.latest_payment_date.text
        }])
        csv_file='lic_details.csv'
        df['Total Installments'] = (df['End Year'] - df['Start Year']) / (df['Payment Period'] / 12)
        df['Total Payable amount'] = df['Total Installments'] * df['Premium Amount']

        if os.path.exists(csv_file):
            # Load existing CSV
            df_existing = pd.read_csv(csv_file)

            # Concatenate the new data with existing data
            df_combined = pd.concat([df_existing, df], ignore_index=True)

            # Write the combined DataFrame back to the CSV
            df_combined.to_csv(csv_file, index=False)
        else:
            # If CSV does not exist, write the new DataFrame directly
            df.to_csv(csv_file, index=False)
        self.manager.current='main'

    def clear_inputs(self):
        self.policy_number=""
        self.end_year=""
        self.start_year=""
        self.start_month=""
        self.prem_amount=""
        self.latest_payment_date=""
        self.payment_peroid=""
    def go_back(self,instance):
        self.clear_inputs()
        self.manager.current='main'

    def on_pre_enter(self, *args):
        # Reset the UI when the screen is about to be displayed
        self.layout.clear_widgets()  # Clear any existing widgets
        self.load_ui()  # Reload the UI


