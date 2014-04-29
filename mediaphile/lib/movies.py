import os
import shutil
import datetime
from mediaphile.lib.file_operations import remove_source_folders, get_files_in_folder, \
    generate_valid_target, generate_folders_from_date, generate_filename_from_date, \
    get_tag_from_filename


def relocate_movies(source_dir, target_dir=None, append_timestamp=True, remove_source=True, tag=None,
                    movie_extensions_to_include=None):
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

