import hashlib
import logging
import os
from mediaphile.cli import default_new_filename_format, default_timestamp_format, default_duplicate_filename_format
from mediaphile.lib import months
import logging
performance_log = logging.getLogger("performance_log")
log = logging.getLogger("verboselogger")


def generate_valid_target(filename, duplicate_filename_format=default_duplicate_filename_format):
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


def get_tag_from_filename(filename, source_dir):
    """

    :param filename:
    :param source_dir:
    """
    result = os.path.split(filename)[0][len(source_dir):]

    if result and result[0] == os.sep:
        result = result[1:]

    return result


def generate_folders_from_date(file_date, tag=None, prefix=None):
    """
    Generates a date-based folder structure as a string using a datetime.

    :param prefix:
    :param file_date:
    :param tag: if not None it will replace the day-part of the result.
    :returns: string
    """
    params = [str(file_date.year), months[file_date.month], tag or str(file_date.day)]
    if prefix:
        params.insert(0, prefix)

    return os.sep.join(params)


def generate_filename_from_date(filename, file_date, timestamp_format=default_timestamp_format,
                                new_filename_format=default_new_filename_format):
    """
    Generates a filename based on the original filename and the timestamp provided.

    :param timestamp_format:
    :param new_filename_format:
    :param filename:
    :param file_date: If not provided it will be fetched from the file.

    Example of use::

        0 -- ok
        1 -- bad
    """
    filename = os.path.basename(filename)
    timestamp = file_date.strftime(timestamp_format)
    if timestamp in filename:
        filename = filename.replace(timestamp, '')

    basename, ext = os.path.splitext(filename)
    return new_filename_format % dict(filename=basename, timestamp=timestamp, file_extension=ext)


def dirwalk(folder, extensions_to_include=None):
    """
    Traverse a directory yielding any file matching extensions_to_include or all if extensions_to_include is None.
    NB! The list of extensions must be in the form of ['jpg', 'png'] and not ['.jpg', '.png']!

    :param folder: the directory to traverse/scan.
    :param extensions_to_include: list if file-extensions to include. If not provided or None all files will be included.
    """
    extensions_check = extensions_to_include is not None
    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
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


def remove_source_folders(folders):
    """
    Removes any empty folders.

    :param folders: folders to process.
    """
    for folder in folders:
        if len(list(dirwalk(folder))) == 0:
            os.removedirs(folder)


def find_duplicates(source_folder, target_folder, delete_duplicates=False,
                    rename_duplicates=False, dry_run=False, verbose=False, use_timestamp_for_diff=False):
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
        performance_log.debug("Scanning source folder ..."),

    for filename in dirwalk(source_folder):
        st = os.stat(filename)
        source_files.setdefault(st.st_size, []).append((filename, st))

    if verbose:
        performance_log.debug("done!")

    if verbose:
        performance_log.debug("Scanning target folder ..."),

    for filename in dirwalk(target_folder):
        st = os.stat(filename)
        target_files.setdefault(st.st_size, []).append((filename, st))

    if verbose:
        performance_log.debug("done!")

    for file_size, file_data in target_files.items():
        existing_files = source_files.get(file_size, [])
        for existing_filename, existing_st in existing_files:
            for filename, st in file_data:
                duplicate_found = False
                if use_timestamp_for_diff:
                    existing_creation_time = st.st_mtime < st.st_ctime and st.st_mtime or st.st_ctime
                    st_creation_time = existing_st.st_mtime < existing_st.st_ctime and existing_st.st_mtime or existing_st.st_ctime
                    if existing_creation_time == st_creation_time:
                        duplicate_found = True
                else:
                    duplicate_found = get_checksum(filename) == get_checksum(existing_filename)

                if duplicate_found:
                    if delete_duplicates and not dry_run:
                        os.remove(filename)

                    if verbose:
                        log.debug("%s = %s." % (filename, existing_filename))

                    yield filename


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


def build_file_cache(path, ignore_files=None):
    """
    Builds a cache using filesize as key and a list of matching filenames as value.

    :param path: the folder containing files to process.
    :returns: a dictionary of filesize mapped against matching filenames in path.
    """
    result = {}
    for filename in dirwalk(path):
        p, f = os.path.split(filename)
        if ignore_files and f.lower() in ignore_files:
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


def clean_up(source_folder, ignore_files=None):
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
