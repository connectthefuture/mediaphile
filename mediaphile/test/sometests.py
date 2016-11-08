import sys
from mediaphile.lib import months
from mediaphile.lib.file_operations import generate_filename_from_date, generate_folders_from_date
from mediaphile.lib.metadata import get_metadata, get_parsed_metadata
from mediaphile.lib.photos import get_photos_in_folder

fname = sys.argv[1]
print(get_parsed_metadata(fname))
