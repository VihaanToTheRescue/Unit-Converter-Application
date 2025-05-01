import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QComboBox, QLineEdit, QPushButton, QLabel, QCompleter)
from PyQt5.QtCore import Qt

class UnitConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")
        self.setGeometry(100, 100, 600, 400)


        self.conversions = {
            'Length': {
                'Meters': 1.0,
                'Kilometers': 1000.0,
                'Centimeters': 0.01,
                'Millimeters': 0.001,
                'Micrometers': 1e-6,
                'Nanometers': 1e-9,
                'Miles': 1609.34,
                'Yards': 0.9144,
                'Feet': 0.3048,
                'Inches': 0.0254
            },
            'Weight': {
                'Kilograms': 1.0,
                'Grams': 0.001,
                'Milligrams': 1e-6,
                'Metric Tons': 1000.0,
                'Pounds': 0.453592,
                'Ounces': 0.0283495,
                'Carats': 0.0002,
                'Stones': 6.35029
            },
            'Temperature': {
                'Celsius': lambda x: x + 273.15,
                'Fahrenheit': lambda x: (x - 32) * 5/9 + 273.15,
                'Kelvin': lambda x: x
            },
            'Volume': {
                'Liters': 1.0,
                'Milliliters': 0.001,
                'Cubic Meters': 1000.0,
                'Cubic Centimeters': 0.001,
                'Gallons (US)': 3.78541,
                'Quarts (US)': 0.946353,
                'Pints (US)': 0.473176,
                'Cups (US)': 0.236588,
                'Fluid Ounces (US)': 0.0295735
            },
            'Area': {
                'Square Meters': 1.0,
                'Square Kilometers': 1e6,
                'Square Centimeters': 0.0001,
                'Square Millimeters': 1e-6,
                'Hectares': 10000.0,
                'Acres': 4046.86,
                'Square Miles': 2.58999e6,
                'Square Yards': 0.836127,
                'Square Feet': 0.092903
            },
            'Speed': {
                'Meters/Second': 1.0,
                'Kilometers/Hour': 0.277778,
                'Miles/Hour': 0.44704,
                'Knots': 0.514444
            },
            'Time': {
                'Seconds': 1.0,
                'Minutes': 60.0,
                'Hours': 3600.0,
                'Days': 86400.0,
                'Weeks': 604800.0
            },
            'Power': {
                'Watts': 1.0,
                'Kilowatts': 1000.0,
                'Horsepower': 745.7,
                'Megawatts': 1e6
            },
            'Energy': {
                'Joules': 1.0,
                'Kilojoules': 1000.0,
                'Megajoules': 1e6,
                'Watt-Hours': 3600.0,
                'Kilowatt-Hours': 3.6e6
            },
            'Pressure': {
                'Pascals': 1.0,
                'Kilopascals': 1000.0,
                'Atmospheres': 101325.0,
                'Bars': 100000.0,
                'Millibars': 100.0
            }
        }

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search categories or units...")
        main_layout.addWidget(self.search_bar)

        self.category_combo = QComboBox()
        self.category_combo.addItems(self.conversions.keys())
        main_layout.addWidget(QLabel("Select Category:"))
        main_layout.addWidget(self.category_combo)

        self.from_unit_combo = QComboBox()
        self.to_unit_combo = QComboBox()
        main_layout.addWidget(QLabel("From Unit:"))
        main_layout.addWidget(self.from_unit_combo)
        main_layout.addWidget(QLabel("To Unit:"))
        main_layout.addWidget(self.to_unit_combo)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter value")
        self.output_field = QLineEdit()
        self.output_field.setReadOnly(True)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(QLabel(" = "))
        input_layout.addWidget(self.output_field)
        main_layout.addLayout(input_layout)

        self.convert_button = QPushButton("Convert")
        main_layout.addWidget(self.convert_button)

        self.result_label = QLabel("")
        main_layout.addWidget(self.result_label)

        self.update_units()

        all_items = list(self.conversions.keys()) + [unit for category in self.conversions.values() for unit in category.keys()]
        self.completer = QCompleter(all_items)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_bar.setCompleter(self.completer)

        self.category_combo.currentTextChanged.connect(self.update_units)
        self.convert_button.clicked.connect(self.convert)
        self.search_bar.textChanged.connect(self.filter_search)
        self.input_field.textChanged.connect(self.convert)

    def update_units(self):
        category = self.category_combo.currentText()
        units = list(self.conversions[category].keys())
        self.from_unit_combo.clear()
        self.to_unit_combo.clear()
        self.from_unit_combo.addItems(units)
        self.to_unit_combo.addItems(units)

    def filter_search(self):
        search_text = self.search_bar.text().lower()
        self.category_combo.clear()
        filtered_categories = [cat for cat in self.conversions.keys() if search_text in cat.lower() or
                              any(search_text in unit.lower() for unit in self.conversions[cat].keys())]
        self.category_combo.addItems(filtered_categories if filtered_categories else self.conversions.keys())
        self.update_units()

    def convert(self):
        try:
            value = float(self.input_field.text())
            category = self.category_combo.currentText()
            from_unit = self.from_unit_combo.currentText()
            to_unit = self.to_unit_combo.currentText()

            if category == 'Temperature':
                to_kelvin = self.conversions[category][from_unit]
                from_kelvin = self.conversions[category][to_unit]
                kelvin_value = to_kelvin(value)
                if to_unit == 'Celsius':
                    result = kelvin_value - 273.15
                elif to_unit == 'Fahrenheit':
                    result = (kelvin_value - 273.15) * 9/5 + 32
                else:
                    result = kelvin_value
            else:
                from_factor = self.conversions[category][from_unit]
                to_factor = self.conversions[category][to_unit]
                result = value * from_factor / to_factor


            if result.is_integer():
                self.output_field.setText(f"{int(result)}")
            else:
                self.output_field.setText(f"{result:.6f}".rstrip('0').rstrip('.'))
            self.result_label.setText("")
        except ValueError:
            self.output_field.setText("")
            self.result_label.setText("Please enter a valid number")
        except Exception as e:
            self.output_field.setText("")
            self.result_label.setText(f"Error: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = UnitConverter()
    converter.show()
    sys.exit(app.exec_())