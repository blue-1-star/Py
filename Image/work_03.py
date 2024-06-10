# Import PIL (Note: the package name is Pillow, yet we import from PIL).
# Yes, the import here is confusing. More context here: https://pypi.org/project/Pillow/
from PIL import Image

# Import pytesseract (a Python wrapper for Tesseract)
# Note: You will need to have Tesseract installed on your machine for pytesseract to work.
import pytesseract

# Extract text from the image
im_path ="G:/Programming/Py/Image/data/"
# filename = "id_cod_e.bmp"
# filename = "test.jpg"
filename = "p0002.png"
image_path = im_path + filename 
image = Image.open(image_path)
# image.show()
extracted_text = pytesseract.image_to_string(image, lang='ukr+eng')
# Write the extracted text to a file
# filename.replace()
txt_path = im_path + filename[:-3]+'txt' 
with open(txt_path, 'w') as f:
    f.write(extracted_text)
print(extracted_text)


