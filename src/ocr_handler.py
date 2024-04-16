import easyocr
import numpy as np
from PIL import Image
import pillow_heif
import io


class OpticalCharacterRecogniser:
    def __init__(self, image_path, language="en"):
        self.language = language
        self.reader = easyocr.Reader([self.language], gpu=True)
        img = self.load_image(image_path)
        self.image = self.image_to_nparray(img)

    def extract_text(self):
        results = self.reader.readtext(self.image)
        extracted_text = ""
        for result in results:
            text = result[1]
            extracted_text += text + " "
        return extracted_text.strip()

    def load_image(self, image_path):
        if image_path.lower().endswith((".heic", ".heif")):
            heif_file = pillow_heif.read_heif(image_path)
            image = heif_file.to_pillow()
        else:
            image = Image.open(image_path)
        return image

    def image_to_nparray(self, image):
        if image.format != "TIFF":
            byte_io = io.BytesIO()
            image.save(byte_io, format="TIFF")
            byte_io.seek(0)
            image = Image.open(byte_io)

        image_np_array = np.array(image)
        return image_np_array
