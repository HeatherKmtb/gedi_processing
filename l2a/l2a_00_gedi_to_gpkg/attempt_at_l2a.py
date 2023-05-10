#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 08:51:17 2023

@author: heatherkay
"""

import datetime
import logging

import geopandas
import h5py
import pandas
import numpy

logger = logging.getLogger(__name__)

def get_beam_lst(input_file):
    """
    A function which returns a list of beam names.
    :param input_file: input file path.
    :return: list of strings
    """
    gedi_h5_file = h5py.File(input_file, "r")
    gedi_keys = list(gedi_h5_file.keys())
    gedi_beams = [
        "BEAM0000",
        "BEAM0001",
        "BEAM0010",
        "BEAM0011",
        "BEAM0101",
        "BEAM0110",
        "BEAM1000",
        "BEAM1011",
    ]
    gedi_beams_lst = []
    for gedi_beam_name in gedi_keys:
        if gedi_beam_name in gedi_beams:
            gedi_beams_lst.append(gedi_beam_name)
    gedi_h5_file.close()
    return gedi_beams_lst

def get_metadata(input_file):
    """
    A function which returns a dict of the file metadata.
    :param input_file: input file path.
    :return: dict with the metadata.
    """
    gedi_h5_file = h5py.File(input_file, "r")

    file_att_keys = list(gedi_h5_file.attrs.keys())
    if "short_name" in file_att_keys:
        gedi_short_name = gedi_h5_file.attrs["short_name"]
    else:
        raise Exception("Could not find the GEDI file short name - valid file?")

    metadata_dict = dict()
    if gedi_short_name == "GEDI_L2A":
        gedi_keys = list(gedi_h5_file.keys())

        if "METADATA" in gedi_keys:
            gedi_metadata_keys = list(gedi_h5_file["METADATA"])
            if "DatasetIdentification" in gedi_metadata_keys:
                metadata_dict["version_id"] = gedi_h5_file["METADATA"][
                    "DatasetIdentification"
                ].attrs["VersionID"]
                metadata_dict["pge_version"] = gedi_h5_file["METADATA"][
                    "DatasetIdentification"
                ].attrs["PGEVersion"]
                creation_date_str = gedi_h5_file["METADATA"][
                    "DatasetIdentification"
                ].attrs["creationDate"]
                metadata_dict["creation_date"] = datetime.datetime.strptime(
                    creation_date_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                metadata_dict["file_uuid"] = gedi_h5_file["METADATA"][
                    "DatasetIdentification"
                ].attrs["uuid"]
            else:
                raise Exception(
                    "No metadata DatasetIdentification directory - is this file valid?"
                )
        else:
            raise Exception("No metadata directory - is this file valid?")
    else:
        raise Exception(
            "The input file must be a GEDI_L2A - not implemented for other products yet."
        )
    gedi_h5_file.close()
    return metadata_dict



def get_gedi02_b_beam_as_gdf(
    input_file, gedi_beam_name, valid_only=True, out_epsg_code=4326
):
    """
    A function which gets a geopandas dataframe for a beam. Note the parameters
    with multiple values in the z axis are not included in the dataframe.
    :param input_file: input file path.
    :param gedi_beam_name: the name of the beam to be processed.
    :param valid_only: If True (default) then returns which are labelled as invalid
                       are removed from the dataframe.
    :param out_epsg_code: If provided the returns will be reprojected to the EPSG
                          code provided. default is EPSG:4326
    """
    gedi_beams = get_beam_lst(input_file)
    if gedi_beam_name not in gedi_beams:
        raise Exception(
            "Beam '{}' is not available within the file: {}".format(
                gedi_beam_name, input_file
            )
        )

    gedi_h5_file = h5py.File(input_file, "r")

    file_att_keys = list(gedi_h5_file.attrs.keys())
    if "short_name" in file_att_keys:
        gedi_short_name = gedi_h5_file.attrs["short_name"]
    else:
        raise Exception("Could not find the GEDI file short name - valid file?")

    if gedi_short_name != "GEDI_L2A":
        raise Exception("The input file must be a GEDI_L2A.")

    logger.debug("Creating geopandas dataframe for beam: {}".format(gedi_beam_name))
    gedi_beam = gedi_h5_file[gedi_beam_name]
    gedi_beam_keys = list(gedi_beam.keys())

    # Get location info.
    #gedi_beam_geoloc = gedi_beam["geolocation"]
    # Get land cover data.
    #gedi_beam_landcover = gedi_beam["land_cover_data"]
    
    gedi_beam_dict = dict()
    for i in range(101):
        gedi_beam_dict[f"rh_{i}"] = gedi_beam["rh"][...,i]
    gedi_beam_dict["quality_flag"] = gedi_beam["quality_flag"]
    gedi_beam_dict["shot_number"] = gedi_beam["shot_number"]
    gedi_beam_dict["lat_highestreturn"] = gedi_beam["lat_highestreturn"]
    gedi_beam_dict["lat_lowestmode"] = gedi_beam["lat_lowestmode"]
    gedi_beam_dict["lon_highestreturn"] = gedi_beam["lon_highestreturn"]
    gedi_beam_dict["lon_lowestmode"] = gedi_beam["lon_lowestmode"]

    gedi_beam_df = pandas.DataFrame(gedi_beam_dict)

    gedi_beam_gdf = geopandas.GeoDataFrame(
        gedi_beam_df,
        crs="EPSG:4326",
        geometry=geopandas.points_from_xy(
            gedi_beam_df.lon_lowestmode, gedi_beam_df.lat_lowestmode
        ),
    )
#do I need to take this out? Or add in "quality_flag" above
    if valid_only:
        logger.debug(
            "Masking beam {} so only valid returns remain".format(gedi_beam_name)
        )
        gedi_beam_gdf = gedi_beam_gdf[
            (gedi_beam_gdf.quality_flag == 1)
        ]
    if out_epsg_code != 4326:
        logger.debug(
            "Reprojecting beam {} to EPSG:{}.".format(gedi_beam_name, out_epsg_code)
        )
        gedi_beam_gdf = gedi_beam_gdf.to_crs("EPSG:{}".format(out_epsg_code))
    gedi_h5_file.close()
    logger.debug(
        "Finished creating geopandas dataframe for beam: {}".format(gedi_beam_name)
    )
    return gedi_beam_gdf


def gedi02_a_beams_gpkg(input_file, out_vec_file, valid_only=True, out_epsg_code=4326):
    """
    A function which converts all the beams to a GPKG vector file with each beam
    as a different layer within the vector file.
    :param input_file: input file path.
    :param out_vec_file: output file path
    :param gedi_beam_name: the name of the beam to be processed.
    :param valid_only: If True (default) then returns which are labelled as invalid
                       are removed from the dataframe.
    :param out_epsg_code: If provided the returns will be reprojected to the
                          EPSG code provided. default is EPSG:4326
    """
    gedi_beams = get_beam_lst(input_file)
    for gedi_beam_name in gedi_beams:
        logger.info("Processing beam '{}'".format(gedi_beam_name))
        gedi_beam_gdf = get_gedi02_b_beam_as_gdf(
            input_file, gedi_beam_name, valid_only, out_epsg_code
        )
        gedi_beam_gdf.to_file(out_vec_file, layer=gedi_beam_name, driver="GPKG")
        logger.info("Finished processing beam '{}'".format(gedi_beam_name))
        
        
#gedi02_a_beams_gpkg(input_file="/Users/heatherkay/q_res/gedi/GEDI02_A_2020181135634_O08762_03_T03753_02_003_01_V002.h5", out_vec_file="/Users/heatherkay/q_res/gedi/GEDI02_A_2020181135634_O08762_03_T03753_02_003_01_V002.gpkg", valid_only=False, out_epsg_code=4326)
