import sys
from mediaphile.lib.photos import MpsPhoto

fname = sys.argv[1]
x = MpsPhoto(fname, context={'username': 'Thomas', 'main archive': '/opt/archive/data'})
print(x.build_target_path('username', 'year', 'month_name', 'day', 'model'))
print(x.build_target_filename('filename', '_', 'year', 'month','day', '_', 'hour', 'minute', 'second', 'file_extension'))
y = ('username', '_', 'filename', '_', 'timestamp', 'file_extension')
print(x.build_target_filename(*y))
