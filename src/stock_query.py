"""
股票查询工具主模块 - 使用标准库实现
"""
import json
import os
from datetime import datetime
from typing import Dict, Optional, Tuple
import csv
from io import StringIO

class StockQuery:
    """股票查询类"""
    
    def __init__(self):
        self._setup_console_colors()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'http://finance.sina.com.cn'
        }
    
    def _setup_console_colors(self):
        """设置控制台颜色"""
        self.COLORS = {
            'red': '\033[91m',
            'green': '\033[92m',
            'cyan': '\033[96m',
            'magenta': '\033[95m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
        
    def get_stock_data(self, code: str) -> Optional[Dict]:
        """获取股票数据"""
        try:
            # 新浪股票API
            url = f"http://hq.sinajs.cn/list={code}"
            # 使用标准库urllib替代requests
            from urllib import request, error
            req = request.Request(url, headers=self.headers)
            response = request.urlopen(req)
            content = response.read().decode('gbk')
            
            data = content.split('="')
            if len(data) < 2:
                print(f"{self.COLORS['red']}无法获取股票 {code} 的数据{self.COLORS['end']}")
                return None
                
            values = data[1].split(',')
            if len(values) < 32:
                print(f"{self.COLORS['red']}股票 {code} 数据不完整{self.COLORS['end']}")
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
            print(f"{self.COLORS['red']}获取股票数据时出错: {str(e)}{self.COLORS['end']}")
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
            
        # 显示标题
        print(f"\n{self.COLORS['bold']}{self.COLORS['magenta']}===== {data['name']} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}更新) ====={self.COLORS['end']}\n")
        
        # 显示核心数据
        change_color = 'red' if data['change'] >= 0 else 'green'
        price_text = f"{self.COLORS[change_color]}{data['price']:.2f}{self.COLORS['end']}"
        change_text = f"{self.COLORS[change_color]}{data['change']:+.2f}%{self.COLORS['end']}"
        
        info_items = [
            ("当前价格", price_text),
            ("涨跌幅", change_text),
            ("今日开盘", f"{data['open']:.2f}"),
            ("今日最高", f"{data['high']:.2f}"),
            ("今日最低", f"{data['low']:.2f}"),
            ("成交量(手)", f"{data['volume']/100:.0f}"),
            ("成交额(万)", f"{data['amount']/10000:.2f}"),
            ("市盈率(P/E)", str(data['pe_ratio'])),
            ("总市值", str(data['market_cap'])),
            ("52周最高", str(data['week52_high'])),
            ("52周最低", str(data['week52_low']))
        ]
        
        for label, value in info_items:
            print(f"{self.COLORS['cyan']}{label:<10}{self.COLORS['end']}: {value}")
        
        # 显示公司信息
        print(f"\n{self.COLORS['bold']}{self.COLORS['cyan']}公司简介{self.COLORS['end']}")
        print(data['company_profile'])
        
        print(f"\n{self.COLORS['bold']}{self.COLORS['cyan']}主营业务{self.COLORS['end']}")
        print(data['main_business'])
        
        print(f"\n{self.COLORS['bold']}{self.COLORS['cyan']}最新财务指标{self.COLORS['end']}")
        print(data['latest_finance'])
        
        # 显示公告
        if data['announcements']:
            print(f"\n{self.COLORS['bold']}{self.COLORS['cyan']}重要公告{self.COLORS['end']}")
            for announcement in data['announcements']:
                print(f"• {announcement}")

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