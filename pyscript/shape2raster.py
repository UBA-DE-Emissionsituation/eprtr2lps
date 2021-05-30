import geopandas as gpd
import numpy
import os
import gdal
from scipy import interpolate
import pykrige as pykg


#  class for writing raster data
class Rasterfun(object):
    def __init__(self):
        pass

    @staticmethod
    def schreibebsq(numpyarray: numpy.ndarray, out: str):
        if len(numpyarray.shape) != 3:
            print("no valid datacube!")
            return -1
        form = "ENVI"
        driver = gdal.GetDriverByName(form)
        dimat = numpy.shape(numpyarray)
        dataset_out = driver.Create(out, dimat[2], dimat[1], dimat[0], gdal.GDT_Float32)
        count = 1
        while count <= dimat[0]:
            dim = count - 1
            dataset_out.GetRasterBand(count).WriteArray(numpyarray[dim, :, :])
            count += 1
        dataset_out = None  # Close dataset clean

    def schreibebsqsingle(numpyarray: numpy.ndarray, out: str):
        if len(numpyarray.shape) != 2:
            print("no valid 2d-dataset!")
            return -1
        form = "ENVI"
        driver = gdal.GetDriverByName(form)
        dimat = numpy.shape(numpyarray)
        dataset_out = driver.Create(out, dimat[1], dimat[0], 1, gdal.GDT_Float32)
        dataset_out.GetRasterBand(1).WriteArray(numpyarray)
        dataset_out = None  # Close dataset clean


#  Class for Rastering Pointdata from Shapefiles
class ShapefilePointtool(object):
    def __init__(self):
        pass

    @staticmethod
    def reproject(vectordata, epsg_from: int, epsg_to: int):
        data = gpd.read_file(vectordata)
        basename = os.path.splitext("/path/to/some/file.txt")[0]
        data.crs = {"init": "epsg:" + str(epsg_from)}
        print("init" + "epsg:" + str(epsg_from))
        print('epsg:' + str(epsg_to))
        a = data.to_crs({'init': 'epsg:' + str(epsg_to)})
        a.to_file(basename + '_' + str(epsg_to) + '_reproj.shp')
        return None

    @staticmethod  # Get the desired column from the table via index, for generic usage
    def get_all_points_aslist(shape, number: int, fillval) -> (numpy.ndarray, [], []):
        data = gpd.read_file(shape)
        data.replace(to_replace="None", value=fillval, inplace=True)
        data.replace(to_replace=float('nan'), value=fillval, inplace=True)
        datar = numpy.vstack([data.centroid.x.values, data.centroid.y.values, data.values[:, number].astype('float')])
        idx = numpy.where(datar[2, :] != fillval)
        datar = datar[:, idx[0]]
        xvals = [min(datar[0]), max(datar[0])]
        yvals = [min(datar[1]), max(datar[1])]
        return datar, xvals, yvals

    @staticmethod
    # use e.g. 0.1 as float step input
    # Cubic Interpolation Do not use with sparse point data!
    def do_grid(table: numpy.ndarray, outfile: str, x: [], y: [], z: int, subname: str, step: float):
        lon = numpy.arange(x[0], x[1], step)
        lat = numpy.arange(y[0], y[1], step)
        lat = numpy.flip(lat)
        gridx, gridy = numpy.meshgrid(lon, lat)
        mapifo = "map info = {Geographic Lat/Lon,1, 1," + ' ' + str(numpy.min(gridx)) + ', ' + str(
            numpy.max(gridy)) + ', ' + str(step) + ', ' + str(step) + ",WGS-84}\n"
        print(mapifo)
        d = numpy.swapaxes(table[0:2, :], 0, 1)
        gridcd = interpolate.griddata(d, table[z, :], (gridx, gridy), method='cubic', fill_value=0)
        gridcd = numpy.nan_to_num(gridcd)
        namm = outfile + '_' + subname
        Rasterfun.schreibebsqsingle(gridcd, namm)
        open(namm + '.hdr', 'a').write(mapifo)
        return None

    # Kriging Please _do_ use with sparse point data as is the case in LPS!
    def do_krigrid(table: numpy.ndarray, outfile: str, x: [], y: [], z: int, subname: str, step: float):
        lon = numpy.arange(x[0], x[1], step)
        lat = numpy.arange(y[0], y[1], step)
        lat = numpy.flip(lat)
        gridx, gridy = numpy.meshgrid(lon, lat)
        mapifo = "map info = {Geographic Lat/Lon,1, 1," + ' ' + str(numpy.min(gridx)) + ', ' + str(
            numpy.max(gridy)) + ', ' + str(step) + ', ' + str(step) + ",WGS-84}\n"
        print(mapifo)
        okay = pykg.OrdinaryKriging(table[0, :], table[1, :], table[z, :], variogram_model="linear", verbose=False,
                                    enable_plotting=False)
        gridcd, semisari = okay.execute('grid', lon, lat)
        gridcd = numpy.nan_to_num(gridcd)
        namm = outfile + '_' + subname
        Rasterfun.schreibebsqsingle(gridcd, namm)
        open(namm + '.hdr', 'a').write(mapifo)
        return None
