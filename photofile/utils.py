import hashlib
import sys
import os
import logging
import shutil
from datetime import datetime
import time
from metadata import get_metadata, get_exif


# Sort of constants ;-)

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


def get_date_from_file(filename):
    """

    :param filename:
    :returns:
    """
    try:
        return get_metadata(filename).get('exif_date', None)
    except (Exception) as ex:
        st = os.stat(filename)
        return datetime.fromtimestamp(st.st_ctime > st.st_mtime and st.st_ctime or st.st_mtime)


def generate_filename_from_date(filename, file_date=None):
    """

    :param filename:
    :param file_date:
    """
    if not file_date:
        file_date = get_date_from_file(filename)

    filename = os.path.basename(filename)
    timestamp = file_date.strftime(timestamp_format)
    if timestamp in filename:
        filename = filename.replace(timestamp, '')

    fname, ext = os.path.splitext(filename)
    return new_filename_format % dict(filename=fname, timestamp=timestamp, file_extension=ext)


def generate_folders_from_date(file_date, tag=None):
    """

    :param file_date:
    :param tag:
    """
    if not tag:
        tag = str(file_date.day)
    return os.sep.join([str(file_date.year), months[file_date.month], tag])


def dirwalk(dir, extensions_to_include=None):
    """

    :param dir:
    :param extensions_to_include:
    """
    extensions_check = extensions_to_include is not None
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in dirwalk(fullpath, extensions_to_include):
                ext = os.path.splitext(x)[-1][1:].lower()
                if not extensions_check or ext in extensions_to_include:
                    yield x
        else:
            ext = os.path.splitext(fullpath)[-1][1:].lower()
            if not extensions_check or ext in extensions_to_include:
                yield fullpath


def get_files_in_folder(folder, extensions_to_include=None, sort_filenames=True):
    """

    :param folder:
    :param extensions_to_include:
    :param sort_filenames:
    """
    result = {}
    for filename in dirwalk(folder, extensions_to_include):
        path, filename = os.path.split(filename)
        result.setdefault(path, []).append(filename)

    if sort_filenames:
        for k, v in result.items():
            v.sort()
            v.reverse()

    return result


def get_photos_in_folder(folder):
    """

    :param folder:
    """
    return get_files_in_folder(folder, extensions_to_include=photo_extensions_to_include)


def get_tag_from_filename(filename, source_dir):
    """

    :param filename:
    :param source_dir:
    """
    result = os.path.split(filename)[0][len(source_dir):]

    if result and result[0] == os.sep:
        result = result[1:]

    return result


def relocate_photos(source_dir, target_dir=None, append_timestamp=True, remove_source=True, tag=None):
    """

    """
    if not target_dir:
        target_dir = source_dir

    photos = get_files_in_folder(source_dir, photo_extensions_to_include)
    for path, filenames in photos.items():
        current_tag = tag
        for filename in filenames:
            complete_filename = os.path.join(path, filename)
            if not current_tag:
                current_tag = get_tag_from_filename(complete_filename, source_dir)
            processed_file = relocate_photo(complete_filename, target_dir=target_dir, append_timestamp=append_timestamp,
                                            remove_source=remove_source, tag=current_tag)
            #if processed_file:
            #    yield processed_file

    if remove_source:
        remove_source_folders(photos.keys())


def generate_valid_target(filename):
    """

    :param filename:
    """
    counter = 1
    while 1:
        if not os.path.exists(filename):
            break
        fname, ext = os.path.splitext(filename)
        filename = duplicate_filename_format % dict(filename=fname, counter=counter, file_extension=ext)
        counter += 1
    return filename


def relocate_photo(filename, target_dir, file_date=None, append_timestamp=True, remove_source=True, tag=None,
                   skip_existing=False, path_prefix=None):
    """

    :param filename:
    :param target_dir:
    :param file_date:
    :param append_timestamp:
    :param remove_source:
    :param tag:
    :param skip_existing:
    :param path_prefix:
    """
    if not file_date:
        file_date = get_date_from_file(filename)

    if path_prefix and path_prefix not in os.listdir(target_dir):
        target_dir = os.path.join(target_dir, path_prefix, generate_folders_from_date(file_date, tag))
    else:
        target_dir = os.path.join(target_dir, generate_folders_from_date(file_date, tag))

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    new_filename = os.path.join(target_dir, append_timestamp and generate_filename_from_date(filename, file_date) or
                                            os.path.basename(filename))

    if skip_existing and os.path.exists(new_filename):
        return

    new_filename = generate_valid_target(new_filename)
    logging.debug("%s -> %s" % (filename, new_filename))

    if remove_source:
        shutil.move(filename, new_filename)
    else:
        shutil.copy(filename, new_filename)

    return new_filename


