from tkinter.messagebox import *
from osgeo import gdal, ogr


def check(file):
    return True if file else False


def vectorToRaster(master, openFileName, saveFileName, vars):
    """
    矢量转栅格
    :return:
    """
    if not (check(openFileName) and check(saveFileName)):
        return
    open_file = openFileName
    vector_ds = ogr.Open(open_file)
    vector_layer = vector_ds.GetLayer()
    pixel_size = vars['栅格边长(m)'].get()
    save_file = saveFileName
    # 确定栅格化参数
    x_min, x_max, y_min, y_max = vector_layer.GetExtent()
    x_res = int((x_max - x_min) / pixel_size)
    y_res = int((y_max - y_min) / pixel_size)
    target_ds = gdal.GetDriverByName('GTiff').Create(save_file, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
    # 进行栅格化
    target_ds.GetRasterBand(1).SetNoDataValue(0)
    gdal.RasterizeLayer(target_ds, [1], vector_layer, options=["ALL_TOUCHED=TRUE", "CLIP=YES"])
    # 保存栅格数据
    target_ds.FlushCache()
    showinfo('CscsGIS', f'成功栅格化{open_file}矢量数据！')
    master.destroy()


def rasterToAscii(master, openFileName, saveFileName, vars):
    """
    栅格转ASCII
    :return:
    """
    if not (check(openFileName) and check(saveFileName)):
        return
    open_file = openFileName
    raster_ds = gdal.Open(open_file)
    save_file = saveFileName
    # 读取栅格数据
    band = raster_ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    xSize = raster_ds.RasterXSize
    ySize = raster_ds.RasterYSize
    # 获取栅格数据的地理参考信息
    geotransform = raster_ds.GetGeoTransform()
    # 创建输出文件
    output_file = open(save_file, 'w')
    output_file.write(f'ncols\t\t{xSize}\n')
    output_file.write(f'nrows\t\t{ySize}\n')
    output_file.write(f'xllcorner\t\t{geotransform[0]:.4f}\n')
    output_file.write(f'yllcorner\t\t{geotransform[3] + ySize * geotransform[5]:.4f}\n')
    output_file.write(f'cellsize\t\t{geotransform[1]}\n')
    output_file.write(f'NODATA_value\t{-9999}\n')
    # 将栅格数据转换为ASCII格式写入输出文件
    data = band.ReadAsArray()
    for i in range(ySize):
        row = data[i]
        row_str = ' '.join(['1' if val != nodata else '0' for val in row])
        output_file.write(row_str + '\n')
    showinfo('CscsGIS', f'成功将{open_file}栅格数据转换为ASCII！')
    master.destroy()
