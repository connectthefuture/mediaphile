#coding=utf-8

import os
import logging
import shutil
import datetime

from PIL import Image
from PIL.ExifTags import TAGS

from mediaphile.cli import default_timestamp_format, default_duplicate_filename_format, default_new_filename_format, \
    default_use_checksum_existence_check
from mediaphile.lib.file_operations import dirwalk, get_files_in_folder, remove_source_folders, \
    generate_folders_from_date, generate_filename_from_date, get_tag_from_filename, generate_valid_target
from mediaphile.lib.metadata import get_metadata


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
        logging.warning("'get_metadata' threw an exception when processing file '%s': %s" % (filename, ex))
        st = os.stat(filename)
        return datetime.fromtimestamp(st.st_ctime > st.st_mtime and st.st_ctime or st.st_mtime)


def get_photos_in_folder(folder, photo_extensions_to_include=None):
    """

    :param folder: the folder to scan for photos.
    """
    return get_files_in_folder(folder, extensions_to_include=photo_extensions_to_include)


def relocate_photos(source_dir, target_dir=None, append_timestamp=True, remove_source=True, tag=None, dry_run=False,
                    photo_extensions_to_include=None, timestamp_format=default_timestamp_format,
                    duplicate_filename_format=default_duplicate_filename_format,
                    new_filename_format=default_new_filename_format, path_prefix=None, skip_existing=False):
    """
    Relocates all photos from the source folder into a date-based hierarchy in the target folder.

    :param skip_existing:
    :param path_prefix:
    :param dry_run:
    :param photo_extensions_to_include:
    :param timestamp_format:
    :param duplicate_filename_format:
    :param new_filename_format:
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

            relocate_photo(
                complete_filename,
                target_dir=target_dir,
                append_timestamp=append_timestamp,
                remove_source=remove_source,
                tag=current_tag,
                skip_existing=skip_existing,
                path_prefix=path_prefix,
                dry_run=False,
                timestamp_format=timestamp_format,
                duplicate_filename_format=duplicate_filename_format,
                new_filename_format=new_filename_format)

    if not dry_run and remove_source:
        remove_source_folders(photos.keys())


def relocate_photo(filename, target_dir, file_date=None, append_timestamp=True, remove_source=True, tag=None,
                   skip_existing=False, path_prefix=None, dry_run=False, timestamp_format=default_timestamp_format,
                   duplicate_filename_format=default_duplicate_filename_format,
                   new_filename_format=default_new_filename_format,
                   use_checksum_existence_check=default_use_checksum_existence_check):
    """

    :param use_checksum_existence_check:
    :param timestamp_format:
    :param duplicate_filename_format:
    :param new_filename_format:
    :param dry_run:
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

    target_dir = os.path.join(target_dir, generate_folders_from_date(file_date, tag, path_prefix))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    new_filename = os.path.join(target_dir, append_timestamp and generate_filename_from_date(
        filename,
        file_date,
        timestamp_format=timestamp_format,
        new_filename_format=new_filename_format) or os.path.basename(filename))

    if skip_existing and os.path.exists(new_filename):
        if use_checksum_existence_check:
            pass  # check checksums
        else:
            return

    new_filename = generate_valid_target(new_filename, duplicate_filename_format)
    logging.debug("%s -> %s" % (filename, new_filename))

    if remove_source:
        if not dry_run:
            shutil.move(filename, new_filename)
        else:
            logging.debug('move')
    else:
        if not dry_run:
            shutil.copy(filename, new_filename)
        else:
            logging.debug('copy')

    return new_filename


def print_tag(source_folder):
    """

    :param source_folder:
    """
    for filename in dirwalk(source_folder):
        print(filename, get_tag_from_filename(filename, source_folder))


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
