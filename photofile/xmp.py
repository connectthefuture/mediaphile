from bs4 import BeautifulSoup

key_mapping = {
    'caption': 'bopt:description',
}


def get_xmp_value(xmp_file, key, xmp_data=None):
    """
    Return value of key if found in xmp_file.

    :param xmp_file: xml file with XMP-compatible data.
    :param key: a valid mapping found in the xmp.key_mapping dictionary.
    """
    if not key in key_mapping:
        raise KeyError("Key '%s' not found in XMP-key mapping." % key)

    if not xmp_data:
        xmp_data = open(xmp_file).read()

    soup = BeautifulSoup(xmp_data)
    result = soup.find_all(key_mapping[key])
    if not result:
        return None

    return result[0]