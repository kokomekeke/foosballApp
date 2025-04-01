from pprint import pprint
from PIL import Image
import piexif

from server.utils import dms_to_dec

codec = 'ISO-8859-1'


def img_exif(exif_dict):
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict


def img_geoloc(exif_dict):
    exif_dict = img_exif(exif_dict)
    print(exif_dict['GPS'])
    return dms_to_dec(exif_dict['GPS']['GPSLatitude']), dms_to_dec(exif_dict['GPS']['GPSLongitude'])

