from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from database import add_product, get_products, delete_product


class ProductsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("مدیریت محصولات")
        self.resize(800, 600)

        layout = QVBoxLayout()

        title = QLabel("مدیریت محصولات جیلیز")
        title.setStyleSheet("font-size:20px;font-weight:bold;")
        layout.addWidget(title)

        self.name = QLineEdit()
        self.name.setPlaceholderText("نام محصول")
        layout.addWidget(self.name)

        self.category = QComboBox()
        self.category.addItems([
            "برگر",
            "پیتزا",
            "سوخاری",
            "سیب زمینی",
            "نوشیدنی",
            "سس"
        ])
        layout.addWidget(self.category)

        self.price = QLineEdit()
        self.price.setPlaceholderText("قیمت")
        layout.addWidget(self.price)

        btn_layout = QHBoxLayout()

        self.save_btn = QPushButton("ذخیره محصول")
        self.delete_btn = QPushButton("حذف محصول")

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.delete_btn)

        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "شناسه",
            "نام محصول",
            "دسته",
            "قیمت"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.save_btn.clicked.connect(self.save_product)
        self.delete_btn.clicked.connect(self.remove_product)

        self.load_products()

    def load_products(self):
        self.table.setRowCount(0)

        products = get_products()

        for row_number, product in enumerate(products):
            self.table.insertRow(row_number)

            for column_number, data in enumerate(product):
                self.table.setItem(
                    row_number,
                    column_number,
                    QTableWidgetItem(str(data))
                )

    def save_product(self):
        name = self.name.text().strip()
        category = self.category.currentText()
        price = self.price.text().strip()

        if not name or not price:
            QMessageBox.warning(self, "خطا", "نام محصول و قیمت را وارد کنید.")
            return

        try:
            price = int(price)
        except ValueError:
            QMessageBox.warning(self, "خطا", "قیمت باید عدد باشد.")
            return

        add_product(name, category, price)

        self.name.clear()
        self.price.clear()

        self.load_products()

        QMessageBox.information(self, "موفق", "محصول ذخیره شد.")

    def remove_product(self):
        row = self.table.currentRow()

        if row == -1:
            QMessageBox.warning(self, "خطا", "ابتدا یک محصول را انتخاب کنید.")
            return

        product_id = int(self.table.item(row, 0).text())

        delete_product(product_id)

        self.load_products()

        QMessageBox.information(self, "موفق", "محصول حذف شد.")