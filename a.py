from PIL import Image
import pytesseract
img_name = './image.png'
img = Image.open(img_name)
text = pytesseract.image_to_string(img, lang='eng')
print(text)






