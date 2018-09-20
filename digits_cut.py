from preprocess.py import *
from get_bounding_box.py import *

import cv2
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class digits_cut :

    def cut_and_affect_to_folder(preprocessed_img, dist, labels, digits_path, ind, last_digit = 2):
        """
        Creates bounding boxes and put each box in the folder corresponding to its label
    preprocessed_img : preprocessed image is after exctarcted dark screen + contrasts

        :param dist: the dist between each cuts, ie the width of each bounding boxes (same widths), output of the 'get_bd_dummy' function
        :param labels: list of int of size 4, 10 labels : from '0' to '9' and 'X' if nothing of the digits BEFORE the COMMA
        :param digits_path: string, the output path to save the bounding boxes in.
                Of the form "Datasets_digits/" and contains the '0', '1', ... 'X' folders
                The image reduced to its bounding box is saved into the folder corresdponding to its label

        :param ind: the ID of the image 'o8sdf7ksqjdh.jpg'
        :param last_digit: int, optional.
                  If 2, we only save the 3 last digits before the comma (without the unity digit)
                  If 3, we save all digits before the comma
        :return:
        """

        for i in range(last_digit):
            inf = i*dist
            sup = (i+1)*dist
            box = preprocessed_img[:, int(inf):int(sup)]
            #label = int(labels_df[labels_df['image'] == ind]['cadran_'+ str(i+1)])
            label = labels[i]
            mpimg.imsave(digits_path +  str(label) + "/" + ind, box)
        return()


    # ------------------------- csv_labels_to_df ----------------------
    #
    # From csv file in 'labels_path', converts into a panda dataframe
    # must contain the 'cadran_1', 'cadran_2',
    # 'cadran_3', 'cadran_4' columns (from first digit to last digit before the comma, from left to right)
    #  and the 'image' column with the name of the image 'osdfhk7sd8.jpg'
    def csv_labels_to_df(labels_path = "Datasets/labels_preprocessed/HQ_quality.csv"):
        """
        From csv file in 'labels_path', converts into a panda dataframe
        The CSV file must contain the 'cadran_1', 'cadran_2',
    'cadran_3', 'cadran_4' columns (from first digit to last digit before the comma, from left to right)
    and the 'image' column with the name of the image 'osdfhk7sd8.jpg'
        :return:
        """
        df = pd.read_csv(labels_path, sep = ";")
        return(df)


"""
A main function to cut the digits on all images.
"""

if __name__ == "main":


    # ---- INITIALISATION ----

    # eleven folder 'Datasets'
    raw_dir = "Datasets_raw/"

    # may be HQ_digital, MQ_digital or LQ_digital
    cat_dir =  "LQ_digital"

    # path to Sacha's output, with the extracted screen
    preprocessed_dir = "Datasets_preprocessed/"+ cat_dir +"_preprocessing/"

    all_images = os.listdir(raw_dir + cat_dir)
    all_images_preprocessed = os.listdir(preprocessed_dir)

    # output path to save individual digits in
    # of the form "Datasets_digits/" and contains the '0', '1', ... 'X' folders
    digits_path = "Datasets_digits/"

    # Csv file with the image name, 'cadran_1', 'cadran_2', 'cadran_3', 'cadran_4' columns containing the digits' labels before the comma
    labels_path = "Datasets_labels/"+cat_dir+".csv"

    # convert file into dataframe
    labels_df   = csv_labels_to_df(labels_path)

    # ---- LOOP ----

    for ind in all_images_preprocessed:
        if ind != ".DS_Store":
            print(ind)
            image = cv2.imread(preprocessed_dir + ind)                  # get the extracted screen from img
            #warped = extract_screen(image)
            preprocessed_img = preprocess2(image)                       # preprocess the img
            dist = get_bd_dummy(preprocessed)                           # get bounding boxes' size

            # get the labels of the digits before the comma
            labels = labels_df[labels_df['image'] == ind][['cadran_1', 'cadran_2', 'cadran_3', 'cadran_4']].values

            # get bounding boxes and save truncated images in the folder corresponding to its label
            cut_and_affect_to_folder(preprocessed_img, dist, labels[0], \
                                     digits_path, ind, last_digit= 2)
            plt.close()



# DECOMMENT IF IMAGES NOT PREPROCESSED ALREADY
'''for ind in all_images:
    print(ind)
    image = cv2.imread(input_dir + ind)
    warped = extract_screen(image)
    preprocessed = preprocess_short(warped)
    dist = get_bd_short_wo_comma(preprocessed)
    preprocessed_img = warped
    labels = labels_df[labels_df['image'] == ind][['cadran_1', 'cadran_2', 'cadran_3', 'cadran_4']].values
    affect_to_folder(preprocessed_img, dist, labels[0], digits_path, ind)

    #plt.savefig(output_dir + "bd_plot_" + ind)
    plt.close()'''