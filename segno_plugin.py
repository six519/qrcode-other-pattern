# -----------------------------------------------------------------------------
# Filename: segno_plugin.py
# Description: Segno Plugin
# Author: Ferdinand Silva <ferdinandsilva@ferdinandsilva.com>
# Created: July 26, 2024
# -----------------------------------------------------------------------------
import io

from PIL import (
    Image,
    ImageColor,
)


def write_other_pattern(
        qrcode, scale=1, border=None, dark='#000', light='#fff',
        finder_dark=False, finder_light=False, data_dark=False,
        data_light=False, version_dark=False, version_light=False,
        format_dark=False, format_light=False, alignment_dark=False,
        alignment_light=False, timing_dark=False, timing_light=False,
        separator=False, dark_module=False, quiet_zone=False, 
        file_pattern=None,
    ):

    # Converting to PIL from qrcode-artistics plugin
    # Thanks to Lars Heuer
    # https://github.com/heuer/qrcode-artistic

    buff = io.BytesIO()
    qrcode.save(
        buff, kind='png', scale=scale, border=border, dark=dark,
        light=light, finder_dark=finder_dark, finder_light=finder_light,
        data_dark=data_dark, data_light=data_light,
        version_dark=version_dark, version_light=version_light,
        format_dark=format_dark, format_light=format_light,
        alignment_dark=alignment_dark, alignment_light=alignment_light,
        timing_dark=timing_dark, timing_light=timing_light,
        separator=separator, dark_module=dark_module, quiet_zone=quiet_zone,
    )
    buff.seek(0)
    pil_image = Image.open(buff).convert('RGBA')

    if not file_pattern:
        raise ValueError('file_pattern is required')
    
    # Create a blank image that will be used upon the function's return
    patterned_qr = Image.new('RGBA', pil_image.size, light)

    # A custom shape that will be pasted onto a previously created blank image
    pattern = Image.open(file_pattern).convert('RGBA')

    if dark != '#000':
        # Replace the custom shape's color
        img_data = pattern.getdata()
        new_data = []
        rgb_range = list(range(0, 256))
        for item in img_data:
            if (
                item[0] in rgb_range 
                and item[1] in rgb_range 
                and item[2] in rgb_range 
                and item[3] > 0
            ):
                # Replace the color with dark value
                new_data.append(ImageColor.getrgb(dark))
                continue
            
            # Retain if transparent
            new_data.append(item)
        pattern.putdata(new_data)

    # Resize the custom image
    resized_pattern = pattern.resize(
        (scale, scale), 
        Image.Resampling.NEAREST,
    )

    # Read converted PIL image from segno
    for y in range(0, pil_image.size[1], scale):
        for x in range(0, pil_image.size[0], scale):
            if pil_image.getpixel((x, y))[0:3] == ImageColor.getrgb(dark):
                # Paste the resized pattern if a black module is detected
                patterned_qr.paste(resized_pattern, (x, y), resized_pattern)

    return patterned_qr