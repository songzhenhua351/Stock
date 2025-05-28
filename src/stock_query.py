"""
股票查询工具主模块
"""
import json
import os
from datetime import datetime
from typing import Dict, Optional, Tuple

import pandas as pd
import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text

class StockQuery:
    """股票查询类"""
    
    def __init__(self):
        self.console = Console()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'http://finance.sina.com.cn'
        }
        
    def get_stock_data(self, code: str) -> Optional[Dict]:
        """获取股票数据"""
        try:
            # 新浪股票API
            url = f"http://hq.sinajs.cn/list={code}"
            response = requests.get(url, headers=self.headers)
            response.encoding = 'gbk'
            
            data = response.text.split('="')
            if len(data) < 2:
                self.console.print(f"[red]无法获取股票 {code} 的数据[/red]")
                return None
                
            values = data[1].split(',')
            if len(values) < 32:
                self.console.print(f"[red]股票 {code} 数据不完整[/red]")
                return None
                
            # 获取公司信息
            company_info = self.get_company_info(code)
            
            # 构建股票数据字典
            stock_data = {
                'name': values[0],
                'open': float(values[1]),
                'prev_close': float(values[2]),
                'price': float(values[3]),
                'high': float(values[4]),
                'low': float(values[5]),
                'volume': float(values[8]),
                'amount': float(values[9]),
                'date': values[30],
                'time': values[31],
                'change': round((float(values[3]) - float(values[2])) / float(values[2]) * 100, 2),
                'pe_ratio': company_info.get('pe_ratio', '--'),
                'market_cap': company_info.get('market_cap', '--'),
                'week52_high': company_info.get('week52_high', '--'),
                'week52_low': company_info.get('week52_low', '--'),
                'company_profile': company_info.get('profile', '--'),
                'main_business': company_info.get('business', '--'),
                'latest_finance': company_info.get('finance', '--'),
                'announcements': company_info.get('announcements', [])
            }
            
            return stock_data
            
        except Exception as e:
            self.console.print(f"[red]获取股票数据时出错: {str(e)}[/red]")
            return None
            
    def get_company_info(self, code: str) -> Dict:
        """获取公司信息(示例数据)"""
        # 实际项目中应该从专业数据源获取这些信息
        return {
            'pe_ratio': 32.5,
            'market_cap': '2350亿',
            'week52_high': 58.86,
            'week52_low': 31.55,
            'profile': '公司是国内领先的人工智能技术提供商',
            'business': '人工智能技术研发与应用服务',
            'finance': '营收同比增长25%，净利润增长30%',
            'announcements': [
                '发布新一代AI大模型',
                '与某央企达成战略合作'
            ]
        }
        
    def display_stock_info(self, data: Dict):
        """显示股票信息"""
        if not data:
            return
            
        # 创建主表格
        table = Table(title=f"{data['name']} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}更新)",
                     show_header=True, header_style="bold magenta")
        
        # 添加列
        table.add_column("指标", style="cyan", no_wrap=True)
        table.add_column("数值", justify="right")
        
        # 添加核心数据
        change_color = "red" if data['change'] >= 0 else "green"
        price_text = Text(f"{data['price']:.2f}", style=change_color)
        change_text = Text(f"{data['change']:+.2f}%", style=change_color)
        
        table.add_row("当前价格", price_text)
        table.add_row("涨跌幅", change_text)
        table.add_row("今日开盘", f"{data['open']:.2f}")
        table.add_row("今日最高", f"{data['high']:.2f}")
        table.add_row("今日最低", f"{data['low']:.2f}")
        table.add_row("成交量(手)", f"{data['volume']/100:.0f}")
        table.add_row("成交额(万)", f"{data['amount']/10000:.2f}")
        table.add_row("市盈率(P/E)", str(data['pe_ratio']))
        table.add_row("总市值", str(data['market_cap']))
        table.add_row("52周最高", str(data['week52_high']))
        table.add_row("52周最低", str(data['week52_low']))
        
        # 显示主表格
        self.console.print(table)
        
        # 显示公司信息
        self.console.print("\n[bold cyan]公司简介[/bold cyan]")
        self.console.print(data['company_profile'])
        
        self.console.print("\n[bold cyan]主营业务[/bold cyan]")
        self.console.print(data['main_business'])
        
        self.console.print("\n[bold cyan]最新财务指标[/bold cyan]")
        self.console.print(data['latest_finance'])
        
        # 显示公告
        if data['announcements']:
            self.console.print("\n[bold cyan]重要公告[/bold cyan]")
            for announcement in data['announcements']:
                self.console.print(f"• {announcement}")

def main():
    """主函数"""
    query = StockQuery()
    
    while True:
        code = input("\n请输入股票代码(按q退出): ").strip().lower()
        
        if code == 'q':
            break
            
        # 检查股票代码格式
        if not code.startswith(('sh', 'sz')):
            print("股票代码格式错误！请使用'sh'或'sz'前缀，如：sh600000")
            continue
            
        # 获取并显示股票数据
        data = query.get_stock_data(code)
        if data:
            query.display_stock_info(data)
        
if __name__ == "__main__":
    main()