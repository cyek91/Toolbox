"""
动态时钟组件 - 显示当前时间的组件
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer, QTime, QDate, Qt

from utils.styles import Styles


class ClockWidget(QWidget):
    """动态时钟组件类"""
    
    def __init__(self, parent=None):
        """
        初始化时钟组件
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.setObjectName("clockWidget")
        self.setStyleSheet(f"background-color: {Styles.BG_DARK};")
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 创建欢迎标签
        self.welcome_label = QLabel("life is a journey")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet(f"""
            color: {Styles.FG_NORMAL};
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 30px;
        """)
        layout.addWidget(self.welcome_label)
        
        # 创建时间标签
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet(f"""
            color: {Styles.ACCENT_COLOR};
            font-size: 72px;
            font-weight: bold;
            font-family: 'Segoe UI', sans-serif;
        """)
        layout.addWidget(self.time_label)
        
        # 创建日期标签
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet(f"""
            color: {Styles.FG_DIMMED};
            font-size: 24px;
            margin-top: 10px;
        """)
        layout.addWidget(self.date_label)

        
        # 创建定时器，每秒更新一次时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        # 初始化时间显示
        self.update_time()
    
    def update_time(self):
        """更新时间显示"""
        current_time = QTime.currentTime()
        time_text = current_time.toString("hh:mm:ss")
        self.time_label.setText(time_text)
        
        # 更新日期
        current_date = QDate.currentDate()
        date_text = current_date.toString("yyyy年MM月dd日 dddd")
        self.date_label.setText(date_text) 