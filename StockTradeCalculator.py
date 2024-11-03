# Student: Ganom Mbochi
# Student ID: 3082898
# Date: 2024-10-29

import csv
import sys
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox, QDoubleSpinBox, QMessageBox
from PyQt6 import QtGui
from datetime import datetime
from decimal import Decimal


class StockTradeProfitCalculator(QDialog):
    

    def __init__(self):

        super().__init__()

        # setting up dictionary of Stocks
        self.profit = None
        self.sTotal = None
        self.pTotal = None
        self.data = self.make_data()

 #sorting the dictionary of the stocks 
        self.stock = sorted(self.data.keys())

        self.dates = sorted(self.data.keys())
        
        # Check if 'Amazon' exists, if not, handle it gracefully
        if 'Amazon' in self.data:
            self.sellCalendarDefaultDate = sorted(self.data['Amazon'].keys())[-1]
            sell_date_qdate = self.tuple_to_qdate(self.sellCalendarDefaultDate)
            print("the close price for amazon is",sell_date_qdate.toString(), self.data['Amazon'][self.sellCalendarDefaultDate])

        else:
            print("----------------------------------")
            print("Amazon not found in the dataset. Available stocks:", self.data.keys())
            self.sellCalendarDefaultDate = QDate.currentDate()  # Default to the current date


       
       
       
        #self.sellCalendarDefaultDate = sorted(self.data['Amazon'].keys())[-1]
        print("self.sellCalendarDefaultDate", self.sellCalendarDefaultDate)

        #displaying widow to center of the screen
        self.center()

        #setting the window title
        self.setWindowTitle("Stock Trade Profit Calculator")

        #adding the layout to the window
        self.setWindowIcon(QtGui.QIcon(''))

        #setting the layout to grid
        grid = QGridLayout()
        #setting spacing to 15
        grid.setSpacing(15)

        #selecting the stock
        stockLabel = QLabel("Select Stock")

        #creating a combo box and adding the cryto to the combo boxfrom the csv file
        self.stockCombo = QComboBox()
        self.stockCombo.addItems(self.stock)

        #positioning the stock label and combo box
        grid.addWidget(stockLabel, 0, 0)
        grid.addWidget(self.stockCombo, 0, 1, 1, 2)

        #LAbe for quantity purchased
        self.amount = QLabel("Quantity Purchased")

        #creating a spin box for the quantity purchased
        self.quantitySelector = QDoubleSpinBox(self)
        self.quantitySelector.setRange(0.01, 100000000.00)
        self.quantitySelector.setValue(1.00000)

        #positioning the quantity label and spin box
        grid.addWidget(self.amount, 1, 0)
        grid.addWidget(self.quantitySelector, 1, 1, 1, 2)

        #adding the calendar for the purchase and selltotal
        self.Purchase = QLabel("Purchase Date")

        #QCalendarWidget for the purchase dateis created
        self.calendar1 = QCalendarWidget(self)
        self.calendar1.setGridVisible(True)

        #sell date lbel
        self.Sell = QLabel("Sell Date")

        #QCalendarWidget for the sell date is created
        self.calendar2 = QCalendarWidget(self)
        self.calendar2.setGridVisible(True)

        #data range
        minDate = QDate(2020, 2, 2)
        maxDate = QDate(2024, 2, 1)

        self.calendar1.setDateRange(minDate, maxDate)
        self.calendar2.setDateRange(minDate, maxDate)

        #assigning the  selected date to the calendar
        self.selected_date1= self.calendar1.selectedDate()
        self.selected_date2 = self.calendar2.selectedDate()

        #label for the purchase total
        self.purchaseTotalLabel = QLabel("Purchase Total")
        #empty label for the purchase total
        self.purchaseTotal = QLabel("")
        
        #label for the sell total
        self.sellTotalLabel = QLabel("Sell Total")
        #empty label for the sell total
        self.sellTotal = QLabel("")

        #label for the profit total
        self.profitTotalLabel= QLabel("Profit Total")
        #empty label for the profit total
        self.profitTotal = QLabel("")   

        self.messageLabel = QLabel("Message")
        self.Pmessage = QLabel("")

        # positioning the calendar widget
        grid.addWidget(self.Purchase, 2, 0)  # positioning the purchase calendar  label
        grid.addWidget(self.calendar1, 2, 1)  # positioning the  purchase calendar widget

        grid.addWidget(self.purchaseTotalLabel, 3, 0)  # positioning the purchase total  label

        grid.addWidget(self.purchaseTotal, 3, 1)  # positioning the purchase total

        grid.addWidget(self.Sell, 2, 2)  # positioning the sel calendar the label
        grid.addWidget(self.calendar2, 2, 3)  # positioning the sell calendar  widget

        grid.addWidget(self.sellTotalLabel, 4, 0)  # positioning the sell total  label
        grid.addWidget(self.sellTotal, 4, 1)  # positioning the sell total

        grid.addWidget(self.profitTotalLabel, 5, 0)  # positioning the profit total  label
        grid.addWidget(self.profitTotal, 5, 1)  # positioning the profit total

        grid.addWidget(self.Pmessage, 6, 3, 1, 6)  # positioning the message

        self.setLayout(grid)  # setting layout to grid

       #connecting the signals to the updateUi
        self.stockCombo.currentIndexChanged.connect(self.updateUi)
        self.quantitySelector.valueChanged.connect(self.updateUi)
        self.calendar1.clicked[QDate].connect(self.updateUi)
        self.calendar2.clicked[QDate].connect(self.updateUi)

        self.resize(550, 450)  # resizing the window



    def updateUi(self):
        '''
        This requires substantial development.
        Updates the UI when control values are changed; should also be called when the app initializes.
        '''
        try:
            print("Updating UI...")

            # Get the selected stock
            selected_stock = self.stockCombo.currentText().strip()

            # Convert selected dates from QDate to tuples
            selected_date1_tuple = (self.calendar1.selectedDate().year(), self.calendar1.selectedDate().month(), self.calendar1.selectedDate().day())
            selected_date2_tuple = (self.calendar2.selectedDate().year(), self.calendar2.selectedDate().month(), self.calendar2.selectedDate().day())

            # Perform calculations
            purchase_total = round(self.data[selected_stock][selected_date1_tuple] * self.quantitySelector.value(), 2)
            sell_total = round(self.data[selected_stock][selected_date2_tuple] * self.quantitySelector.value(), 2)
            profit = round(sell_total - purchase_total, 2)

            # Print the results for debugging
            print(f"Purchase Total: {purchase_total}")
            print(f"Sell Total: {sell_total}")
            print(f"Profit: {profit}")

            # Update the UI elements with the calculated values
            self.purchaseTotal.setText(f"{purchase_total}")
            self.sellTotal.setText(f" {sell_total}")
            self.profitTotal.setText(f"{profit}")

            # Extra
            if profit < 0:
                self.Pmessage.setText("Please select a valid date")
            else:
                self.Pmessage.setText(f"Congratulations! You have made a profit of {profit}")

        except Exception as e:
            print(f"Error in updateUi: {e}")

    def make_data(self):
        '''
        This code reads the stock market CSV file and generates a dictionary structure.
        :return: a dictionary of dictionaries
        '''
        data = {}
        try:
            with open('Transformed_Stock_Market_Dataset.csv', mode='r') as file:
                reader = csv.DictReader(file)
                stock_names = reader.fieldnames[1:]  # All columns except 'Date' are stock names

                for row in reader:
                    date_string = row['Date']
                    date_tuple = self.string_date_into_tuple(date_string)

                    for stock in stock_names:
                        price = row[stock].replace(',', '')
                        try:
                            price = float(price)
                        except ValueError:
                            price = 0.0

                        if stock not in data:
                            data[stock] = {}

                        data[stock][date_tuple] = price

            print("Data loaded successfully.")
            print(f"Stocks available: {stock_names}")  # Debugging: Print all available stock names

        except Exception as e:
            print(f"Error reading data: {e}")
        return data

    def string_date_into_tuple(self, date_string):
        '''
        Converts a date in string format (e.g., "2024-02-02") into a tuple (year, month, day).
        :return: tuple representing the date
        '''
        try:
            if '-' in date_string:
                date_obj = datetime.strptime(date_string, "%d-%m-%Y")
            else:
                date_obj = datetime.strptime(date_string, "%m/%d/%Y")
            return date_obj.year, date_obj.month, date_obj.day
        except ValueError:
            print(f"Error parsing date: {date_string}")
            return None

    def tuple_to_qdate(self, date_tuple):
        '''
        Converts a date tuple (year, month, day) into a QDate object.
        :return: QDate object
        '''
        return QDate(date_tuple[0], date_tuple[1], date_tuple[2])
    
    def unique(self, non_unique_list):
        '''
        This method is complete
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        '''
        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list

# Function that centers the window
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # EXTRA FEATURE 1
        # Added dialog when trying to quit the app

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:

            event.accept()
        else:

            event.ignore()

# This is complete
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
                QWidget{
                    background: #322F2F ;
                }
                
                QComboBox{
                    border: 1px solid ;
                    padding: 5px;
                    border-radius: 8px;
                    background: #1e81b0;
                }
                QDoubleSpinBox{
                    border: 1px solid ;
                    padding: 5px;
                    border-radius: 8px;
                    background: #1e81b0;
                }
                
                QLabel#purchaseTotal{
                    border: 1px solid ;
                    border-radius: 8px;
                    
                }
                QLabel{
                font-style: normal;
                font-size: 10pt;
                font-weight: Medium;
                }
                
                QCalendarWidget QAbstractItemView
                { 
                    selection-background-color: #042944; 
                    selection-color: white;
                }
                QCalendarWidget QWidget 
                {
                  color:grey;
                }
                QCalendarWidget QTableView
                {
                    border-width:0px;
                    background-color:#f8f8ff;
                }
                
               
                
            """
    
    )
    stock_calculator = StockTradeProfitCalculator()
    stock_calculator.show()
    sys.exit(app.exec())
