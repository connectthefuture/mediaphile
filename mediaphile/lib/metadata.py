#coding=utf-8
import os
import time
import datetime
import re
import exifread
from file_operations import creation_date
from mediaphile.lib import months


# Credits http://eran.sandler.co.il/2011/05/20/extract-gps-latitude-and-longitude-data-from-exif-using-python-imaging-library-pil/
def _frac_to_simple(frac):
    """

    """
    if not frac:
        return None
    try:
        f, n = frac
        return round(float(f) / float(n), 3)
    except (Exception):
        return None


def _convert_to_degrees(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format

    :param value:
    :returns:
    """
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def extract_location_data(data):
    """

    :param data:
    :returns:
    """
    try:
        location_name = ', '.join(data['Iptc.Application2.LocationName'].values)
    except:
        location_name = None

    try:
        city = ', '.join(data['Iptc.Application2.City'].values)
    except:
        city = None

    try:
        province_state = ', '.join(data['Iptc.Application2.ProvinceState'].values)
    except:
        province_state = None

    try:
        country_code = ', '.join(data['Iptc.Application2.CountryCode'].values)
    except:
        country_code = None

    try:
        country_name = ', '.join(data['Iptc.Application2.CountryName'].values)
    except KeyError:
        country_name = None

    return location_name, city, province_state, country_code, country_name


def extract_gps_info(data):
    """
    Extracts longitude, latitude and altitude from EXIF metadata.

    :param data:
    """
    # http://linfiniti.com/2009/06/reading-geotagging-data-from-blackberry-camera-images/
    try:
        # Will be either 'E' or 'W'
        my_lon_direction = data['Exif.GPSInfo.GPSLongitudeRef']
        # Will return a rational number like : '27/1'
        my_lon_degrees = data['Exif.GPSInfo.GPSLongitude'][0]
        # Will return a rational number like : '53295/1000'
        my_lon_minutes = data['Exif.GPSInfo.GPSLongitude'][1]
        # Will be either 'N' or 'S'
        my_lat_direction = data['Exif.GPSInfo.GPSLatitudeRef']
        # Will return a rational number like : '27/1'
        my_lat_degrees = data['Exif.GPSInfo.GPSLatitude'][0]
        # Will return a rational number like : '56101/1000'
        my_lat_minutes = data['Exif.GPSInfo.GPSLatitude'][1]
    except:
        return None, None, None

    # Get the degree and minute values
    my_reg_exp = re.compile('^[0-9]*')
    my_lon_degrees_float = float(my_reg_exp.search(str(my_lon_degrees)).group())
    my_lat_degrees_float = float(my_reg_exp.search(str(my_lat_degrees)).group())
    my_lon_minutes_float = float(my_reg_exp.search(str(my_lon_minutes)).group())
    my_lat_minutes_float = float(my_reg_exp.search(str(my_lat_minutes)).group())

    # Divide the values by the divisor
    my_reg_exp = re.compile('[0-9]*$')
    my_lon = my_lon_degrees_float / float(my_reg_exp.search(str(my_lon_degrees)).group())
    my_lat = my_lat_degrees_float / float(my_reg_exp.search(str(my_lat_degrees)).group())
    my_lon_min = my_lon_minutes_float / float(my_reg_exp.search(str(my_lon_minutes)).group())
    my_lat_min = my_lat_minutes_float / float(my_reg_exp.search(str(my_lat_minutes)).group())

    # We now have degrees and decimal minutes, so convert to decimal degrees...
    my_lon += my_lon_min / 60
    my_lat += my_lat_min / 60

    # Use a negative sign as needed
    if my_lon_direction == 'W':
        my_lon = 0 - my_lon

    if my_lat_direction == 'S':
        my_lat = 0 - my_lat

    altitude = 'Exif.GPSInfo.GPSAltitude' in data and data['Exif.GPSInfo.GPSAltitude'][0] or None

    return my_lon, my_lat, altitude


def get_metadata(filename, details=False):
    """

    :param filename:
    :return:
    """
    path, filename = os.path.split(filename)
    path = os.path.abspath(path)
    filename, ext = os.path.splitext(filename)
    complete_filename = os.path.join(path, filename+ext)

    f = open(complete_filename, 'rb')
    tags = exifread.process_file(f, details=details)
    result = {'CreationDate': creation_date(complete_filename)}

    if not tags:
        return result

    for tag in tags.keys():
        print("%s=%s" %(tag, tags[tag]))

        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            result[tag] = tags[tag]

    if 'EXIF DateTimeDigitized' in result:
        result['EXIF Date'] = datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(str(result['EXIF DateTimeDigitized']), "%Y:%m:%d %H:%M:%S")))

    return result
    #     result['exposure_time'] = _frac_to_simple(metadata.get("ExposureTime", metadata.get('ShutterSpeedValue', 0)))
    #     result['fnumber'] = _frac_to_simple(metadata.get("FNumber", -1.0))
    #     result['focal_length'] = _frac_to_simple(metadata.get("FocalLength", -1.0))


def get_parsed_metadata(filename, params=None):
    """

    :param filename:
    :return:
    """
    if not params:
        params = get_metadata(filename, True)

    dt = params['EXIF Date'] or params['CreationDate']
    dtt = dt.timetuple()
    ts = time.mktime(dtt)

    path, fname = os.path.split(filename)
    fname, ext = os.path.splitext(fname)

    result = {
        'year': dt.year,
        'month_name': months.get(dt.month, None),
        'day': dt.day,
        'filename': fname,
        'month': dt.month,
        'hour': dt.hour,
        'minute': dt.minute,
        'second': dt.second,
        'microsecond': dt.microsecond,
        'file_extension': ext,
        'model': str(params.get('Image Model', '')),
        'make': str(params.get('Image Make', '')),
        'path': path,
        'date': dt,
        'timestamp': int(ts)
    }

    return result