# Sort of constants ;-)
from datetime import datetime

months = {}
if not months:
    for month in range(1, 12 + 1):
        date = datetime(1900, month, 1)
        months[month] = date.strftime('%B')


photo_extensions_to_include = (
    'jpg',
    'nef',
    'png',
    'bmp',
    'gif',
    'cr2',
    'tif',
    'tiff',
    'jpeg',
)

movie_extensions_to_include = (
    'avi',
    'mov',
    'mp4',
    'mpg',
    'mts',
    'mpeg',
    'mkv',
    '3gp',
    'wmv',
    'm2t',
)

timestamp_format = '%Y%m%d_%H%M%S%f'
duplicate_filename_format = '%(filename)s~%(counter)s%(file_extension)s'
new_filename_format = "%(filename)s_%(timestamp)s%(file_extension)s"
ignore_files = ('thumbs.db', 'pspbrwse.jbf', 'picasa.ini', 'autorun.inf', 'hpothb07.dat',)
#FOLDERS_TO_SKIP = ('DCIM','100_FUJI'.'100CASIO',)
