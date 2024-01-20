import sys
from pprint import pprint
import ffmpeg
import pikepdf
from PIL import Image
from PIL.ExifTags import TAGS
from tinytag import TinyTag


def get_media_metadata(media_file):
    ffmpeg_data = ffmpeg.probe(media_file)["streams"]
    tt_data = TinyTag.get(media_file).as_dict()
    return tt_data, ffmpeg_data


def get_pdf_metadata(pdf_file):
    pdf = pikepdf.Pdf.open(pdf_file)
    return dict(pdf.docinfo)


def get_image_metadata(image_file):
    image = Image.open(image_file)
    info_dict = {
            "Filename": image.filename,
            "Image Size": image.size,
            "Image Height": image.height,
            "Image Width": image.width,
            "Image Format": image.format,
            "Image Mode": image.mode,
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1)
            }
    exifdata = image.getexif()
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        info_dict[tag] = data
    return info_dict


if __name__ == "__main__":
    file = sys.argv[1]
    if file.endswith(".pdf"):
        pprint(get_pdf_metadata(file))
    elif file.endswith(".jpg"):
        pprint(get_image_metadata(file))
    else:
        pprint(get_media_metadata(file))
