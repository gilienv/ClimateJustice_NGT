from PIL import Image
from datetime import datetime

current_datetime = datetime.now()
current_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M_%S")
img_download_path = f'CaptchaImg/{current_datetime}.png'


image_path = 'CaptchaImg/screenshot.png'
# cropped_image = image.crop((left, top, right, bottom))
crop_box = (1600, 680, 2000, 750)
image = Image.open(image_path)
cropped_image = image.crop(crop_box)

# Save the cropped image to a file
cropped_image.save(img_download_path)
