"""
工具运行器 - 负责运行不同类型的工具
"""
import subprocess
import webbrowser
from typing import Dict, Any, Optional


class ToolRunner:
    """工具运行器，负责运行不同类型的工具"""
    
    def __init__(self, paths: Dict[str, str]):
        """
        初始化工具运行器
        
        Args:
            paths: 路径配置字典
        """
        self.paths = paths
    
    def run_tool(self, tool: Dict[str, Any]) -> Optional[str]:
        """
        运行工具
        
        Args:
            tool: 工具数据
            
        Returns:
            错误信息，如果运行成功则返回None
        """
        tool_type = tool.get("type", "")
        path = tool.get("path", "")
        command = tool.get("command", "")
        optional = tool.get("optional", "")
        
        if not path:
            return "工具路径未配置"
        
        try:
            if tool_type == "url":
                # 打开URL
                webbrowser.open(path)
            
            elif tool_type == "java":
                # 运行Java程序
                java_version = tool.get("java_version", "java8")
                java_path = self.paths.get(java_version)
                
                if not java_path:
                    return f"未找到Java版本 {java_version} 的配置"
                
                # 构建命令
                cmd = f"\"{java_path}\" {optional} {command} \"{path}\""
                subprocess.Popen(cmd, shell=True)
            
            elif tool_type == "python":
                # 运行Python程序
                python_path = self.paths.get("python3")
                
                if not python_path:
                    return "未找到Python路径配置"
                
                # 构建命令
                cmd = f"\"{python_path}\" {command} \"{path}\" {optional}"
                subprocess.Popen(cmd, shell=True)
            
            elif tool_type == "gui" or tool_type == "terminal":
                # 直接运行程序或打开终端
                if command:
                    cmd = f"{command} \"{path}\" {optional}"
                else:
                    cmd = f"\"{path}\" {optional}"
                
                subprocess.Popen(cmd, shell=True)
            
            else:
                return f"未知的工具类型: {tool_type}"
            
            return None
        
        except Exception as e:
            return f"运行工具时出错: {str(e)}" 