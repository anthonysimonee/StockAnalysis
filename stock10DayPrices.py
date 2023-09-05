import pandas as pd
import sys
from tkinter import messagebox
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class StockAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Analyzer")   # Adjusts title of application
        self.setGeometry(740, 300, 1000, 500)   # Adjusts position and dimensions (x, y, width, height)

        # Create a QWidget instance to serve as the main widget
        main_widget = QWidget(self)
        
        # Set the created main_widget as the central widget of the QMainWindow
        self.setCentralWidget(main_widget)
        
        # Create a QVBoxLayout instance to serve as the main layout for the main_widget
        main_layout = QVBoxLayout()
        
        # Set the main_layout as the layout for the main_widget
        main_widget.setLayout(main_layout)


        # Initialize the user interface by calling the init_ui method
        self.init_ui()

        # Apply the Fusion theme
        app.setStyle("Fusion")                  

    def init_ui(self):
        self.ticker_label = QLabel("Enter the ticker symbol (e.g., GOOG):", self)
        self.ticker_label.setGeometry(20, 20, 250, 30)

        self.ticker_entry = QLineEdit(self)
        self.ticker_entry.setGeometry(20, 60, 150, 30)

        self.start_date_label = QLabel("Enter the starting date (YYYY-MM-DD):", self)
        self.start_date_label.setGeometry(20, 100, 250, 30)

        self.start_date_entry = QLineEdit(self)
        self.start_date_entry.setGeometry(20, 140, 150, 30)

        self.analyze_button = QPushButton("Analyze", self)
        self.analyze_button.setGeometry(20, 190, 100, 40)
        self.analyze_button.clicked.connect(self.analyze_stock)

    def analyze_stock(self):
        ticker = self.ticker_entry.text()
        starting_date = self.start_date_entry.text()

        filePath = f'./stock_data/{ticker}.csv'
        df = pd.read_csv(filePath)

        filtered_data = df[df['Date'] >= starting_date]

        start_value = filtered_data['Close'].iloc[0]
        end_value = filtered_data['Close'].iloc[-1]
        percentage_change = ((end_value - start_value) / start_value) * 100
        percentage_change_sign = '+' if percentage_change >= 0 else '-'

        highest_high = filtered_data['High'].max()
        lowest_low = filtered_data['Low'].min()

        average_closing_value = filtered_data['Close'].mean()

        twenty_four_hour_volume = filtered_data['Volume'].iloc[-1] - filtered_data['Volume'].iloc[-2]
        twenty_four_hour_high = filtered_data['High'].iloc[-1]
        twenty_four_hour_low = filtered_data['Low'].iloc[-1]

        result_message = f"""Analysis for Ticker: {ticker}
Starting Date: {starting_date}
Today's Value: ${round(end_value, 2)}
24H Volume: {twenty_four_hour_volume}
24H High: ${round(twenty_four_hour_high, 2)}
24H Low: ${round(twenty_four_hour_low, 2)}
Lowest Low: ${round(lowest_low, 2)}
Highest High: ${round(highest_high, 2)}
Percentage Change: {percentage_change_sign}{abs(round(percentage_change, 2))}%
Average Closing Value: ${round(average_closing_value, 2)}"""

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Analysis Results")
        msg_box.setText(result_message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
