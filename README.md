# 渗透测试工具箱

一个基于PyQt6的渗透测试工具箱GUI应用程序，支持Windows系统。

## 功能特性

- **工具分类管理**：支持自定义工具分类
- **工具管理**：支持工具的添加、编辑和删除
- **智能搜索**：支持精确匹配和模糊搜索（基于Levenshtein距离算法）
- **多种工具类型支持**：
  - Java程序（支持Java 8/11/17）
  - Python脚本
  - URL链接（使用默认浏览器打开）
  - GUI/Terminal程序（直接运行）
- **响应式布局**：自动调整工具按钮布局以适应窗口大小
- **无边框窗口**：带有自定义标题栏的现代化UI

## 系统要求

- Windows操作系统
- Python 3.7+
- PyQt6 6.3.0+

## 安装指南

1. 克隆本仓库：
   ```bash
   git clone <仓库地址>
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序：
   ```bash
   python main.py
   ```

## 配置说明

配置文件位于`config.json`，包含以下配置项：

- **路径配置**：
  - `java8`：Java 8路径
  - `java11`：Java 11路径
  - `java17`：Java 17路径
  - `python3`：Python 3路径
  - `open`：文件打开命令（Windows默认为"explorer"）

- **工具分类**：可以添加自定义分类和工具

## 使用说明

1. **添加工具**：
   - 点击"添加工具"按钮
   - 填写工具信息（名称、路径、类型等）
   - 选择分类或创建新分类

2. **运行工具**：
   - 在分类列表中选择分类
   - 点击工具按钮运行

3. **搜索工具**：
   - 在搜索框中输入工具名称
   - 支持模糊匹配（如"nmap"可以匹配到"nmap scanner"）

## 项目结构

```
.
├── .venv/                # Python虚拟环境
├── config.json           # 配置文件
├── controllers/          # 控制器
│   └── tool_controller.py # 工具控制器
├── main.py               # 主程序入口
├── models/               # 数据模型
│   └── config_model.py   # 配置模型
├── README.md            # 说明文档
├── requirements.txt      # 依赖列表
├── screenshot.png       # 程序截图
├── utils/                # 工具类
│   └── runner.py         # 工具运行器
└── views/                # 视图
    └── main_window.py    # 主窗口视图
```

## 截图

![应用截图](screenshot.png)

## 贡献指南

欢迎提交Pull Request或Issue报告问题。

## 许可证

[MIT](LICENSE)
