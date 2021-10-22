import os
import secrets
from flask import current_app, request
from PIL import Image, ImageFile


def save_image(source_image, path, output_size=(125, 125)):
    """Compress and save user-uploaded images to the filesystem.

    Parameters
    ----------
    source_image : [WTForm.image]
        User-uploaded image.
        Must have .filename method if duck-typing.
    path: [string]
        Base dir to save image.
    output_size : tuple, optional
        Desired output size, default is (125, 125).

    Returns
    -------
    [image_fn]
        File name of resized image as it is saved on filesystem.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(source_image.filename)

    if not f_ext:
        # This is in case a PIL image or
        # some buffer data was passed.
        f_ext = ".jpg"

    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path,
                              'static/' + path,
                              image_fn)

    i = compress_image(source_image, output_size)
    i.save(image_path)

    return image_fn


def compress_image(image, output_size=(125, 125)):
    """Compress input image.

    Parameters
    ----------
    image : [image]
        Any valid image.
    output_size : tuple, optional
        Desired output size, default is (125, 125).

    Returns
    -------
    [i]
        Compressed image.
    """
    if isinstance(image, ImageFile.ImageFile):
        i = image
    else:
        i = Image.open(image)

    i.thumbnail(output_size)
    return i


def save_pdf(form_pdf):
    """Save user-uploaded pdf transcript file under /static/transcripts.
    Parameters
    ----------
    form_transcript : [file]
    Returns
    -------
    [str]
        A random hex is generated as the new file name to prevent
        any errors that would arise on the filesystem when filename uniqueness
        is violated.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pdf.filename)
    pdf_fn = random_hex + f_ext
    pdf_path = os.path.join(current_app.root_path,
                            'static/transcripts', pdf_fn)
    form_pdf.save(pdf_path)

    return pdf_path
