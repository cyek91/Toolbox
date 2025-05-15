"""
UI工具类 - 封装UI相关的重复逻辑
"""
from typing import Dict, Any, List
from PyQt6.QtWidgets import (QScrollArea, QWidget, QVBoxLayout, QGridLayout,
                           QLabel, QMenu, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QAction

from views.tool_button import ToolButton
from utils.styles import Styles


class PageCreator:
    """页面创建工具类"""

    @staticmethod
    def create_scroll_page(title: str) -> QScrollArea:
        """
        创建滚动页面

        Args:
            title: 页面标题

        Returns:
            滚动页面控件
        """
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet(f"background-color: {Styles.BG_DARK};")

        # 创建内容控件
        content_widget = QWidget()
        content_widget.setStyleSheet(f"background-color: {Styles.BG_DARK};")
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # 添加标题
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Styles.FG_NORMAL};")
        layout.addWidget(title_label)

        # 设置内容
        scroll_area.setWidget(content_widget)
        return scroll_area


class ToolGridManager:
    """工具网格管理类"""

    def __init__(self, grid_layout: QGridLayout):
        """
        初始化

        Args:
            grid_layout: 网格布局对象
        """
        self.grid = grid_layout
        self.buttons_per_row = 3

    def set_buttons_per_row(self, count: int):
        """
        设置每行按钮数量

        Args:
            count: 按钮数量
        """
        self.buttons_per_row = max(1, count)

    def clear_grid(self):
        """清空网格"""
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_tool_buttons(self, tools: List[Dict[str, Any]],
                        click_handler, right_click_handler):
        """
        添加工具按钮到网格

        Args:
            tools: 工具数据列表
            click_handler: 点击处理函数
            right_click_handler: 右键点击处理函数
        """
        self.clear_grid()

        row, col = 0, 0
        for tool in tools:
            # 创建工具按钮
            tool_button = ToolButton(tool.get("name", ""), tool)
            tool_button.clicked.connect(lambda checked, t=tool: click_handler(t))
            tool_button.right_clicked.connect(
                lambda event, t=tool: right_click_handler(event, t))

            # 添加到网格布局
            self.grid.addWidget(tool_button, row, col)

            # 更新行列索引
            col += 1
            if col >= self.buttons_per_row:
                col = 0
                row += 1


class ContextMenuManager:
    """上下文菜单管理类"""

    @staticmethod
    def create_tool_menu(parent, actions: List[Dict[str, Any]]) -> QMenu:
        """
        创建工具右键菜单

        Args:
            parent: 父控件
            actions: 菜单动作列表，格式为[{"text": str, "handler": callable}]

        Returns:
            菜单对象
        """
        menu = QMenu(parent)
        menu.setStyleSheet(Styles.MENU_STYLE)

        for action_data in actions:
            action = QAction(action_data["text"], parent)
            action.triggered.connect(action_data["handler"])
            menu.addAction(action)

        return menu

    @staticmethod
    def show_tool_menu_at_cursor(menu: QMenu):
        """在光标位置显示菜单"""
        menu.exec(QCursor.pos())
