import os
import unittest
import warnings
import io

from PIL import Image
import segno

_ZBAR = False
try:
    from pyzbar.pyzbar import decode as zbardecode
    _ZBAR = True
except ImportError:
    pass


class TestOtherPattern(unittest.TestCase):

    def decodeImage(self, img, content):

        if not _ZBAR:
            warnings.warn('pyzbar not available')
            return True
        
        decoded_text = zbardecode(img)
        self.assertEqual(1, len(decoded_text))        
        self.assertEqual('QRCODE', decoded_text[0].type)
        return content == decoded_text[0].data.decode('utf-8')

    def test_to_other_pattern(self):
        content = 'https://ferdinandsilva.com'
        scale = 10
        border = 2
        qr_code = segno.make(content)
        width, height = qr_code.symbol_size(scale=scale, border=border)
        out = io.BytesIO()
        new_pattern = qr_code.to_other_pattern(
            scale=scale, 
            border=border, 
            file_pattern=os.path.join(
                os.path.abspath(os.path.dirname(__file__)), 
                '../pattern.png',
            ),
        )
        new_pattern.save(out, format='PNG')
        out.seek(0)
        img = Image.open(out)
        self.assertEqual(True, self.decodeImage(img, content))
        self.assertEqual((width, height), img.size)

if __name__ == '__main__':
    unittest.main()