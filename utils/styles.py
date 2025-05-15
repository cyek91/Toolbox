"""
样式定义 - 包含应用程序的所有CSS样式，采用Windows 11风格的纯暗色主题
"""


from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

class Styles:
    """应用程序样式类"""
    
    @staticmethod
    def add_shadow_effect(widget, radius=5, color="#40000000"):
        """为控件添加阴影效果"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(radius)
        shadow.setColor(QColor(color))
        shadow.setOffset(2, 2)
        widget.setGraphicsEffect(shadow)
    
    # Windows 11 暗色主题颜色
    BG_DARK = "#202020"         # 主背景色
    BG_DARKER = "#171717"       # 更深的背景色
    BG_MEDIUM = "#2D2D30"       # 控件背景色
    BG_LIGHT = "#3E3E42"        # 高亮背景色
    FG_NORMAL = "#E0E0E0"       # 正常文本颜色
    FG_DIMMED = "#9D9D9D"       # 暗淡文本颜色
    ACCENT_COLOR = "#60CDFF"    # Win11风格的强调色
    HOVER_COLOR = "#2A2A2A"     # 悬停颜色
    ERROR_COLOR = "#FF5252"     # 错误/删除颜色
    BORDER_RADIUS = "5px"       # 控件圆角
    
    # 主窗口样式
    MAIN_WINDOW = f"""
        QMainWindow {{
            background-color: {BG_DARKER};
            color: {FG_NORMAL};
        }}
    """
    
    # 标题栏样式
    TITLE_BAR = f"""
        QWidget#titleBar {{
            background-color: {BG_DARKER};
            border-bottom: 1px solid #333333;
        }}
        QLabel#titleLabel {{
            color: {FG_NORMAL};
            font-size: 14px;
            font-weight: bold;
        }}
        QPushButton#closeButton {{
            border: none;
            background-color: #E74C3C;
            min-width: 12px;
            min-height: 12px;
            max-width: 12px;
            max-height: 12px;
            border-radius: 6px;
        }}
        QPushButton#minimizeButton {{
            border: none;
            background-color: #F1C40F;
            min-width: 12px;
            min-height: 12px;
            max-width: 12px;
            max-height: 12px;
            border-radius: 6px;
        }}
        QPushButton#maximizeButton {{
            border: none;
            background-color: #2ECC71;
            min-width: 12px;
            min-height: 12px;
            max-width: 12px;
            max-height: 12px;
            border-radius: 6px;
        }}
        QPushButton#closeButton:hover {{
            background-color: #FF6C5A;
        }}
        QPushButton#minimizeButton:hover {{
            background-color: #FFD95A;
        }}
        QPushButton#maximizeButton:hover {{
            background-color: #5ADE8B;
        }}
        QPushButton#closeButton:pressed {{
            background-color: #C0392B;
        }}
        QPushButton#minimizeButton:pressed {{
            background-color: #D4AC0D;
        }}
        QPushButton#maximizeButton:pressed {{
            background-color: #27AE60;
        }}
    """
    
    # 左侧面板样式
    LEFT_PANEL = f"""
        QWidget#leftPanel {{
            background-color: {BG_DARKER};
        }}
        QListWidget {{
            background-color: {BG_DARKER};
            border: none;
            color: {FG_NORMAL};
            border-radius: 0px;
            outline: none;
            padding: 5px;
        }}
        QListWidget::item {{
            padding: 10px 15px;
            margin: 2px 5px;
            border-radius: {BORDER_RADIUS};
        }}
        QListWidget::item:selected {{
            background-color: {BG_MEDIUM};
            color: {FG_NORMAL};
            border-left: 2px solid {ACCENT_COLOR};
        }}
        QListWidget::item:hover {{
            background-color: {HOVER_COLOR};
        }}
        QLineEdit#searchBox {{
            border: 1px solid #333333;
            border-radius: {BORDER_RADIUS};
            padding: 8px;
            background-color: {BG_MEDIUM};
            color: {FG_NORMAL};
            selection-background-color: {ACCENT_COLOR};
            margin: 5px 15px;
        }}
        QLineEdit#searchBox:focus {{
            border: 1px solid {ACCENT_COLOR};
        }}
        QPushButton#addButton {{
            background-color: {ACCENT_COLOR};
            color: {BG_DARKER};
            border: none;
            border-radius: {BORDER_RADIUS};
            padding: 10px;
            font-size: 13px;
            font-weight: bold;
            margin: 5px 15px;
        }}
        QPushButton#addButton:hover {{
            background-color: #70D7FF;
        }}
        QPushButton#addButton:pressed {{
            background-color: #50BDFF;
        }}
    """
    
    # 右侧面板样式
    RIGHT_PANEL = f"""
        QStackedWidget#rightPanel {{
            background-color: {BG_DARK};
        }}
        QScrollArea {{
            background-color: {BG_DARK};
            border: none;
        }}
        QLabel {{
            color: {FG_NORMAL};
        }}
        QScrollBar:vertical {{
            border: none;
            background: {BG_DARKER};
            width: 10px;
            margin: 0px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical {{
            background: #555555;
            min-height: 30px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: #666666;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
    """
    
    # 工具按钮统一样式
    TOOL_BUTTON = f"""
        QPushButton {{
            background-color: {BG_MEDIUM};
            color: {FG_NORMAL};
            border: none;
            border-radius: {BORDER_RADIUS};
            font-size: 14px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
        }}
        QPushButton:hover {{
            background-color: {BG_LIGHT};
        }}
        QPushButton:pressed {{
            background-color: {BG_DARKER};
        }}
    """
    
    # 工具对话框样式
    TOOL_DIALOG = f"""
        QDialog {{
            background-color: {BG_DARK};
            color: {FG_NORMAL};
        }}
        QLabel {{
            color: {FG_NORMAL};
            background-color: transparent;
        }}
        QLineEdit {{
            border: 1px solid #333333;
            border-radius: {BORDER_RADIUS};
            padding: 10px;
            background-color: {BG_MEDIUM};
            color: {FG_NORMAL};
            selection-background-color: {ACCENT_COLOR};
        }}
        QLineEdit:focus {{
            border: 1px solid {ACCENT_COLOR};
        }}
        QComboBox {{
            border: 1px solid #333333;
            border-radius: {BORDER_RADIUS};
            padding: 10px;
            background-color: {BG_MEDIUM};
            color: {FG_NORMAL};
        }}
        QComboBox:focus {{
            border: 1px solid {ACCENT_COLOR};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {BG_MEDIUM};
            color: {FG_NORMAL};
            selection-background-color: {BG_LIGHT};
            selection-color: {FG_NORMAL};
            border: 1px solid #333333;
            border-radius: {BORDER_RADIUS};
        }}
        QPushButton {{
            background-color: {BG_MEDIUM};
            color: {FG_NORMAL};
            border: none;
            border-radius: {BORDER_RADIUS};
            padding: 10px;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {BG_LIGHT};
        }}
        QPushButton:pressed {{
            background-color: {BG_DARKER};
        }}
        QDialogButtonBox > QPushButton {{
            min-width: 80px;
        }}
        QDialogButtonBox > QPushButton[text="OK"] {{
            background-color: {ACCENT_COLOR};
            color: {BG_DARKER};
            font-weight: bold;
        }}
        QDialogButtonBox > QPushButton[text="OK"]:hover {{
            background-color: #70D7FF;
        }}
        QDialogButtonBox > QPushButton[text="OK"]:pressed {{
            background-color: #50BDFF;
        }}
        
        QDialogButtonBox > QPushButton[text="Cancel"] {{
            background-color: #555555;
            color: {FG_NORMAL};
        }}
        QDialogButtonBox > QPushButton[text="Cancel"]:hover {{
            background-color: #666666;
        }}
    """
    
    # 菜单样式
    MENU_STYLE = f"""
        QMenu {{
            background-color: {BG_MEDIUM};
            color: {FG_NORMAL};
            border: 1px solid #333333;
            border-radius: {BORDER_RADIUS};
            padding: 5px;
        }}
        QMenu::item {{
            padding: 8px 25px 8px 20px;
            border-radius: {BORDER_RADIUS};
        }}
        QMenu::item:selected {{
            background-color: {BG_LIGHT};
            color: {FG_NORMAL};
        }}
        QMenu::separator {{
            height: 1px;
            background-color: #333333;
            margin: 5px 15px;
        }}
    """
    
    @classmethod
    def get_tool_button_style(cls, tool_type: str) -> str:
        """
        根据工具类型获取按钮样式
        
        Args:
            tool_type: 工具类型
            
        Returns:
            对应的按钮样式
        """
        if tool_type == "url":
            return cls.TOOL_BUTTON_URL
        elif tool_type == "java":
            return cls.TOOL_BUTTON_JAVA
        elif tool_type == "python":
            return cls.TOOL_BUTTON_PYTHON
        elif tool_type == "gui":
            return cls.TOOL_BUTTON_GUI
        elif tool_type == "terminal":
            return cls.TOOL_BUTTON_TERMINAL
        else:
            return cls.TOOL_BUTTON_BASE 