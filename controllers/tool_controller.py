"""
工具控制器 - 处理工具相关操作
"""
from typing import Dict, Any, List, Optional, Callable
from PyQt6.QtWidgets import QMessageBox, QWidget

from models.config_model import ConfigModel
from utils.runner import ToolRunner
from views.tool_dialog import ToolDialog


class ToolController:
    """工具控制器类，处理工具相关操作"""
    
    def __init__(self, config_model: ConfigModel, parent: QWidget = None):
        """
        初始化工具控制器
        
        Args:
            config_model: 配置模型
            parent: 父控件
        """
        self.config_model = config_model
        self.parent = parent
        self.tool_runner = ToolRunner(config_model.get_paths())
        
        # 工具修改回调
        self.on_tool_changed_callback: Optional[Callable] = None
    
    def set_on_tool_changed_callback(self, callback: Callable):
        """
        设置工具修改回调
        
        Args:
            callback: 回调函数
        """
        self.on_tool_changed_callback = callback
    
    def add_tool(self) -> bool:
        """
        添加工具
        
        Returns:
            是否成功添加
        """
        # 创建添加工具对话框
        dialog = ToolDialog(self.config_model.get_categories(), self.parent)
        
        # 如果用户确认，添加工具
        if dialog.exec():
            # 获取工具数据和分类名称
            tool_data = dialog.get_tool_data()
            category_name = dialog.get_category_name()
            
            # 验证工具数据
            if not self._validate_tool_data(tool_data):
                return False
            
            # 添加工具
            success = self.config_model.add_tool(tool_data, category_name)
            
            # 调用回调
            if success and self.on_tool_changed_callback:
                self.on_tool_changed_callback()
            
            return success
        
        return False
    
    def edit_tool(self, tool: Dict[str, Any], category_name: str) -> bool:
        """
        编辑工具
        
        Args:
            tool: 工具数据
            category_name: 分类名称
            
        Returns:
            是否成功编辑
        """
        # 创建编辑工具对话框
        dialog = ToolDialog(self.config_model.get_categories(), self.parent, tool)
        
        # 预先选择当前分类
        category_index = dialog.category_combo.findText(category_name)
        if category_index >= 0:
            dialog.category_combo.setCurrentIndex(category_index)
        
        # 如果用户确认，更新工具
        if dialog.exec():
            # 获取新的工具数据和分类名称
            new_tool_data = dialog.get_tool_data()
            new_category_name = dialog.get_category_name()
            
            # 验证工具数据
            if not self._validate_tool_data(new_tool_data):
                return False
            
            # 更新工具
            success = self.config_model.update_tool(tool, new_tool_data, category_name, new_category_name)
            
            # 调用回调
            if success and self.on_tool_changed_callback:
                self.on_tool_changed_callback()
            
            return success
        
        return False
    
    def delete_tool(self, tool: Dict[str, Any], category_name: str) -> bool:
        """
        删除工具
        
        Args:
            tool: 工具数据
            category_name: 分类名称
            
        Returns:
            是否成功删除
        """
        # 确认删除
        reply = QMessageBox.question(
            self.parent,
            "确认删除",
            f"确定要删除工具\"{tool.get('name')}\"吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 删除工具
            success = self.config_model.delete_tool(tool, category_name)
            
            # 调用回调
            if success and self.on_tool_changed_callback:
                self.on_tool_changed_callback()
            
            return success
        
        return False
    
    def run_tool(self, tool: Dict[str, Any]) -> bool:
        """
        运行工具
        
        Args:
            tool: 工具数据
            
        Returns:
            是否成功运行
        """
        # 运行工具
        error = self.tool_runner.run_tool(tool)
        
        # 如果出错，显示错误信息
        if error:
            QMessageBox.warning(self.parent, "警告", error)
            return False
        
        return True
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """
        计算两个字符串的Levenshtein距离
        
        Args:
            s1: 字符串1
            s2: 字符串2
            
        Returns:
            编辑距离
        """
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def filter_tools(self, text: str, fuzzy_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        根据文本过滤工具(支持模糊匹配)
        
        Args:
            text: 过滤文本
            fuzzy_threshold: 模糊匹配阈值(0-1)
            
        Returns:
            符合条件的工具列表，按匹配度排序
        """
        result = []
        
        # 如果文本为空，返回空列表
        if not text:
            return result
        
        # 转换为小写，便于不区分大小写比较
        text = text.lower()
        
        # 遍历所有分类和工具
        for category in self.config_model.get_categories():
            for tool in category.get("tools", []):
                # 获取工具名称，转换为小写
                tool_name = tool.get("name", "").lower()
                
                # 精确匹配
                if text in tool_name:
                    # 复制工具数据，并添加分类信息和匹配分数
                    tool_copy = tool.copy()
                    tool_copy["category"] = category.get("name", "")
                    tool_copy["match_score"] = 1.0  # 完全匹配
                    result.append(tool_copy)
                    continue
                
                # 模糊匹配
                distance = self._levenshtein_distance(text, tool_name)
                max_len = max(len(text), len(tool_name))
                similarity = 1 - (distance / max_len)
                
                if similarity >= fuzzy_threshold:
                    # 复制工具数据，并添加分类信息和匹配分数
                    tool_copy = tool.copy()
                    tool_copy["category"] = category.get("name", "")
                    tool_copy["match_score"] = similarity
                    result.append(tool_copy)
        
        # 按匹配分数降序排序
        result.sort(key=lambda x: x["match_score"], reverse=True)
        return result
    
    def _validate_tool_data(self, tool_data: Dict[str, Any]) -> bool:
        """
        验证工具数据
        
        Args:
            tool_data: 工具数据
            
        Returns:
            是否有效
        """
        # 检查工具名称
        if not tool_data.get("name"):
            QMessageBox.warning(self.parent, "警告", "请输入工具名称")
            return False
        
        # 检查工具路径
        if not tool_data.get("path"):
            QMessageBox.warning(self.parent, "警告", "请输入工具路径或URL")
            return False
        
        # 如果是Java类型，检查Java版本
        if tool_data.get("type") == "java" and not tool_data.get("java_version"):
            QMessageBox.warning(self.parent, "警告", "请选择Java版本")
            return False
        
        return True 