# coding:utf-8
"""
create on Mar 17,2019 by Wayne
"""

import xlrd
import xlwt
import xlutils.copy

data = xlrd.open_workbook('../000PublicData/demo_excel.xls')
table = data.sheets()[0]  # 打开第一张表
nrows = table.nrows  # 获取表的行数
for i in range(nrows):  # 循环逐行打印
    if i == 0:  # 跳过第一行
        continue
    print(table.row_values(i)[:4])  # 取前四行

"""
xlrd读取excel文件时不能对其进行操作的
xlwt生成excel文件时不能在已有的excel文件基础上进行修改的
如果需要修改文件就要使用xluntils模块
pyExcelerator模块与xlwt类似，也可以用来生成excel文件
"""
# 创建workbook和sheet对象
workbook = xlwt.Workbook()  # 注意Workbook的开头W要大写
sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
sheet1.write(0, 0,  "this should overwrite1")
sheet1.write(0, 1,  "aaaaaaaa")
# 保存excel文件，有同名文件时直接覆盖
workbook.save("../000PublicData/test_save_excel.xls")

# 打开一个workbook
rb = xlrd.open_workbook('../000PublicData/demo_excel.xls')
wb = xlutils.copy.copy(rb)
# 获取sheet对象，通过sheet_by_index()获取sheet对象没有write()方法
ws = wb.get_sheet(0)
# 写入数据
ws.write(0, 0, '出发点')
# 添加sheet页
wb.add_sheet("sheet_add_2", cell_overwrite_ok=True)
wb.save('../000PublicData/demo_excel.xls')
