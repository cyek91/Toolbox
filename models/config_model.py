"""
配置模型 - 负责配置文件的读写和管理
"""
import json
import os
from typing import Dict, List, Any, Optional


class ConfigModel:
    """配置模型类，负责处理配置文件的读写和管理"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置模型
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置数据字典
        """
        if not os.path.exists(self.config_file):
            # 如果配置文件不存在，创建默认配置
            default_config = {
                "paths": {
                    "java8": "",
                    "java11": "",
                    "java17": "",
                    "python3": "",
                    "open": "explorer"
                },
                "categories": []
            }
            self.save_config(default_config)
            return default_config
        
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件出错: {str(e)}")
            return {"paths": {}, "categories": []}
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        保存配置到文件
        
        Args:
            config: 要保存的配置数据，如果为None则保存当前配置
            
        Returns:
            是否保存成功
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.config = config
            return True
        except Exception as e:
            print(f"保存配置文件出错: {str(e)}")
            return False
    
    def get_paths(self) -> Dict[str, str]:
        """
        获取路径配置
        
        Returns:
            路径配置字典
        """
        return self.config.get("paths", {})
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        获取所有工具分类
        
        Returns:
            分类数据列表
        """
        return self.config.get("categories", [])
    
    def get_category_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        根据名称获取分类
        
        Args:
            name: 分类名称
            
        Returns:
            分类数据字典，如果不存在则返回None
        """
        for category in self.get_categories():
            if category.get("name") == name:
                return category
        return None
    
    def add_tool(self, tool_data: Dict[str, Any], category_name: str) -> bool:
        """
        添加工具到指定分类
        
        Args:
            tool_data: 工具数据
            category_name: 分类名称
            
        Returns:
            是否添加成功
        """
        category = self.get_category_by_name(category_name)
        if category:
            category.get("tools", []).append(tool_data)
            return self.save_config()
        return False
    
    def update_tool(self, old_tool: Dict[str, Any], new_tool: Dict[str, Any], 
                    old_category_name: str, new_category_name: str) -> bool:
        """
        更新工具信息
        
        Args:
            old_tool: 原工具数据
            new_tool: 新工具数据
            old_category_name: 原分类名称
            new_category_name: 新分类名称
            
        Returns:
            是否更新成功
        """
        # 如果分类名称未变，直接在原分类中更新
        if old_category_name == new_category_name:
            category = self.get_category_by_name(old_category_name)
            if category:
                tools = category.get("tools", [])
                for i, tool in enumerate(tools):
                    if tool == old_tool:
                        tools[i] = new_tool
                        return self.save_config()
        else:
            # 从旧分类中删除
            old_category = self.get_category_by_name(old_category_name)
            if old_category:
                tools = old_category.get("tools", [])
                if old_tool in tools:
                    tools.remove(old_tool)
            
            # 添加到新分类
            return self.add_tool(new_tool, new_category_name)
        
        return False
    
    def delete_tool(self, tool: Dict[str, Any], category_name: str) -> bool:
        """
        删除工具
        
        Args:
            tool: 工具数据
            category_name: 分类名称
            
        Returns:
            是否删除成功
        """
        category = self.get_category_by_name(category_name)
        if category:
            tools = category.get("tools", [])
            if tool in tools:
                tools.remove(tool)
                return self.save_config()
        return False 