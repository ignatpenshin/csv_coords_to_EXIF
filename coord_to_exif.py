import pandas as pd
import os
from exif import Image
import glob
import logging

logging.basicConfig(format = '%(message)s', level=logging.INFO, filename= "log.txt", filemode = "w")

def decdeg2dms(dd):
    mnt,sec = divmod(dd*3600,60)
    deg,mnt = divmod(mnt,60)
    return deg,mnt,sec

csv = pd.read_csv('coords.csv', sep=';', header=0)
d = pd.DataFrame(csv)

images = glob.glob('*.jpg')
count = 0
for img in images:
    with open(img, 'rb') as image_file:
        my_img = Image(image_file)
        try:
            my_img.set("gps_latitude", decdeg2dms(d.loc[d['photo'] == img]['lat'].item()))
            my_img.set("gps_longitude", decdeg2dms(d.loc[d['photo'] == img]['lon'].item()))
            my_img.set("gps_latitude_ref", "N")
            my_img.set("gps_longitude_ref", "E")
            print(my_img.get("gps_latitude"), my_img.get("gps_latitude_ref"), my_img.get("gps_longitude"), my_img.get("gps_longitude_ref"))
            with open(img, 'wb') as new_img_file:
                new_img_file.write(my_img.get_file())
                count += 1
        except ValueError:
            logging.info(img + " - coords not found")
logging.info(str(count) + '/' + str(len(images)) + ' updated')

        