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
    return Decimal(Decimal(coordelement) / Decimal(1000))


def meters_to_feet(ele_meters):
    multiplier = Decimal(3.28084)
    elevation = Decimal(ele_meters)
    return elevation * multiplier


def meters_sec_to_kts(inspeed):
    multiplier = Decimal(1.94384)
    if inspeed == '9999':
        return Decimal(9999)
    return Decimal(Decimal(inspeed) * multiplier)

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
    'obs_elevation_feet': {
        'loc': slice(46, 51),
        'datatype': meters_to_feet
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
        'datatype': int
    },
    'wind_speed_kts': {
        'loc': slice(65, 69),
        'datatype': meters_sec_to_kts
    },
    'wind_obs_spd_qual_code': {
        'loc': slice(69, 70),
        'datatype': str
    },
}
