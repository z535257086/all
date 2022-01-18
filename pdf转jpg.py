import fitz
import os

'''
# 将PDF转化为图片
pdfPath pdf文件的路径
imgPath 图像要保存的文件夹
zoom_x x方向的缩放系数
zoom_y y方向的缩放系数
rotation_angle 旋转角度
'''


def pdf_image(pdfPath, imgPath, zoom_x, zoom_y, rotation_angle):
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    # 逐页读取PDF
    for pg in range(0, pdf.pageCount):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        # 开始写图像
        pm.save(imgPath + str(pg) + ".png")
    pdf.close()


def listdir(path, list_name):  # 传入存储的list

    for files in os.walk(path):
        for file in files:
            list_name.append(file)
    # new_name = [i[:-4] for i in list_name[2]]
    # print(new_name)
    for i in list_name[2]:
        new_name = i[:-4]
        if ".pdf" in i:
            pdf_image(r"D:\pdf\{}".format(i), r"D:\pdf\{}".format(new_name), 5, 5, 0)


pdf = []
listdir(r"D:\pdf", pdf)
# pdf_image(r"C:\Users\admin\PycharmProjects\untitled1\pdf\LSVMB6C68LN031497手续.pdf", r"D:\pdf\\", 5, 5, 0)
