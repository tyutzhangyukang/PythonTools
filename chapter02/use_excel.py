from datetime import datetime

import MySQLdb

from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Font, colors


class ExcelUtils(object):
    """
    pip install openpyxl
    pip install pillow
    """
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws_two = self.wb.create_sheet('我的表单')
        self.ws.title = '你的表单'
        self.ws.sheet_properties.tabColor = 'ff0000'
        self.ws_three = self.wb.create_sheet()

    def do_sth(self):
        #插入数据
        self.ws['A1'] = 66
        self.ws['A2'] = '你好'
        self.ws['A3'] = datetime.now()

        for row in self.ws_two['A1:E5']:
            for cell in row:
                cell.value = 2

        #对数据进行求和
        self.ws_two['G1'] = '=SUM(A1:E1)'

        #设置文字
        font = Font(sz=18, color=colors.RED)
        self.ws['A2'].font = font
        #插入图片
        img = Image('./static/temp.jpg')
        self.ws.add_image(img, 'B1')

        #合并单元格
        self.ws.merge_cells('A4:E5')
        self.ws.unmerge_cells('A4:E5')
        self.wb.save('./static/test.xlsx')

    def read_xls(self):
        """
        读取excel数据
        :return:
        """
        ws = load_workbook('./static/template.xlsx')
        names = ws.get_sheet_names()
        #print(names)
        # wb = ws.active
        # wb = ws['北京大学统计']
        # wb = ws[names[0]]
        # for row in wb.rows:
        #     for cell in row:
        #         print(cell.value)
        conn = self.get_conn()
        cusor = conn.cursor()
        sql = 'INSERT INTO `score`(`year`,`max`,`avg`) VALUES(2001, 400, 360)'
        cusor.execute(sql)
        conn.autocommit(True)
        print(conn)

    def get_conn(self):
        """获取MySQL的连接"""
        conn = MySQLdb.connect(
            db='user_grade',
            host='127.0.0.1',
            user='root',
            password='',
            charset='utf8'
        )
        return conn


if __name__ == '__main__':
    client = ExcelUtils()
    client.read_xls()