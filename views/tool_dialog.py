"""
工具对话框 - 用于添加和编辑工具
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, 
                             QDialogButtonBox, QFileDialog)
from PyQt6.QtCore import Qt
from typing import List, Dict, Any, Optional

from utils.styles import Styles


class ToolDialog(QDialog):
    """工具对话框类，用于添加和编辑工具"""
    
    def __init__(self, categories: List[Dict[str, Any]], parent=None, tool_data: Optional[Dict[str, Any]] = None):
        """
        初始化工具对话框
        
        Args:
            categories: 分类数据列表
            parent: 父控件
            tool_data: 工具数据（编辑模式）
        """
        super().__init__(parent)
        
        # 设置对话框属性
        self.setWindowTitle("添加工具" if tool_data is None else "编辑工具")
        self.setMinimumWidth(400)
        self.setStyleSheet(Styles.TOOL_DIALOG)
        
        # 保存分类和工具数据
        self.categories = categories
        self.tool_data = tool_data
        self.is_edit_mode = tool_data is not None
        
        # 创建界面
        self.setup_ui()
        
        # 如果是编辑模式，填充数据
        if self.is_edit_mode:
            self.fill_tool_data()
    
    def setup_ui(self):
        """创建界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 表单布局
        self.form_layout = QFormLayout()
        
        # 工具名称
        self.name_edit = QLineEdit()
        self.form_layout.addRow("工具名称:", self.name_edit)
        
        # 工具类型
        self.type_combo = QComboBox()
        self.type_combo.addItems(["java", "gui", "url", "python", "terminal"])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        self.form_layout.addRow("工具类型:", self.type_combo)
        
        # Java版本（仅对Java类型可见）
        self.java_label = QLabel("Java版本:")
        self.java_version_combo = QComboBox()
        self.java_version_combo.addItems(["java8", "java11", "java17"])
        self.form_layout.addRow(self.java_label, self.java_version_combo)
        
        # 路径/URL
        self.path_label = QLabel("路径:")
        self.path_edit = QLineEdit()
        self.browse_button = QPushButton("浏览...")
        self.browse_button.clicked.connect(self.browse_file)
        self.path_layout = QHBoxLayout()
        self.path_layout.addWidget(self.path_edit)
        self.path_layout.addWidget(self.browse_button)
        self.form_layout.addRow(self.path_label, self.path_layout)
        
        # 命令
        self.command_label = QLabel("命令:")
        self.command_edit = QLineEdit()
        self.form_layout.addRow(self.command_label, self.command_edit)
        
        # 可选参数
        self.optional_label = QLabel("可选参数:")
        self.optional_edit = QLineEdit()
        self.form_layout.addRow(self.optional_label, self.optional_edit)
        
        # 分类
        self.category_combo = QComboBox()
        self.category_combo.addItems([cat["name"] for cat in self.categories])
        self.form_layout.addRow("所属分类:", self.category_combo)
        
        # 按钮
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                         QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        # 添加表单布局和按钮到主布局
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(self.button_box)
        
        # 初始化显示/隐藏Java版本选择
        self.on_type_changed(self.type_combo.currentText())
    
    def on_type_changed(self, text: str):
        """
        根据工具类型显示或隐藏相关字段
        
        Args:
            text: 工具类型
        """
        # 重置所有字段的显示状态
        self.reset_field_visibility()
        
        if text == "url":
            # URL类型只需要名称和URL地址
            self.path_label.setText("URL地址:")
            self.path_edit.setPlaceholderText("https://example.com")
            self.browse_button.setVisible(False)
            # 隐藏不需要的字段
            self.java_label.setVisible(False)
            self.java_version_combo.setVisible(False)
            self.command_label.setVisible(False)
            self.command_edit.setVisible(False)
            self.optional_label.setVisible(False)
            self.optional_edit.setVisible(False)
            # 清空不需要的字段
            self.command_edit.setText("")
            self.optional_edit.setText("")
            
        elif text == "java":
            # Java类型需要所有字段
            self.path_label.setText("路径:")
            self.path_edit.setPlaceholderText("")
            self.browse_button.setVisible(True)
            # 显示Java特有字段
            self.java_label.setVisible(True)
            self.java_version_combo.setVisible(True)
            # 其他字段也要显示
            self.command_label.setVisible(True)
            self.command_edit.setVisible(True)
            self.optional_label.setVisible(True)
            self.optional_edit.setVisible(True)
            # 设置默认命令
            if not self.command_edit.text():
                self.command_edit.setText("-jar")
            
        else:
            # 其他类型（gui, python, terminal）
            self.path_label.setText("路径:")
            self.path_edit.setPlaceholderText("")
            self.browse_button.setVisible(True)
            # 隐藏Java特有字段
            self.java_label.setVisible(False)
            self.java_version_combo.setVisible(False)
            # 其他字段保持显示
            self.command_label.setVisible(True)
            self.command_edit.setVisible(True)
            self.optional_label.setVisible(True)
            self.optional_edit.setVisible(True)
    
    def reset_field_visibility(self):
        """重置所有字段的显示状态"""
        self.path_label.setVisible(True)
        self.path_edit.setVisible(True)
        self.browse_button.setVisible(True)  # 不是布局对象setVisible，而是布局中的控件
        self.java_label.setVisible(True)
        self.java_version_combo.setVisible(True)
        self.command_label.setVisible(True)
        self.command_edit.setVisible(True)
        self.optional_label.setVisible(True)
        self.optional_edit.setVisible(True)
    
    def browse_file(self):
        """打开文件选择对话框"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*)")
        if file_path:
            self.path_edit.setText(file_path)
    
    def fill_tool_data(self):
        """填充工具数据（编辑模式）"""
        if not self.tool_data:
            return
            
        # 填充基本字段
        self.name_edit.setText(self.tool_data.get("name", ""))
        
        # 设置类型
        tool_type = self.tool_data.get("type", "")
        index = self.type_combo.findText(tool_type)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
        
        # 设置路径
        self.path_edit.setText(self.tool_data.get("path", ""))
        
        # 设置命令
        self.command_edit.setText(self.tool_data.get("command", ""))
        
        # 设置可选参数
        self.optional_edit.setText(self.tool_data.get("optional", ""))
        
        # 设置Java版本（如果适用）
        if tool_type == "java":
            java_version = self.tool_data.get("java_version", "java8")
            index = self.java_version_combo.findText(java_version)
            if index >= 0:
                self.java_version_combo.setCurrentIndex(index)
        
        # 根据工具类型更新UI
        self.on_type_changed(tool_type)
    
    def get_tool_data(self) -> Dict[str, Any]:
        """
        获取工具数据
        
        Returns:
            工具数据字典
        """
        tool_data = {
            "name": self.name_edit.text(),
            "type": self.type_combo.currentText(),
            "path": self.path_edit.text(),
            "command": self.command_edit.text(),
            "optional": self.optional_edit.text()
        }
        
        # 如果是Java类型，添加Java版本
        if tool_data["type"] == "java":
            tool_data["java_version"] = self.java_version_combo.currentText()
        
        return tool_data
    
    def get_category_name(self) -> str:
        """
        获取选择的分类名称
        
        Returns:
            分类名称
        """
        return self.category_combo.currentText() 