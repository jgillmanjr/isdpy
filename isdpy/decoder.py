"""
Basically a dictionary used for decoding a record

Based off of ftp://ftp.ncdc.noaa.gov/pub/data/noaa/ish-format-document.pdf
"""
import datetime
from decimal import Decimal

# Any functions that serve as 'data types' for processing the data


def dtgutc(dtgstring):
    return datetime.datetime.strptime(dtgstring, '%Y%m%d%H%M')


def scalecoordinate(coordelement):
    return Decimal(coordelement) / Decimal(1000)


def meters_to_feet(ele_meters):
    multiplier = Decimal(3.28084)
    elevation = Decimal(ele_meters)
    return elevation * multiplier


def obs_elevation_feet(ele_meters):
    if ele_meters == '+9999':
        return int(ele_meters)
    return meters_to_feet(ele_meters)


def ceiling_height_feet(ht_meters):
    if ht_meters == '99999':
        return int(ht_meters)
    return meters_to_feet(ht_meters)


def scale_down_ten(numeric_input):
    return Decimal(numeric_input) / Decimal(10)


def meters_sec_to_kts(inspeed):
    multiplier = Decimal(1.94384)
    if inspeed == '9999':
        return Decimal(9999)
    return scale_down_ten(inspeed) * multiplier


def meter_to_stat_mile(distance):
    multiplier = Decimal(0.000621371)
    return Decimal(distance) * multiplier


def scale_air_temp(airtemp):
    if airtemp == '+9999':
        return Decimal(airtemp)
    return scale_down_ten(airtemp)


def scale_sea_lvl_prs_hecto(pressure):
    if pressure == '99999':
        return Decimal(pressure)
    return scale_down_ten(pressure)


def sea_lvl_prs_in_hg(kpprs):
    multiplier = Decimal(0.2953)
    if kpprs == '99999':
        return Decimal(kpprs)
    return scale_down_ten(kpprs) * multiplier

# End Functions


datamap = {
    'total_var_chars': {
        'loc': slice(0, 4),
        'datatype': int
    },
    'usaf_id': {
        'loc': slice(4, 10),
        'datatype': str
    },
    'wban_id': {
        'loc': slice(10, 15),
        'datatype': str
    },
    'obs_dtg_utc': {
        'loc': slice(15, 27),
        'datatype': dtgutc
    },
    'obs_src_flag': {
        'loc': slice(27, 28),
        'datatype': str
    },
    'obs_lat_dec': {
        'loc': slice(28, 34),
        'datatype': scalecoordinate
    },
    'obs_lon_dec': {
        'loc': slice(34, 41),
        'datatype': scalecoordinate
    },
    'report_type_code': {
        'loc': slice(41, 46),
        'datatype': str
    },
    'obs_elevation_meter': {
        'loc': slice(46, 51),
        'datatype': int
    },
    'station_call_id': {
        'loc': slice(51, 56),
        'datatype': str
    },
    'obs_quality_proc_name': {
        'loc': slice(56, 60),
        'datatype': str
    },
    'wind_direction_true': {
        'loc': slice(60, 63),
        'datatype': int
    },
    'wind_dir_qual_code': {
        'loc': slice(63, 64),
        'datatype': str
    },
    'wind_obs_type_code': {
        'loc': slice(64, 65),
        'datatype': str
    },
    'wind_speed_meters_sec': {
        'loc': slice(65, 69),
        'datatype': scale_down_ten
    },
    'wind_obs_spd_qual_code': {
        'loc': slice(69, 70),
        'datatype': str
    },
    'ceiling_height_meters': {
        'loc': slice(70, 75),
        'datatype': int
    },
    'ceiling_height_qual_code': {
        'loc': slice(75, 76),
        'datatype': str
    },
    'ceiling_determ_code': {
        'loc': slice(76, 77),
        'datatype': str
    },
    'cavok_code': {
        'loc': slice(77, 78),
        'datatype': str
    },
    'visibility_meters': {
        'loc': slice(78, 84),
        'datatype': int
    },
    'visibility_qual_code': {
        'loc': slice(84, 85),
        'datatype': str
    },
    'vis_variability_code': {
        'loc': slice(85, 86),
        'datatype': str
    },
    'vis_var_qual_code': {
        'loc': slice(86, 87),
        'datatype': str
    },
    'air_temp_c': {
        'loc': slice(87, 92),
        'datatype': scale_air_temp
    },
    'air_temp_qual_code': {
        'loc': slice(92, 93),
        'datatype': str
    },
    'dew_point_c': {
        'loc': slice(93, 98),
        'datatype': scale_air_temp
    },
    'dew_point_qual_code': {
        'loc': slice(98, 99),
        'datatype': str
    },
    'sea_lvl_prs_hectopscl': {
        'loc': slice(99, 104),
        'datatype': scale_sea_lvl_prs_hecto
    },
    'sea_lvl_prs_qual_code': {
        'loc': slice(104, 105),
        'datatype': str
    },
    'start_additional_data_here': {
        'loc': slice(105, 108),
        'datatype': str
    },
    'lqd_prcp_start': {
        'loc': slice(108, 111),
        'datatype': str
    },
    'lqd_prcp_measure_hours': {
        'loc': slice(111, 113),
        'datatype': int
    },
    'lqd_prcp_depth_mm': {
        'loc': slice(113, 117),
        'datatype': scale_down_ten
    },
    'lqd_prcp_cond_code': {
        'loc': slice(117, 118),
        'datatype': str
    },
    'lqd_prcp_qual_code': {
        'loc': slice(118, 119),
        'datatype': str
    },
    # "Custom" mappings below
    'obs_elevation_feet': {
        'loc': slice(46, 51),
        'datatype': obs_elevation_feet
    },
    'wind_speed_kts': {
        'loc': slice(65, 69),
        'datatype': meters_sec_to_kts
    },
    'ceiling_height_feet': {
        'loc': slice(70, 75),
        'datatype': ceiling_height_feet
    },
    'visibility_statute_miles': {
        'loc': slice(78, 84),
        'datatype': meter_to_stat_mile
    },
    'sea_lvl_prs_in_hg': {
        'loc': slice(99, 104),
        'datatype': sea_lvl_prs_in_hg
    },
}
