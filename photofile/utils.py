#coding=utf-8
import os
import logging
import hashlib
import shutil
from datetime import datetime
import time
from PIL import Image
from PIL.ExifTags import TAGS
from metadata import get_metadata, get_exif
from photofile.constants import *


def get_date_from_file(filename):
    """
    Get the creation date from the specified filename, either from the EXIF-metadata or the creation-date of the file
    it EXIF-data is not available.

    @param filename: the file to process
    @returns: datetime
    """
    try:
        return get_metadata(filename).get('exif_date', None)
    except Exception as ex:
        logging.warning("get_metadata threw an exception when processing file '%s': %s" % (filename, ex))
        st = os.stat(filename)
        return datetime.fromtimestamp(st.st_ctime > st.st_mtime and st.st_ctime or st.st_mtime)


def generate_filename_from_date(filename, file_date=None):
    """
    Generates a filename based on the original filename and the timestamp provided.

    :param filename:
    :param file_date: If not provided it will be fetched from the file.
    """
    if not file_date:
        file_date = get_date_from_file(filename)

    filename = os.path.basename(filename)
    timestamp = file_date.strftime(timestamp_format)
    if timestamp in filename:
        filename = filename.replace(timestamp, '')

    basename, ext = os.path.splitext(filename)
    return new_filename_format % dict(filename=basename, timestamp=timestamp, file_extension=ext)


def generate_folders_from_date(file_date, tag=None):
    """
    Generates a date-based folder structure as a string using a datetime.

    :param file_date:
    :param tag: if not None it will replace the day-part of the result.
    :returns: string
    """
    if not tag:
        tag = str(file_date.day)
    return os.sep.join([str(file_date.year), months[file_date.month], tag])


def dirwalk(dir, extensions_to_include=None):
    """
    Traverse a directory yielding any file matching extensions_to_include or all if extensions_to_include is None.
    NB! The list of extensions must be in the form of ['jpg', 'png'] and not ['.jpg', '.png']!

    :param dir: the directory to traverse/scan.
    :param extensions_to_include: list if file-extensions to include. If not provided or None all files will be included.
    """
    extensions_check = extensions_to_include is not None
    for f in os.listdir(dir):
        full_path = os.path.join(dir, f)
        if os.path.isdir(full_path) and not os.path.islink(full_path):
            for x in dirwalk(full_path, extensions_to_include):
                ext = os.path.splitext(x)[-1][1:].lower()
                if not extensions_check or ext in extensions_to_include:
                    yield x
        else:
            ext = os.path.splitext(full_path)[-1][1:].lower()
            if not extensions_check or ext in extensions_to_include:
                yield full_path


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

    :param folder: the folder to scan for photos.
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
    Relocates all photos from the source folder into a date-based hierarchy in the target folder.

    :param source_dir: folder to process.
    :param target_dir: folder to build date-based structure and move photos into.
    :param append_timestamp: boolean value indicating if we add a timestamp to every processed filename.
    :param remove_source: boolean value indicating if we remove photos from the source folder when processed.
    :param tag: string value to use instead of the day-part in the folder structure.
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
            relocate_photo(complete_filename, target_dir=target_dir, append_timestamp=append_timestamp,
                           remove_source=remove_source, tag=current_tag)

    if remove_source:
        remove_source_folders(photos.keys())


