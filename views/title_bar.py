"""
自定义标题栏 - 实现无边框窗口的标题栏
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

from utils.styles import Styles


class TitleBar(QWidget):
    """自定义标题栏类"""
    
    # 自定义信号
    minimize_clicked = pyqtSignal()
    maximize_clicked = pyqtSignal()
    close_clicked = pyqtSignal()
    
    def __init__(self, title: str = "渗透测试工具箱", parent=None):
        """
        初始化标题栏
        
        Args:
            title: 标题文本
            parent: 父控件
        """
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setStyleSheet(Styles.TITLE_BAR)
        self.setFixedHeight(32)
        
        # 水平布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(8)
        
        # 创建三个macOS风格的按钮
        self.close_button = QPushButton()
        self.close_button.setObjectName("closeButton")
        self.close_button.setToolTip("关闭")
        self.close_button.clicked.connect(self.close_clicked.emit)
        layout.addWidget(self.close_button)
        
        self.minimize_button = QPushButton()
        self.minimize_button.setObjectName("minimizeButton")
        self.minimize_button.setToolTip("最小化")
        self.minimize_button.clicked.connect(self.minimize_clicked.emit)
        layout.addWidget(self.minimize_button)
        
        self.maximize_button = QPushButton()
        self.maximize_button.setObjectName("maximizeButton")
        self.maximize_button.setToolTip("最大化")
        self.maximize_button.clicked.connect(self.maximize_clicked.emit)
        layout.addWidget(self.maximize_button)
        
        # 添加一些间距
        layout.addSpacing(8)
        
        # 添加标题标签
        self.title_label = QLabel(title)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label, 1)  # 1是拉伸因子
    
    def update_maximize_button(self, is_maximized: bool):
        """
        更新最大化按钮图标 (在macOS风格下不需要改变外观)
        
        Args:
            is_maximized: 是否最大化
        """
        # macOS风格下不需要改变按钮外观
        pass
    
    def mouseDoubleClickEvent(self, event):
        """
        鼠标双击事件处理 - 最大化/还原窗口
        
        Args:
            event: 鼠标事件
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.maximize_clicked.emit()
        super().mouseDoubleClickEvent(event) 