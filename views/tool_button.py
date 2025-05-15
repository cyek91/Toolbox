"""
自定义工具按钮 - 支持右键菜单
"""
from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent

from utils.styles import Styles


class ToolButton(QPushButton):
    """自定义工具按钮，支持右键菜单"""
    
    # 右键点击信号
    right_clicked = pyqtSignal(object)
    
    def __init__(self, text: str, tool_data: dict, parent=None):
        """
        初始化工具按钮
        
        Args:
            text: 按钮文本
            tool_data: 工具数据
            parent: 父控件
        """
        super().__init__(text, parent)
        self.tool_data = tool_data
        
        # 设置固定大小
        self.setFixedSize(180, 70)
        
        # 使用统一样式
        self.setStyleSheet(Styles.TOOL_BUTTON)
        Styles.add_shadow_effect(self)
    
    def mousePressEvent(self, event: QMouseEvent):
        """
        鼠标按下事件处理
        
        Args:
            event: 鼠标事件
        """
        if event.button() == Qt.MouseButton.RightButton:
            # 发射右键点击信号
            self.right_clicked.emit(event)
        else:
            # 默认处理
            super().mousePressEvent(event) 