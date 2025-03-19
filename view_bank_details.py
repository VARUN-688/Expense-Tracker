import pandas as pd
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class ViewBankDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewBankDetailsScreen, self).__init__(**kwargs)
        self.load_bank_details()

    def load_bank_details(self):
        # Clear any existing widgets
        self.clear_widgets()

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        csv_file = 'bank_details.csv'
        if os.path.exists(csv_file):
            # Load the CSV file
            df = pd.read_csv(csv_file)

            # If there are no bank details, show a message
            if df.empty:
                self.layout.add_widget(Label(text="No bank details available."))
            else:
                # Display each row of the DataFrame with a delete button
                for index, row in df.loc[df["User"]==open('current_user.txt','r').read()].iterrows():
                    row_layout = BoxLayout(orientation='horizontal', spacing=10)

                    # Display bank name, branch, balance, and last 4 digits
                    bank_detail_label = Label(
                        text=f"Name:-                           {row['Bank Name']}\nBranch:-                         {row['Branch Name']}\nBalance:-                       {row['Balance']}\nAccount Number:-      {row['Account Number']}",
                        size_hint=(0.8, 1)
                    )
                    row_layout.add_widget(bank_detail_label)

                    # Add a delete button
                    delete_button = Button(text="Delete", size_hint=(0.2, 1))
                    delete_button.bind(on_press=lambda instance, idx=index: self.confirm_delete(idx))
                    row_layout.add_widget(delete_button)

                    self.layout.add_widget(row_layout)

        else:
            self.layout.add_widget(Label(text="No bank details available."))

        # Back button to return to the main screen
        back_button = Button(text="Back to Main Menu", size_hint=(1, 0.2))
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def confirm_delete(self, idx):
        # Create a confirmation popup before deleting
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Are you sure you want to delete this bank detail?"))

        # Yes/No buttons
        yes_button = Button(text="Yes", size_hint=(1, 0.3))
        no_button = Button(text="No", size_hint=(1, 0.3))

        content.add_widget(yes_button)
        content.add_widget(no_button)

        popup = Popup(title='Confirm Deletion', content=content, size_hint=(0.8, 0.4))

        # Bind yes button to deletion
        yes_button.bind(on_press=lambda instance: self.delete_bank_detail(idx, popup))
        # Close popup if 'No' is pressed
        no_button.bind(on_press=popup.dismiss)

        popup.open()

    def delete_bank_detail(self, idx, popup):
        csv_file = 'bank_details.csv'
        if os.path.exists(csv_file):
            # Load the CSV file
            df = pd.read_csv(csv_file)

            # Drop the row with the specified index
            df = df.drop(idx)

            # Save the updated DataFrame back to the CSV
            df.to_csv(csv_file, index=False)

        # Close the popup and refresh the bank details view
        popup.dismiss()
        self.load_bank_details()

    def go_back(self, instance):
        # Switch back to the main screen
        self.manager.current = 'main'
    def on_pre_enter(self, *args):
        # Reset the UI when the screen is about to be displayed
        self.layout.clear_widgets()  # Clear any existing widgets
        self.load_bank_details()  # Reload the UI
