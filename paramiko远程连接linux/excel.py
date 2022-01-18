import xlrd
import xlwt
from xlutils.copy import copy

class e_controller():
    def __init__(self, excelname, index):
        # 读取时需要
        self.data = xlrd.open_workbook(excelname)
        self.table = self.data.sheet_by_index(index)
        # 写入时需要
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.worksheet = self.workbook.add_sheet("my-sheet")

    # 读取excel
    def get_value(self, rowx, colx):
        return self.table.cell_value(rowx, colx)

    # 获取有效行数
    def get_nrows(self):
        return self.table.nrows

    # 获取有效列数
    def get_ncols(self):
        return self.table.ncols

    # 获取行数据
    def get_nrow_value(self, rowx):
        return self.table.row_values(rowx, start_colx=0, end_colx=None)

    # 写入excle,0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error, 6 blank
    def set_value(self, row, col, value):
        self.worksheet.write(row, col, value)
        self.workbook.save("D:\\result.xls")

    # 数据整行写入excel
    def set_values(self, value):
        for r in range(len(value)):
            for c in range(len(value[r])):
                self.worksheet.write(r, c, value[r][c])
        self.workbook.save("D:\\result.xls")
        print("写入成功")

