# 实时股票查询工具

## 项目简介
这是一个基于命令行的实时股票价格查询工具，支持同时查询多支股票，数据来源为新浪股票API。本工具包括传统K线图和现代化界面两种显示方式。

## 功能特点
- 实时查询股票价格
- 默认包含沪指、深指查询
- 支持多股票同时查询
- 可配置查询间隔和线程数
- K线图形象直观展示股票走势
- 现代化界面提供更美观的数据展示

## 安装说明
1. 克隆仓库：
```bash
# 从Gitee克隆
git clone https://gitee.com/your-username/stock-query.git
cd stock-query
```

2. 安装依赖：
```bash
# 使用 Python3 安装依赖
python3 -m pip install -r requirements.txt

# 可选：更新 pip 到最新版本
python3 -m pip install --upgrade pip
```

## 使用方法
```bash
# 基本使用 - 传统界面
python3 -m src.main -c sz000816

# 使用现代化界面
python3 -m src.modern_main -c sz000816

# 查询多支股票
python3 -m src.main -c sh601003,sz000816,sz000778

# 自定义查询间隔和线程数
python3 -m src.main -c sz000816 -t 4 -s 3
```

### 命令行参数
- `-c, --codes`: 股票代码（必需），多个代码用逗号分隔
- `-s, --interval`: 查询间隔（秒），默认6秒
- `-t, --threads`: 线程数，默认3个线程
- `-h, --help`: 显示帮助信息

## 项目结构
```
stock-query/
├── src/
│   ├── __init__.py
│   ├── main.py         # 传统界面入口
│   ├── modern_main.py  # 现代化界面入口
│   ├── stock.py        # 传统股票数据处理
│   └── modern_stock.py # 现代化股票数据处理
├── tests/              # 单元测试
├── charts/             # 生成的图表保存目录
├── requirements.txt    # 依赖包列表
├── pyproject.toml      # 项目配置
└── README.md           # 项目说明
```

## 技术实现
- 使用新浪股票API获取实时数据
- 多线程并发查询
- Matplotlib生成可视化图表
- Pandas处理和分析股票数据
- 线程池实现高效数据获取
- 优雅的命令行参数处理

## Gitee代码管理
将代码提交到公司Gitee服务器的步骤：

1. 在Gitee上创建一个新仓库

2. 配置本地仓库的远程地址：
```bash
# 添加Gitee远程仓库
git remote add gitee https://gitee.com/your-username/stock-query.git
```

3. 初次提交代码：
```bash
# 初始化本地仓库(如果尚未初始化)
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "初始提交：实时股票查询工具"

# 推送到Gitee
git push -u gitee master
```

4. 后续更新：
```bash
git add .
git commit -m "更新说明"
git push gitee master
```

## 注意事项
- 投资需谨慎，股市有风险。本工具仅供参考，不构成任何投资建议。
- 本工具需要 Python 3.6 或更高版本。
- 如果遇到权限问题，可能需要使用 `sudo python3 -m pip install -r requirements.txt` 进行安装。
- 图表保存在当前目录或charts目录中，可通过查看对应的PNG文件查看。