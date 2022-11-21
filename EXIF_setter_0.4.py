"""
/***************************************************************************
  EXIF_setter_x.x.py

  Python 3.x script that set location and datetime_original data to photos taken by AidaLight application.
  This script requires exif module.
  Photo files with .jpg or .jpeg extension.
  One have to make "JPEG_AND_CSV_INPUT" and "JPEG_OUTPUT" folders in the same location as this script. 
  To the "JPEG_AND_CSV_INPUT" folder one should copy the .jpeg files and .csv file (from Aida_data_parser script). 
  
  --------------------------------------
  Date : 17.11.2022
  Copyright: (C) 2022 by Piotr Michałowski
  Email: piotrm35@hotmail.com
/***************************************************************************
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as published
 * by the Free Software Foundation.
 *
 ***************************************************************************/
"""


#========================================================================================================


import os
import exif      # pip install exif


def get_coordinate_tuple(coordinate):
    coordinate = float(coordinate)
    degrees = int(coordinate)
    tmp = (coordinate - degrees) * 60
    minutes = int(tmp)
    seconds = (tmp - minutes) * 60
    return (degrees, minutes, seconds)


def print_all_image_data(my_image):
    print('------------------------------------------------------------------')
    print()
    if my_image.has_exif:
        for tag in my_image.list_all():
            print("my_image.get('" + str(tag) + "')= " + str(my_image.get(tag)))
    else:
        print('my_image.has_exif = False')
    print()


#========================================================================================================
# setup:


INPUT_JPEG_AND_CSV_FOLDER_PATH = os.path.join('.', 'JPEG_AND_CSV_INPUT')
OUTPUT_JPEG_FOLDER_PATH = os.path.join('.', 'JPEG_OUTPUT')


#========================================================================================================
# work:


def work():
    if not os.path.exists(OUTPUT_JPEG_FOLDER_PATH):
        os.mkdir(OUTPUT_JPEG_FOLDER_PATH)
        print('os.mkdir(' + str(OUTPUT_JPEG_FOLDER_PATH) + ')')
    if len(os.listdir(OUTPUT_JPEG_FOLDER_PATH)) > 0:
        print(OUTPUT_JPEG_FOLDER_PATH + " isn't empty")
        return
    csv_file_names = [f for f in os.listdir(INPUT_JPEG_AND_CSV_FOLDER_PATH) if os.path.isfile(os.path.join(INPUT_JPEG_AND_CSV_FOLDER_PATH, f)) and os.path.splitext(f)[1].upper() == '.CSV']
    if len(csv_file_names) != 1:
        print('len(csv_file_names) != 1')
        return
    csv_file = open(os.path.join(INPUT_JPEG_AND_CSV_FOLDER_PATH, csv_file_names[0]), 'r')
    lines = csv_file.readlines()
    csv_file.close()
    first_line = True
    csv_dict = {}
    for line in lines:
        if not first_line:
            line_list = line.split(',')
            if len(line_list) == 4:
                csv_dict[line_list[3].replace('\n', '')] = {'lat': line_list[0], 'lon': line_list[1], 'time_stamp': line_list[2]}
            else:
                print('len(line_list) != 4 -> line: ' + str(line))
        first_line = False
    img_file_names = [f for f in os.listdir(INPUT_JPEG_AND_CSV_FOLDER_PATH) if os.path.isfile(os.path.join(INPUT_JPEG_AND_CSV_FOLDER_PATH, f)) and (os.path.splitext(f)[1].upper() == '.JPG' or os.path.splitext(f)[1].upper() == '.JPEG')]
    if len(img_file_names) == 0:
        print('len(img_file_names) == 0')
        return
    for img_file_name in img_file_names:
        if img_file_name in csv_dict.keys():
            print('img_file_name: ' + str(img_file_name))
            with open(os.path.join(INPUT_JPEG_AND_CSV_FOLDER_PATH, img_file_name), 'rb') as image_file:
                my_image = exif.Image(image_file)
##                print_all_image_data(my_image)
                my_image.datetime_original = csv_dict[img_file_name]['time_stamp']
                my_image.gps_latitude = get_coordinate_tuple(csv_dict[img_file_name]['lat'])
                my_image.gps_latitude_ref = 'N'
                my_image.gps_longitude = get_coordinate_tuple(csv_dict[img_file_name]['lon'])
                my_image.gps_longitude_ref = 'E'
                my_image.make = 'AidaLight'
##                print_all_image_data(my_image)
            with open(os.path.join(OUTPUT_JPEG_FOLDER_PATH, img_file_name), 'wb') as new_image_file:
                new_image_file.write(my_image.get_file())
        else:
            print('img_file_name NOT in csv_dict.keys() -> img_file_name: ' + str(img_file_name))


print()
print('SCRIPT BEGIN')
work()
print('SCRIPT END')
print()


#========================================================================================================
