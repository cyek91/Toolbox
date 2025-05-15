"""
主窗口 - 应用程序的主界面
"""
from typing import Dict, Any, List, Optional
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QStackedWidget, QLabel, QPushButton, 
                             QGridLayout, QFrame, QListWidgetItem, QScrollArea,
                             QLineEdit, QMenu, QMessageBox, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QAction, QCursor

from views.title_bar import TitleBar
from views.tool_button import ToolButton
from views.clock_widget import ClockWidget
from utils.styles import Styles
from utils.ui_utils import PageCreator, ToolGridManager, ContextMenuManager
from controllers.tool_controller import ToolController
from models.config_model import ConfigModel


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__(None, Qt.WindowType.FramelessWindowHint)
        
        # 设置窗口基本属性
        self.setWindowTitle("渗透测试工具箱")
        self.setMinimumSize(960, 640)
        
        # 窗口拖动相关变量
        self.dragging = False
        self.drag_position = QPoint()
        
        # 搜索模式设置
        self.fuzzy_mode = True
        
        # 初始化模型和控制器
        self.config_model = ConfigModel()
        self.tool_controller = ToolController(self.config_model, self)
        self.tool_controller.set_on_tool_changed_callback(self.reload_tools)
        
        # 创建界面
        self.setup_ui()
        
        # 加载工具
        self.reload_tools()
        
        # 将窗口移动到屏幕中央
        self.center_window()
    
    def setup_ui(self):
        """创建界面"""
        # 设置样式
        self.setStyleSheet(Styles.MAIN_WINDOW)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建标题栏
        self.title_bar = TitleBar()
        self.title_bar.minimize_clicked.connect(self.showMinimized)
        self.title_bar.maximize_clicked.connect(self.toggle_maximize)
        self.title_bar.close_clicked.connect(self.close)
        main_layout.addWidget(self.title_bar)
        
        # 创建内容区域
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addLayout(content_layout)
        
        # 创建左侧面板
        self.left_panel = self.create_left_panel()
        content_layout.addWidget(self.left_panel, 1)
        
        # 创建右侧面板
        self.right_panel = self.create_right_panel()
        content_layout.addWidget(self.right_panel, 4)
    
    def create_left_panel(self) -> QWidget:
        """
        创建左侧面板
        
        Returns:
            左侧面板控件
        """
        left_panel = QWidget()
        left_panel.setObjectName("leftPanel")
        left_panel.setFixedWidth(250)
        left_panel.setStyleSheet(Styles.LEFT_PANEL)
        
        # 左侧面板布局
        layout = QVBoxLayout(left_panel)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)
        
        # 搜索框
        self.search_box = QLineEdit()
        self.search_box.setObjectName("searchBox")
        self.search_box.setPlaceholderText("搜索工具...")
        self.search_box.textChanged.connect(self.filter_tools)
        layout.addWidget(self.search_box)
        
        # 分类列表
        self.category_list = QListWidget()
        self.category_list.setObjectName("categoryList")
        self.category_list.currentRowChanged.connect(self.display_category)
        layout.addWidget(self.category_list)
        
        # 添加工具按钮
        self.add_button = QPushButton("添加工具")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_tool)
        layout.addWidget(self.add_button)
        
        return left_panel
    
    def create_right_panel(self) -> QStackedWidget:
        """
        创建右侧面板
        
        Returns:
            右侧面板控件
        """
        right_panel = QStackedWidget()
        right_panel.setObjectName("rightPanel")
        right_panel.setStyleSheet(Styles.RIGHT_PANEL)
        
        return right_panel
    
    def calculate_buttons_per_row(self) -> int:
        """
        计算每行显示的按钮数量
        
        Returns:
            每行按钮数量
        """
        right_panel_width = self.width() - 250  # 减去左侧面板宽度
        available_width = right_panel_width - 60  # 减去边距
        button_width = 180  # 按钮宽度加间距
        
        # 计算每行可容纳的按钮数量，最少为3个
        buttons_per_row = max(3, available_width // button_width)
        return int(buttons_per_row)
    
    def create_category_pages(self):
        """为每个分类创建工具页面"""
        # 清空右侧面板
        while self.right_panel.count() > 0:
            self.right_panel.removeWidget(self.right_panel.widget(0))
        
        # 清空分类列表
        self.category_list.clear()
        
        # 创建时钟页面（欢迎页面）
        clock_page = ClockWidget()
        self.right_panel.addWidget(clock_page)
        
        # 创建搜索结果页面
        search_page = self.create_search_page()
        self.right_panel.addWidget(search_page)
        
        # 为每个分类创建页面
        for category in self.config_model.get_categories():
            category_name = category.get("name", "")
            
            # 添加到分类列表
            self.category_list.addItem(category_name)
            
            # 创建分类页面
            category_page = self.create_category_page(category)
            self.right_panel.addWidget(category_page)
            
        # 默认显示时钟页面
        self.right_panel.setCurrentIndex(0)
    
    def create_search_page(self) -> QScrollArea:
        """
        创建搜索结果页面
        
        Returns:
            搜索结果页面
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
        title_label = QLabel("搜索结果")
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Styles.FG_NORMAL};")
        layout.addWidget(title_label)
        
        # 添加搜索结果网格
        self.search_grid = QGridLayout()
        self.search_grid.setSpacing(15)
        layout.addLayout(self.search_grid)
        
        # 添加伸缩项
        layout.addStretch()
        
        # 设置内容
        scroll_area.setWidget(content_widget)
        
        return scroll_area
    
    def create_category_page(self, category: Dict[str, Any]) -> QScrollArea:
        """
        创建分类页面
        
        Args:
            category: 分类数据
            
        Returns:
            分类页面
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
        
        # 添加分类标题
        title_label = QLabel(category.get("name", ""))
        title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Styles.FG_NORMAL};")
        layout.addWidget(title_label)
        
        # 创建工具网格
        tools_grid = QGridLayout()
        tools_grid.setSpacing(15)
        
        # 计算每行显示的按钮数量
        buttons_per_row = self.calculate_buttons_per_row()
        
        # 为每个工具创建按钮
        row, col = 0, 0
        for tool in category.get("tools", []):
            # 创建工具按钮
            tool_button = ToolButton(tool.get("name", ""), tool)
            tool_button.clicked.connect(lambda checked, t=tool: self.run_tool(t))
            tool_button.right_clicked.connect(lambda event, t=tool, c=category.get("name", ""): 
                                             self.show_tool_context_menu(event, t, c))
            
            # 添加到网格布局
            tools_grid.addWidget(tool_button, row, col)
            
            # 更新行列索引
            col += 1
            if col >= buttons_per_row:
                col = 0
                row += 1
        
        # 添加网格布局和伸缩项
        layout.addLayout(tools_grid)
        layout.addStretch()
        
        # 设置内容
        scroll_area.setWidget(content_widget)
        
        return scroll_area
    
    def display_category(self, index: int):
        """
        显示指定分类
        
        Args:
            index: 分类索引
        """
        # 索引+2是因为第0个是时钟页面，第1个是搜索结果页面
        self.right_panel.setCurrentIndex(index + 2)
        
        # 清空搜索框
        self.search_box.clear()
    
    def filter_tools(self, text: str):
        """
        过滤工具
        
        Args:
            text: 过滤文本
        """
        try:
            if not text:
                # 如果搜索文本为空，显示当前分类
                if hasattr(self, 'category_list') and self.category_list.currentRow() >= 0:
                    self.right_panel.setCurrentIndex(self.category_list.currentRow() + 2)
                else:
                    # 如果没有选中分类，则显示时钟页面
                    self.right_panel.setCurrentIndex(0)
                return
            
            # 显示搜索结果页面
            if hasattr(self, 'right_panel'):
                self.right_panel.setCurrentIndex(1)
            
            # 清空搜索结果网格
            if hasattr(self, 'search_grid'):
                while self.search_grid.count():
                    item = self.search_grid.takeAt(0)
                    if item and item.widget():
                        item.widget().deleteLater()
            
            # 获取过滤后的工具(默认使用模糊搜索，阈值0.6)
            if hasattr(self, 'tool_controller'):
                filtered_tools = self.tool_controller.filter_tools(text, fuzzy_threshold=0.6)
            else:
                return
            
            # 计算每行显示的按钮数量
            buttons_per_row = self.calculate_buttons_per_row() if hasattr(self, 'calculate_buttons_per_row') else 3
            
            # 为每个工具创建按钮
            row, col = 0, 0
            for tool in filtered_tools:
                if not isinstance(tool, dict) or 'name' not in tool:
                    continue
                
                # 创建工具按钮
                tool_button = ToolButton(tool.get("name", ""), tool)
                
                # 显示匹配分数（如果是模糊搜索）
                if hasattr(self, 'fuzzy_mode') and self.fuzzy_mode and "match_score" in tool:
                    score = tool["match_score"]
                    tool_button.setToolTip(f"匹配度: {score:.0%}")
                    # 根据匹配度调整透明度
                    tool_button.setGraphicsEffect(None)
                    if score < 0.8:
                        opacity = 0.5 + (score * 0.625)  # 0.6-1.0
                        tool_button.setGraphicsEffect(self.create_opacity_effect(opacity))
                
                tool_button.clicked.connect(lambda checked, t=tool: self.run_tool(t))
                tool_button.right_clicked.connect(lambda event, t=tool, c=tool.get("category", ""): 
                                                self.show_tool_context_menu(event, t, c))
                
                # 添加到网格布局
                if hasattr(self, 'search_grid'):
                    self.search_grid.addWidget(tool_button, row, col)
                
                # 更新行列索引
                col += 1
                if col >= buttons_per_row:
                    col = 0
                    row += 1
        except Exception as e:
            print(f"Error in filter_tools: {str(e)}")
            # 出错时恢复显示所有工具
            if hasattr(self, 'category_list') and self.category_list.currentRow() >= 0:
                self.right_panel.setCurrentIndex(self.category_list.currentRow() + 2)
    
    def create_opacity_effect(self, opacity: float):
        """创建透明度效果"""
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(opacity)
        return effect
    
    def add_tool(self):
        """添加工具"""
        self.tool_controller.add_tool()
    
    def edit_tool(self, tool: Dict[str, Any], category_name: str):
        """
        编辑工具
        
        Args:
            tool: 工具数据
            category_name: 分类名称
        """
        self.tool_controller.edit_tool(tool, category_name)
    
    def delete_tool(self, tool: Dict[str, Any], category_name: str):
        """
        删除工具
        
        Args:
            tool: 工具数据
            category_name: 分类名称
        """
        self.tool_controller.delete_tool(tool, category_name)
    
    def run_tool(self, tool: Dict[str, Any]):
        """
        运行工具
        
        Args:
            tool: 工具数据
        """
        self.tool_controller.run_tool(tool)
    
    def show_tool_context_menu(self, event, tool: Dict[str, Any], category_name: str):
        """
        显示工具右键菜单
        
        Args:
            event: 事件
            tool: 工具数据
            category_name: 分类名称
        """
        menu = QMenu(self)
        menu.setStyleSheet(Styles.MENU_STYLE)
        
        # 创建菜单项
        edit_action = QAction("编辑工具", self)
        edit_action.triggered.connect(lambda: self.edit_tool(tool, category_name))
        menu.addAction(edit_action)
        
        delete_action = QAction("删除工具", self)
        delete_action.triggered.connect(lambda: self.delete_tool(tool, category_name))
        menu.addAction(delete_action)
        
        # 显示菜单
        menu.exec(QCursor.pos())
    
    def reload_tools(self):
        """重新加载工具"""
        self.create_category_pages()
    
    def toggle_maximize(self):
        """切换最大化/还原窗口状态"""
        if self.isMaximized():
            self.showNormal()
            self.title_bar.update_maximize_button(False)
        else:
            self.showMaximized()
            self.title_bar.update_maximize_button(True)
    
    def mousePressEvent(self, event):
        """
        鼠标按下事件处理
        
        Args:
            event: 鼠标事件
        """
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() < self.title_bar.height():
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """
        鼠标移动事件处理
        
        Args:
            event: 鼠标事件
        """
        if self.dragging and not self.isMaximized():
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件处理
        
        Args:
            event: 鼠标事件
        """
        self.dragging = False
    
    def resizeEvent(self, event):
        """
        窗口大小变化事件处理
        
        Args:
            event: 大小变化事件
        """
        # 重新加载工具，调整布局
        self.reload_tools()
        super().resizeEvent(event)
    
    def center_window(self):
        """将窗口居中显示"""
        # 获取屏幕几何信息
        screen_geometry = self.screen().geometry()
        
        # 计算窗口位置
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        
        # 移动窗口
        self.move(x, y) 