def generate_valid_target(filename):
    """
    Generates a new filename if there is already an existing file with the same name.

    :param filename: the target file we want to create
    :returns: string
    """
    counter = 1
    while True:
        if not os.path.exists(filename):
            break
        base_name, ext = os.path.splitext(filename)
        filename = duplicate_filename_format % dict(filename=base_name, counter=counter, file_extension=ext)
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
    Removes any empty folders.

    :param folders: folders to process.
    """
    for folder in folders:
        if len(list(dirwalk(folder))) == 0:
            os.removedirs(folder)


def find_duplicates(source_folder, target_folder, delete_duplicates=False, verbose=False):
    """
    Finds filenames present in both the source folder and the target folder and optionally removes them.

    :param source_folder: the source folder.
    :param target_folder: the master folder.
    :param delete_duplicates: boolean value to indicate if we want to remove any duplicates found from the source folder.
    :param verbose: boolean value indicating verbose logging.
    """
    source_files = {}
    target_files = {}
    if verbose:
        logging.debug("Scanning source folder ..."),

    for filename in dirwalk(source_folder):
        st = os.stat(filename)
        source_files.setdefault(st.st_size, []).append((filename, st))

    if verbose:
        logging.debug("done!")

    if verbose:
        logging.debug("Scanning target folder ..."),

    for filename in dirwalk(target_folder):
        st = os.stat(filename)
        target_files.setdefault(st.st_size, []).append((filename, st))

    if verbose:
        logging.debug("done!")

    if verbose:
        logging.debug("Locating duplicates:")

    for file_size, file_data in target_files.items():
        existing_files = source_files.get(file_size, [])
        for existing_filename, existing_st in existing_files:
            for filename, st in file_data:
                existing_creation_time = st.st_mtime < st.st_ctime and st.st_mtime or st.st_ctime
                st_creation_time = existing_st.st_mtime < existing_st.st_ctime and existing_st.st_mtime or existing_st.st_ctime
                if existing_creation_time == st_creation_time:
                    if delete_duplicates:
                        os.remove(filename)

                    if verbose:
                        logging.debug("%s appears to be a duplicate of %s." % (filename, existing_filename))

                    yield filename


    # base_filename, ext = os.path.splitext(filename)
    # if ext:
    #     if ext[1:].lower() in photo_extensions_to_include:
    #         exif = get_exif(filename)
    #         return str(
    #             time.strptime(exif.get('DateTime', exif.get('DateTimeOriginal', exif.get('DateTimeDigitized'))),
    #                           "%Y:%m:%d %H:%M:%S"))
    #

def get_checksum(filename):
    """
    Generates a hexdigest version of the SHA512 checksum generated from the provided filename.

    :param filename:
    :returns: a string.
    """
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
    Builds a cache using filesize as key and a list of matching filenames as value.

    :param path: the folder containing files to process.
    :returns: a dictionary of filesize mapped against matching filenames in path.
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
    Locates files in the source folder not present in the target folder. Uses filesize to determine if something is
    duplicate or not.

    :param source_folder: the folder containing files you want to check are present in the target folder.
    :param target_folder: the folder containing existing files.
    :param verbose: boolean value indicating if the process logs debug info or not.
    """
    if verbose:
        logging.debug("Scanning source folder ..."),

    source_files = build_file_cache(source_folder)

    if verbose:
        logging.debug("done!")

    if verbose:
        logging.debug("Scanning target folder ..."),

    target_files = build_file_cache(target_folder)

    if verbose:
        logging.debug("done!")

    sha_cache = {}
    if verbose:
        logging.debug("Locating new content:")

    for file_size, filenames in target_files.items():
        if not file_size in source_files.keys():
            for filename in filenames:
                if verbose:
                    logging.debug(filename)

                yield filename
        else:
            for existing_filename in source_files[file_size]:
                for filename in filenames:

                    if existing_filename[:8] == filename[:8]:
                        continue

                    if not existing_filename in sha_cache:
                        sha_cache[existing_filename] = get_checksum(existing_filename)

                    if not filename in sha_cache:
                        sha_cache[filename] = get_checksum(filename)

                    if sha_cache[existing_filename] != sha_cache[filename]:
                        if verbose:
                            logging.debug(filename)

                        yield filename


def print_tag(source_folder):
    """

    :param source_folder:
    """
    for filename in dirwalk(source_folder):
        print(filename, get_tag_from_filename(filename, source_folder))


