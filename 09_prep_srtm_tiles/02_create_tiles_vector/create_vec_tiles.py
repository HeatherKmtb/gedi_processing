from typing import List
from osgeo import gdal
from osgeo import ogr

import rsgislib.vectorattrs

def create_wgs84_vector_grid(out_vec_file:str, out_vec_lyr:str, out_format:str, grid_x:int, grid_y:int, bbox:List[float], overlap:float=None, tile_names_col:str='tile_names', tile_name_prefix:str=''):
    """
    A function which creates a regular grid across a defined area using the
    WGS84 (EPSG 4236) projection.

    :param out_vec_file: output vector file
    :param out_vec_lyr: output vector layer name
    :param out_format: the output vector file format.
    :param grid_x: the size in the x axis of the grid cells.
    :param grid_y: the size in the y axis of the grid cells.
    :param bbox: the area for which cells will be defined (MinX, MaxX, MinY, MaxY).
    :param overlap: the overlap added to each grid cell. If None then no overlap applied.
    :param tile_names_col:
    :param tile_name_prefix:

    """
    import math
    import rsgislib.tools.projection
    import rsgislib.vectorattrs
    from rsgislib.vectorutils.createvectors import create_poly_vec_bboxs

    epsg_code = 4326
    min_x = float(bbox[0])
    max_x = float(bbox[1])
    min_y = float(bbox[2])
    max_y = float(bbox[3])
    grid_x = float(grid_x)
    grid_y = float(grid_y)

    n_x_cells = math.floor((max_x - min_x) / grid_x)
    x_remain = (max_x - min_x) - (grid_x * n_x_cells)

    n_y_cells = math.floor((max_y - min_y) / grid_y)
    y_remain = (max_y - min_y) - (grid_y * n_y_cells)

    print("Cells: [{0}, {1}]".format(n_x_cells, n_y_cells))

    bboxs = []
    tile_names = []
    for i in range(n_y_cells):
        c_max_y = max_y - (i * grid_y)
        c_min_y = c_max_y - grid_y
        for j in range(n_x_cells):
            c_min_x = min_x + (j * grid_x)
            c_max_x = c_min_x + grid_x
            lat_lon_str_name = rsgislib.tools.projection.get_deg_coord_as_str(lat=c_min_x, lon=c_max_y, n_chars=4)
            tile_names.append(f"{tile_name_prefix}{lat_lon_str_name}")
            if overlap is None:
                bboxs.append([c_min_x, c_max_x, c_min_y, c_max_y])
            else:
                bboxs.append([c_min_x - overlap, c_max_x + overlap, c_min_y - overlap,
                              c_max_y + overlap])
        if x_remain > 0:
            c_min_x = min_x + (n_x_cells * grid_x)
            c_max_x = c_min_x + x_remain
            lat_lon_str_name = rsgislib.tools.projection.get_deg_coord_as_str(lat=c_min_x, lon=c_max_y, n_chars=4)
            tile_names.append(f"{tile_name_prefix}{lat_lon_str_name}")
            if overlap is None:
                bboxs.append([c_min_x, c_max_x, c_min_y, c_max_y])
            else:
                bboxs.append([c_min_x - overlap, c_max_x + overlap, c_min_y - overlap,
                              c_max_y + overlap])
    if y_remain > 0:
        c_max_y = max_y - (n_y_cells * grid_y)
        c_min_y = c_max_y - y_remain
        for j in range(n_x_cells):
            c_min_x = min_x + (j * grid_x)
            c_max_x = c_min_x + grid_x
            lat_lon_str_name = rsgislib.tools.projection.get_deg_coord_as_str(lat=c_min_x, lon=c_max_y, n_chars=4)
            tile_names.append(f"{tile_name_prefix}{lat_lon_str_name}")
            if overlap is None:
                bboxs.append([c_min_x, c_max_x, c_min_y, c_max_y])
            else:
                bboxs.append([c_min_x - overlap, c_max_x + overlap, c_min_y - overlap,
                              c_max_y + overlap])
        if x_remain > 0:
            c_min_x = min_x + (n_x_cells * grid_x)
            c_max_x = c_min_x + x_remain
            lat_lon_str_name = rsgislib.tools.projection.get_deg_coord_as_str(lat=c_min_x, lon=c_max_y, n_chars=4)
            tile_names.append(f"{tile_name_prefix}{lat_lon_str_name}")
            if overlap is None:
                bboxs.append([c_min_x, c_max_x, c_min_y, c_max_y])
            else:
                bboxs.append([c_min_x - overlap, c_max_x + overlap, c_min_y - overlap,
                              c_max_y + overlap])

    for bbox in bboxs:
        if bbox[2] < -180:
            bbox[2] = -180
        if bbox[3] > 180:
            bbox[3] = 180

    create_poly_vec_bboxs(out_vec_file, out_vec_lyr, out_format, epsg_code, bboxs)
    rsgislib.vectorattrs.write_vec_column(out_vec_file, out_vec_lyr, tile_names_col, ogr.OFTString, tile_names)

create_wgs84_vector_grid('/scratch/a.hek4/gedi_files_2021_12_16/data/srtm_overlap_tiles.gpkg', 'srtm_tiles', 'GPKG', 1, 1, [-180, 180, -56, 60], overlap=0.0277777778, tile_name_prefix='srtm_')
rsgislib.vectorattrs.pop_bbox_cols('/scratch/a.hek4/gedi_files_2021_12_16/data/srtm_overlap_tiles.gpkg', 'srtm_tiles', x_min_col='xmin', x_max_col='xmax', y_min_col='ymin', y_max_col='ymax')

create_wgs84_vector_grid('/scratch/a.hek4/gedi_files_2021_12_16/data/srtm_tiles.gpkg', 'srtm_tiles', 'GPKG', 1, 1, [-180, 180, -56, 60], tile_name_prefix='srtm_')
rsgislib.vectorattrs.pop_bbox_cols('/scratch/a.hek4/gedi_files_2021_12_16/data/srtm_tiles.gpkg', 'srtm_tiles', x_min_col='xmin', x_max_col='xmax', y_min_col='ymin', y_max_col='ymax')


