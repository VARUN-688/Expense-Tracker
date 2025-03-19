from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import pandas as pd
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from datetime import datetime, timedelta
from kivy.graphics import Rectangle


class ExpenseDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load transaction data
        self.df = pd.read_csv("transactions.csv")
        self.df["Date"] = pd.to_datetime(self.df["Date"])

        # Background Image
        with self.canvas.before:
            self.bg = Rectangle(source="background.png", pos=self.pos, size=self.size)
        self.bind(size=self.update_bg)

        # Main Layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header Layout
        header = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        header.add_widget(Label(text="Expense Dashboard", font_size=30, bold=True, color=(1, 1, 1, 1)))

        # Filters Layout
        filters = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)

        banks = ["All"] + list(self.df["Bank"].dropna().unique())
        types = ["All"] + list(self.df["Type"].dropna().unique())  # Credit / Debit
        categories = ["All"] + list(self.df["Category"].dropna().unique())
        branches = ["All"] + list(self.df["Branch"].dropna().unique())

        self.bank_spinner = Spinner(text="All", values=banks)
        self.type_spinner = Spinner(text="All", values=types)
        self.category_spinner = Spinner(text="All", values=categories)
        self.branch_spinner = Spinner(text="All", values=branches)

        filters.add_widget(Label(text="Bank:"))
        filters.add_widget(self.bank_spinner)
        filters.add_widget(Label(text="Type:"))
        filters.add_widget(self.type_spinner)
        filters.add_widget(Label(text="Category:"))
        filters.add_widget(self.category_spinner)
        filters.add_widget(Label(text="Branch:"))
        filters.add_widget(self.branch_spinner)

        # Apply Filters Button
        self.apply_button = Button(
            text="Apply Filters",
            size_hint=(None, None),
            size=(200, 50),
            background_color=(0, 0.6, 1, 1)  # Blue
        )
        self.apply_button.bind(on_press=self.apply_filters)

        # Summary Layout
        summary_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=100)

        self.total_label = Label(text="Total Transactions: 0", font_size=18, bold=True)
        self.credit_label = Label(text="Total Credit: 0", font_size=18, bold=True)
        self.debit_label = Label(text="Total Debit: 0", font_size=18, bold=True)
        self.bank_label = Label(text="Most Used Bank: N/A", font_size=18, bold=True)

        summary_layout.add_widget(self.total_label)
        summary_layout.add_widget(self.credit_label)
        summary_layout.add_widget(self.debit_label)
        summary_layout.add_widget(self.bank_label)

        # Charts Grid Layout (2 Rows, 2 Columns)
        self.chart_grid = GridLayout(cols=2, rows=2, spacing=10)

        # Initial Charts
        self.pie_chart1 = self.create_pie_chart(self.df, "Category", "Expense Breakdown")
        self.bar_chart1 = self.create_bar_chart(self.df, "Bank", "Bank-wise Expense")
        self.pie_chart2 = self.create_pie_chart(self.df, "Type", "Credit vs Debit Breakdown")
        self.bar_chart2 = self.create_bar_chart(self.df, "Branch", "Branch-wise Expense")

        self.chart_grid.add_widget(self.pie_chart1)
        self.chart_grid.add_widget(self.bar_chart1)
        self.chart_grid.add_widget(self.pie_chart2)
        self.chart_grid.add_widget(self.bar_chart2)

        # Back Button
        back_button = Button(text="Back", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.go_back)

        # Add widgets to main layout
        layout.add_widget(header)
        layout.add_widget(filters)
        layout.add_widget(self.apply_button)  # Apply Filters Button
        layout.add_widget(summary_layout)
        layout.add_widget(self.chart_grid)  # Grid Layout for Charts
        layout.add_widget(back_button)

        self.add_widget(layout)

    def update_bg(self, *args):
        """ Update background image when window resizes """
        self.bg.pos = self.pos
        self.bg.size = self.size

    def apply_filters(self, *args):
        """ Apply filters only when 'Apply Filters' button is clicked """
        filtered_df = self.df.copy()

        # Apply Bank Filter
        if self.bank_spinner.text != "All":
            filtered_df = filtered_df[filtered_df["Bank"] == self.bank_spinner.text]

        # Apply Type Filter
        if self.type_spinner.text != "All":
            filtered_df = filtered_df[filtered_df["Type"] == self.type_spinner.text]

        # Apply Category Filter
        if self.category_spinner.text != "All":
            filtered_df = filtered_df[filtered_df["Category"] == self.category_spinner.text]

        # Apply Branch Filter
        if self.branch_spinner.text != "All":
            filtered_df = filtered_df[filtered_df["Branch"] == self.branch_spinner.text]

        # Update Summary Values
        self.total_label.text = f"Total Transactions: {len(filtered_df)}"
        self.credit_label.text = f"Total Credit: {filtered_df[filtered_df['Type'] == 'Credit']['Amount'].sum():.2f}"
        self.debit_label.text = f"Total Debit: {filtered_df[filtered_df['Type'] == 'Debit']['Amount'].sum():.2f}"
        self.bank_label.text = f"Most Used Bank: {filtered_df['Bank'].mode()[0] if not filtered_df.empty else 'N/A'}"

        # Update Graphs
        self.update_graphs(filtered_df)

    def update_graphs(self, df):
        """ Update all charts inside the 2x2 grid layout """
        self.chart_grid.clear_widgets()  # Clear previous charts

        self.pie_chart1 = self.create_pie_chart(df, "Category", "Expense Breakdown")
        self.bar_chart1 = self.create_bar_chart(df, "Bank", "Bank-wise Expense")
        self.pie_chart2 = self.create_pie_chart(df, "Type", "Credit vs Debit Breakdown")
        self.bar_chart2 = self.create_bar_chart(df, "Branch", "Branch-wise Expense")

        self.chart_grid.add_widget(self.pie_chart1)
        self.chart_grid.add_widget(self.bar_chart1)
        self.chart_grid.add_widget(self.pie_chart2)
        self.chart_grid.add_widget(self.bar_chart2)

    def create_pie_chart(self, df, column, title):
        """ Generate Pie Chart for given column """
        if df.empty or column not in df.columns:
            return Label(text=f"No data for {title}", font_size=18, color=(1, 0, 0, 1))

        fig, ax = plt.subplots()
        df[column].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_title(title)
        return FigureCanvasKivyAgg(fig)

    def create_bar_chart(self, df, column, title):
        """ Generate Bar Chart for given column """
        if df.empty or column not in df.columns:
            return Label(text=f"No data for {title}", font_size=18, color=(1, 0, 0, 1))

        fig, ax = plt.subplots()
        df.groupby(column)["Amount"].sum().plot(kind="bar", ax=ax)
        ax.set_title(title)
        return FigureCanvasKivyAgg(fig)

    def go_back(self, instance):
        """ Navigate back """
        self.manager.current = "main"
