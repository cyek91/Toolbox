"""渗透测试工具箱应用 - 程序入口

该模块是应用程序的主入口点，负责初始化GUI应用程序和主窗口。
"""

import sys
from typing import NoReturn

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from views.main_window import MainWindow

def main() -> NoReturn:
    """程序入口函数
    
    初始化QApplication，创建并显示主窗口，启动事件循环。
    """
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序名称
    app.setApplicationName("渗透测试工具箱")
    
    # 创建主窗口(延迟100ms显示确保完全初始化)
    window = MainWindow()
    QTimer.singleShot(100, window.show)
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 