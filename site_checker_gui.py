import sys
import requests
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QLabel, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class SiteCheckerThread(QThread):
    finished = pyqtSignal(list)
    progress = pyqtSignal(str)

    def __init__(self, urls):
        super().__init__()
        self.urls = urls

    def check_site(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            response_time = round((time.time() - start_time) * 1000, 2)
            status = response.status_code
            return url, status, response_time, None
        except requests.RequestException as e:
            response_time = round((time.time() - start_time) * 1000, 2)
            return url, None, response_time, str(e)

    def run(self):
        results = []
        for url in self.urls:
            self.progress.emit(f"Checking {url}...")
            result = self.check_site(url)
            results.append(result)
        self.finished.emit(results)

class SiteCheckerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Site Connectivity Checker")
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URLs (comma-separated)")
        self.url_input.setMinimumWidth(400)
        url_layout.addWidget(self.url_input)

        self.check_button = QPushButton("Check Sites")
        self.check_button.clicked.connect(self.start_check)
        url_layout.addWidget(self.check_button)

        layout.addLayout(url_layout)

        self.status_label = QLabel("Ready to check sites")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["URL", "Status", "Response Time (ms)", "Error"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: #333333;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
                color: #333333;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: 1px solid #dee2e6;
                font-weight: bold;
                color: #333333;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QTableWidgetItem {
                color: #333333;
            }
        """)

    def start_check(self):
        urls = [url.strip() for url in self.url_input.text().split(',') if url.strip()]
        
        if not urls:
            QMessageBox.warning(self, "Input Error", "Please enter at least one URL")
            return

        self.table.setRowCount(0)
        self.check_button.setEnabled(False)
        self.status_label.setText("Checking sites...")

        self.checker_thread = SiteCheckerThread(urls)
        self.checker_thread.progress.connect(self.update_status)
        self.checker_thread.finished.connect(self.update_results)
        self.checker_thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def update_results(self, results):
        self.table.setRowCount(len(results))
        
        for row, (url, status, response_time, error) in enumerate(results):
            url_item = QTableWidgetItem(url)
            self.table.setItem(row, 0, url_item)

            status_item = QTableWidgetItem(str(status) if status else 'N/A')
            status_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, status_item)

            time_item = QTableWidgetItem(str(response_time))
            time_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, time_item)

            error_item = QTableWidgetItem(error if error else '')
            self.table.setItem(row, 3, error_item)

        self.status_label.setText(f"Check completed at {datetime.now().strftime('%H:%M:%S')}")
        self.check_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = SiteCheckerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 