def remove_source_folders(folders):
    """

    """
    for folder in folders:
        if len(list(dirwalk(folder))) == 0:
            os.removedirs(folder)


def find_duplicates(source_folder, target_folder, delete_duplicates=False, verbose=False):
    """

    """
    source_files = {}
    target_files = {}
    if verbose: logging.debug("Scanning source folder ..."),
    for filename in dirwalk(source_folder):
        st = os.stat(filename)
        source_files.setdefault(st.st_size, []).append((filename, st))
    if verbose: logging.debug("done!")

    if verbose: logging.debug("Scanning target folder ..."),
    for filename in dirwalk(target_folder):
        st = os.stat(filename)
        target_files.setdefault(st.st_size, []).append((filename, st))
    if verbose: logging.debug("done!")

    if verbose: logging.debug("Locating duplicates:")
    for filesize, filedata in target_files.items():
        existing_files = source_files.get(filesize, [])
        for existing_filename, existing_st in existing_files:
            for filename, st in filedata:
                existing_ctime = st.st_mtime < st.st_ctime and st.st_mtime or st.st_ctime
                st_ctime = existing_st.st_mtime < existing_st.st_ctime and existing_st.st_mtime or existing_st.st_ctime
                if existing_ctime == st_ctime:
                    if delete_duplicates:
                        os.remove(filename)
                    if verbose: logging.debug("%s appears to be a duplicate of %s." % (filename, existing_filename))
                    yield filename


def get_checksum(filename):
    """

    :param filename:
    """
    fname, ext = os.path.splitext(filename)
    if ext:
        if ext[1:].lower() in photo_extensions_to_include:
            if 1:  #try:
                exif = get_exif(filename)
                return str(
                    time.strptime(exif.get('DateTime', exif.get('DateTimeOriginal', exif.get('DateTimeDigitized'))),
                                  "%Y:%m:%d %H:%M:%S"))
                #except Exception, e:
                #    logging.debug("Error using PIL on %s: %s." % (filename, e))

    f = open(filename)
    result = hashlib.sha512()
    while 1:
        data = f.read(4096)
        if not data:
            break
        result.update(data)
    return result.hexdigest()


def build_file_cache(path):
    """

    """
    result = {}
    for filename in dirwalk(path):
        p, f = os.path.split(filename)
        if f.lower() in ignore_files:
            continue
        st = os.stat(filename)
        result.setdefault(st.st_size, []).append(filename)
    return result


def find_new_files(source_folder, target_folder, verbose=False):
    """

    :param source_folder:
    :param target_folder:
    :param verbose:
    """
    if verbose: logging.debug("Scanning source folder ..."),
    source_files = build_file_cache(source_folder)
    if verbose: logging.debug("done!")

    if verbose: logging.debug("Scanning target folder ..."),
    target_files = build_file_cache(target_folder)
    if verbose: logging.debug("done!")

    sha_cache = {}
    if verbose: logging.debug("Locating new content:")
    for filesize, filenames in target_files.items():
        if not filesize in source_files.keys():
            for filename in filenames:
                if verbose: logging.debug(filename)
                yield filename
        else:
            for existing_filename in source_files[filesize]:
                for filename in filenames:

                    if existing_filename[:8] == filename[:8]:
                        continue

                    if not existing_filename in sha_cache:
                        sha_cache[existing_filename] = get_checksum(existing_filename)

                    if not filename in sha_cache:
                        sha_cache[filename] = get_checksum(filename)

                    if sha_cache[existing_filename] != sha_cache[filename]:
                        if verbose: logging.debug filename
                        yield filename


def print_tag(sourcefolder):
    """

    :param sourcefolder:
    """
    for filename in dirwalk(sourcefolder):
        print(filename, get_tag_from_filename(filename, sourcefolder))


def clean_up(sourcefolder):
    """

    :param sourcefolder:
    """
    logging.debug("Cleaning up %s" % sourcefolder)
    for filename in dirwalk(sourcefolder):
        if os.path.basename(filename) in ignore_files:
            os.remove(filename)

    paths = {}
    for path in [os.path.join(sourcefolder, path) for path in os.listdir(sourcefolder)]:

        if os.path.isdir(path):
            paths[os.path.join(sourcefolder, path)] = []

    for filename in dirwalk(sourcefolder):
        path, filename = os.path.split(filename)
        paths.setdefault(path, []).append(filename)

    path_names = paths.keys()
    path_names.sort()
    path_names.reverse()
    for path in path_names:
        if not paths[path]:
            try:
                os.removedirs(path)
            except (Exception) as e:
                logging.debug("Error removing %s because %s." % (path, e))


