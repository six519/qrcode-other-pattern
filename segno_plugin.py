import io

from PIL import (
    Image,
    ImageColor,
)


def write_other_pattern(qrcode, scale=1, border=None, dark='#000', light='#fff',
              finder_dark=False, finder_light=False, data_dark=False,
              data_light=False, version_dark=False, version_light=False,
              format_dark=False, format_light=False, alignment_dark=False,
              alignment_light=False, timing_dark=False, timing_light=False,
              separator=False, dark_module=False, quiet_zone=False, file_pattern=None):

    # Converting to PIL from qrcode-artistics plugin
    # Thanks to Lars Heuer
    # https://github.com/heuer/qrcode-artistic

    buff = io.BytesIO()
    qrcode.save(buff, kind='png', scale=scale, border=border, dark=dark,
                light=light, finder_dark=finder_dark, finder_light=finder_light,
                data_dark=data_dark, data_light=data_light,
                version_dark=version_dark, version_light=version_light,
                format_dark=format_dark, format_light=format_light,
                alignment_dark=alignment_dark, alignment_light=alignment_light,
                timing_dark=timing_dark, timing_light=timing_light,
                separator=separator, dark_module=dark_module, quiet_zone=quiet_zone)
    buff.seek(0)
    pil_image = Image.open(buff).convert('RGBA')

    if not file_pattern:
        raise ValueError('file_pattern is required')
    
    pattern = Image.open(file_pattern).convert('RGBA')

    if dark != '#000':
        # replace color
        img_data = pattern.getdata()
        new_data = []
        for item in img_data:
            if item[0] in list(range(0, 256)) and item[1] in list(range(0, 256)) and item[2] in list(range(0, 256)) and item[3] > 0:
                new_data.append(ImageColor.getrgb(dark))
            else:
                new_data.append(item)
        pattern.putdata(new_data)

    patterned_qr = Image.new('RGBA', pil_image.size, light)

    for y in range(0, pil_image.size[1], scale):
        for x in range(0, pil_image.size[0], scale):
            if pil_image.getpixel((x, y))[0:3] == ImageColor.getrgb(dark):
                resized_pattern = pattern.resize((scale, scale), Image.Resampling.NEAREST)
                patterned_qr.paste(resized_pattern, (x, y), resized_pattern)

    return patterned_qr