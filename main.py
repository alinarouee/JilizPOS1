import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)

from PySide6.QtCore import Qt

from database import create_tables
from config import SHOP_NAME
from products import ProductsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(SHOP_NAME)
        self.resize(1200, 700)

        create_tables()

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        title = QLabel("🍔 نرم افزار صندوق جیلیز 🍟")
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:20px;
        """)
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        buttons = QHBoxLayout()

        btn_sale = QPushButton("ثبت سفارش")
        btn_products = QPushButton("محصولات")
        btn_reports = QPushButton("گزارش فروش")
        btn_exit = QPushButton("خروج")

        for btn in [btn_sale, btn_products, btn_reports, btn_exit]:
            btn.setMinimumHeight(70)
            btn.setStyleSheet("""
                font-size:18px;
            """)
            buttons.addWidget(btn)

        # اتصال دکمه‌ها
        btn_products.clicked.connect(self.open_products)
        btn_exit.clicked.connect(self.close)

        layout.addLayout(buttons)

        central.setLayout(layout)

    def open_products(self):
        self.products_window = ProductsWindow()
        self.products_window.show()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())