def relocate_movies(source_dir, target_dir=None, append_timestamp=True, remove_source=True, tag=None):
    """

    :param source_dir:
    :param target_dir:
    :param append_timestamp:
    :param remove_source:
    :param tag:
    """
    if not target_dir:
        target_dir = source_dir

    movies = get_files_in_folder(source_dir, movie_extensions_to_include)
    for path, filenames in movies.items():
        current_tag = tag
        for filename in filenames:
            complete_filename = os.path.join(path, filename)
            if not current_tag:
                current_tag = get_tag_from_filename(complete_filename, source_dir)
            relocate_movie(complete_filename, target_dir=target_dir, append_timestamp=append_timestamp,
                           remove_source=remove_source, tag=current_tag)

    if remove_source:
        remove_source_folders(movies.keys())


def relocate_movie(filename, target_dir, append_timestamp=True, remove_source=True, tag=None, skip_existing=False,
                   path_prefix=None):
    """

    :param filename:
    :param target_dir:
    :param append_timestamp:
    :param remove_source:
    :param tag:
    :param skip_existing:
    :param path_prefix:
    """
    st = os.stat(filename)
    date = st.st_ctime < st.st_mtime and datetime.fromtimestamp(st.st_ctime) or datetime.fromtimestamp(st.st_mtime)

    if path_prefix:
        target_dir = os.path.join(target_dir, path_prefix, generate_folders_from_date(date, tag))
    else:
        target_dir = os.path.join(target_dir, generate_folders_from_date(date, tag))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    new_filename = os.path.join(target_dir,
                                append_timestamp and generate_filename_from_date(filename, date) or os.path.basename(
                                    filename))
    new_filename = generate_valid_target(new_filename)

    if skip_existing and os.path.exists(new_filename):
        return

    if remove_source:
        shutil.move(filename, new_filename)
    else:
        shutil.copy(filename, new_filename)

    return new_filename

#coding=utf-8
import os
import logging
from PIL import Image
from PIL.ExifTags import TAGS
from metadata import get_exif


def generate_thumb(media_folder, absolute_filename, width, height, do_crop, alternative_thumbnail_name=None, raise_exception_on_error = False):
    """

    :param media_folder:
    :param absolute_filename:
    :param width:
    :param height:
    :param do_crop:
    :param alternative_thumbnail_name:
    :param raise_exception_on_error:
    """
    logging.debug("Generating thumb: %s" % absolute_filename)

    fname, ext = os.path.splitext(os.path.basename(absolute_filename))
    if alternative_thumbnail_name:
        fname = alternative_thumbnail_name
    resized_image = '%s_%sx%s%s%s' % (fname, width, height, do_crop and '_crop' or '',ext)

    if not os.path.exists(absolute_filename):
        logging.warning("inputfile %s does not exists" % absolute_filename)
        if raise_exception_on_error:
            raise Exception('Inputfile "%s" does not exists.' % absolute_filename)
        return 'inputfile does not exists'

    thumb_dir = os.path.join(media_folder, 'thumbs')

    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)

    output = os.path.join(thumb_dir, resized_image)
    final_url = "%sthumbs/%s" % (settings.MEDIA_URL, resized_image)

    if not os.path.exists(output):
        try:
            resize_image(absolute_filename, output, width, height, crop=do_crop)
        except (Exception) as ex:
            logging.warning(ex)

    return final_url


def resize_image(source_file, target_file, width, height, crop=False):
    """
    Resizes an image specified by source_file and writes output to target_file.
    Will read EXIF data from source_file, look for information about orientation
    and rotate photo if such info is found.

    :param source_file:
    :param target_file:
    :param width:
    :param height:
    :param crop:
    """
    image = Image.open(source_file)
    orientation = 0
    try:
        for tag, value in image._getexif().items():
            if TAGS.get(tag, tag) == 'Orientation':
                orientation = value
    except (Exception) as ex:
        logging.warning(ex)
        orientation = None

    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    if not crop:
        image.thumbnail((width, height), Image.ANTIALIAS)
    else:
        src_width, src_height = image.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = width, height
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = int(float(src_width - crop_width) / 2)
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = int(float(src_height - crop_height) / 3)
        image = image.crop((x_offset, y_offset, x_offset+int(crop_width), y_offset+int(crop_height)))
        image = image.resize((int(dst_width), int(dst_height)), Image.ANTIALIAS)

    # rotate according to orientation stored in exif-data:
    if orientation:
        if orientation == 2:
            # Vertical Mirror
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # Rotation 180°
            image = image.transpose(Image.ROTATE_180)
        elif orientation == 4:
            # Horizontal Mirror
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == 5:
            # Horizontal Mirror + Rotation 270°
            image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
        elif orientation == 6:
            # Rotation 270°
            image = image.transpose(Image.ROTATE_270)
        elif orientation == 7:
            # Vertical Mirror + Rotation 270°
            image = image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
        elif orientation == 8:
            # Rotation 90°
            image = image.transpose(Image.ROTATE_90)

    image.save(target_file)
