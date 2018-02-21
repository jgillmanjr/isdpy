import csv
import io
import datetime
import gzip
from operator import itemgetter
from ftplib import FTP  # Why can't the requests library support FTP?
from isdpy.decoder import datamap

ISD_HOST = 'ftp.ncdc.noaa.gov'
BASE_ISD_PATH = '/pub/data/noaa/'
HISTORY_FILE_NAME = 'isd-history.csv'
ISD_FILE_DATE_FORMAT = '%Y%m%d'


class StationList:
    def __init__(self, station_dict):
        self.station_dict = station_dict

    def get_icao_station_filenames(self, station_icao, year):
        init_list = []
        station_key = station_icao.upper()
        if station_key in self.station_dict:
            for entry in self.station_dict[station_key]:
                start = entry['start_date']
                end = entry['end_date']
                if not (start <= datetime.date(int(year), 1, 1) <= end):  # Exclude matches outside the year
                    continue
                usaf = entry['usaf_id']
                wban = entry['wban_id']
                init_list.append(
                    {
                        'filename': usaf + '-' + wban + '-' + str(year) + '.gz',
                        'base_file': usaf + '-' + wban + '-' + str(year),
                        'start_date': start.strftime(ISD_FILE_DATE_FORMAT),
                        'end_date': end.strftime(ISD_FILE_DATE_FORMAT),
                    }
                )
        return sorted(init_list, key=itemgetter('start_date'), reverse=True)  # Sort by start date

    def download_latest_icao(self, station_icao, year):
        top_file = self.get_icao_station_filenames(station_icao, year)[0]
        gzfile = get_ftp(filename=top_file['filename'], path=BASE_ISD_PATH + str(year), keep_bytes=True)
        return bytes_to_line_array(gzip.decompress(gzfile))

    def decode_record(self, record, datamap=datamap):
        decoded_dict = {}
        for k, v in datamap.items():
            datatype = v['datatype']
            loc = v['loc']
            decoded_dict[k] = datatype(record[loc]).strip() if datatype is str else datatype(record[loc])

        return decoded_dict


def bytes_to_line_array(bobj, encoding='utf-8'):
    return bobj.decode(encoding).splitlines()


def get_ftp(filename, host=ISD_HOST, path=BASE_ISD_PATH, keep_bytes=False):
    """
    Did you know that requests should support FTP??
    But, because it doesn't, shenanigans ensue...
    So, yeah, return a list of lines... this is why I drink... that and I suck at python
    Unless you want to keep it binary..
    """
    ftp_byte_stream = io.BytesIO()

    with FTP(host=host) as ftp:
        ftp.login()
        ftp.cwd(path)
        ftp.retrbinary('RETR ' + filename, ftp_byte_stream.write)
        ftp_byte_stream.seek(0)

    if not keep_bytes:
        return bytes_to_line_array(ftp_byte_stream.read())  # Return the line array

    return ftp_byte_stream.read()  # Return the byte object


def get_stations_with_icao():
    # For now, just get stations that have an ICAO code
    station_dict = {}

    station_data = get_ftp(host=ISD_HOST, path=BASE_ISD_PATH, filename=HISTORY_FILE_NAME)

    cr = csv.DictReader(station_data, delimiter=',')
    for line in cr:
        icao = line['ICAO'].upper()

        if icao == '':
            continue

        if icao not in station_dict:
            station_dict[icao] = []

        station_dict[icao].append(
            {
                'start_date': datetime.datetime.strptime(line['BEGIN'], ISD_FILE_DATE_FORMAT).date(),
                'end_date': datetime.datetime.strptime(line['END'], ISD_FILE_DATE_FORMAT).date(),
                'name': line['STATION NAME'],
                'usaf_id': line['USAF'],
                'wban_id': line['WBAN'],
                'state': line['STATE'],
                'country': line['CTRY'],
            }
        )

    return StationList(station_dict=station_dict)