def clean_up(source_folder):
    """

    :param source_folder:
    """
    logging.debug("Cleaning up %s" % source_folder)
    for filename in dirwalk(source_folder):
        if os.path.basename(filename) in ignore_files:
            os.remove(filename)

    paths = {}
    for path in [os.path.join(source_folder, path) for path in os.listdir(source_folder)]:

        if os.path.isdir(path):
            paths[os.path.join(source_folder, path)] = []

    for filename in dirwalk(source_folder):
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
    Relocates movies into a date-based hierarchy based on the creation date of the files.

    :param source_dir: the source folder containing movies to process.
    :param target_dir: the target folder to hold the date-based folder structure.
    :param append_timestamp: boolean value indicating if we add a timestamp to the filenames.
    :param remove_source: boolean value indicating if we remove the source files from the source dir on success.
    :param tag: single string to use instead of the day-part in the date-based folder structure.
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
    Will create (or move into if remove_source is set to True) a photo a date-hierarchy based on the EXIF-date found in
    the photo metadata.

    :param filename: the original file to process.
    :param target_dir: the target folder to hold the generated data-hierarchy.
    :param append_timestamp: a boolean value indicating if the generated filename should include a timestamp.
    :param remove_source: boolean value indicating if the original source should be removed after processing.
    :param tag: single word text string to use instead of the day-part of the folder structure, to group photos by tag.
    :param skip_existing: boolean value indicating if the processing should exit if target file is already present.
    :param path_prefix: string to prepend the generated date-based hierarchy folder structure.
    """
    st = os.stat(filename)
    dt = st.st_ctime < st.st_mtime and datetime.fromtimestamp(st.st_ctime) or datetime.fromtimestamp(st.st_mtime)

    if path_prefix:
        target_dir = os.path.join(target_dir, path_prefix, generate_folders_from_date(dt, tag))
    else:
        target_dir = os.path.join(target_dir, generate_folders_from_date(dt, tag))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    new_filename = os.path.join(target_dir,
                                append_timestamp and generate_filename_from_date(filename, dt) or os.path.basename(
                                    filename))
    new_filename = generate_valid_target(new_filename)

    if skip_existing and os.path.exists(new_filename):
        return

    if remove_source:
        shutil.move(filename, new_filename)
    else:
        shutil.copy(filename, new_filename)

    return new_filename


def generate_thumb(media_folder, absolute_filename, width, height, do_crop, alternative_thumbnail_name=None,
                   raise_exception_on_error=False):
    """

    :param media_folder: target folder to hold the generated thumbnails.
    :param absolute_filename: the original photo to use as base for the thumbnail.
    :param width: max width of the generated thumbnail.
    :param height: max height of the generated thumbnail.
    :param do_crop: boolean value indicating if the image should be cropped using width and height arguments as bounds.
    :param alternative_thumbnail_name: alternative name for the generated thumbnail.
    :param raise_exception_on_error: boolean value indicating if we raise exception on any error or return quietly.
    """
    logging.debug("Generating thumb: %s" % absolute_filename)

    filename, ext = os.path.splitext(os.path.basename(absolute_filename))
    if alternative_thumbnail_name:
        filename = alternative_thumbnail_name

    if not os.path.exists(absolute_filename):
        logging.warning("inputfile %s does not exists" % absolute_filename)

        if raise_exception_on_error:
            raise Exception('Inputfile "%s" does not exists.' % absolute_filename)

        return

    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    output = os.path.join(media_folder, '%s_%sx%s%s%s' % (filename, width, height, do_crop and '_crop' or '', ext))
    if not os.path.exists(output):
        try:
            resize_image(absolute_filename, output, width, height, crop=do_crop)
        except (Exception) as ex:
            logging.warning(ex)

    return output


def resize_image(source_file, target_file, width, height, crop=False):
    """
    Resizes an image specified by source_file and writes output to target_file.
    Will read EXIF data from source_file, look for information about orientation
    and rotate photo if such info is found.

    :param source_file: the original photo or image.
    :param target_file: the target output file for the resized and processed photo.
    :param width: max width for the processed photo.
    :param height: max height for the processed photo.
    :param crop: boolean value indicating if the photo should be cropped using width and height as boundries.
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
        image = image.crop((x_offset, y_offset, x_offset + int(crop_width), y_offset + int(crop_height)))
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
