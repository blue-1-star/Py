import cv2 as cv 
import sys 
import xlsxwriter
from PIL import Image
import easyocr
import os
import pandas as pd 
from glob import glob
import time 
import numpy as np
from pathlib import Path 
import ctypes
import matplotlib.pyplot as plt
import torch
device = torch.device('cpu')

def getting_pixel_counts(img_path, show_images = True): 
    img = cv.imread(img_path)
    if img is None: 
        sys.exit("Could not read image")
        
    # Converting the image to HSV 
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)  
    # Creating a white mask for green colors 
    mask = cv.inRange(hsv_img, (30, 50, 50), (85, 255, 255))
        
    plt.figure(dpi=300)  # Increase DPI to 300
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
    plt.figure(dpi=300)  # Increase DPI for the second plot
    plt.imshow(mask)
    plt.axis('off')
    plt.show() 
    
    white_pixel_count = cv.countNonZero(mask) # number of green pixels
    
    return white_pixel_count


def get_sample_name(image_path):
    # Image Preprocessing 
    reader = easyocr.Reader(['en'])
    output_array = reader.readtext(image_path, detail=0)
    return output_array[-1]

def get_paper_area_px(img_path, min_area=18000, save_squares=True, squares_folder="extracted_squares", debug=True):
    img = cv.imread(img_path)

    if img is None: 
        sys.exit("No image found")
        
    # Convert image to grayscale for better edge detection
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blurred, 50, 150)
    cnts, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # Store areas of detected grids
    grid_area = 0

    for c in cnts: 
        area = cv.contourArea(c)
        # Only process contours within the area threshold
        if area>min_area: 
            x, y, w, h = cv.boundingRect(c)
            width = w
            height = h
            aspect_ratio = width / height
            grid_area = area
                
            # Check for aspect ratio close to 1 (square-like shapes)
            if 0.8 < aspect_ratio < 1.2:
                ROI = img[y:y + h, x:x + w]
                
                # Create a folder for extracted squares if it doesn't exist
                if not os.path.exists(squares_folder):
                    os.makedirs(squares_folder)
                
                # Save the extracted square if needed
                if save_squares: 
                    square_file_name = f"{Path(img_path).stem}_square_{x}_{y}.png"
                    cv.imwrite(os.path.join(squares_folder, square_file_name), ROI)
                
                # Optionally show the extracted ROI
                if debug:
                    plt.figure(dpi=300)
                    plt.imshow(cv.cvtColor(ROI, cv.COLOR_BGR2RGB))
                    plt.axis('off')
                    plt.show()

    if not grid_area:
        print("No squares found within the area threshold.")
        return None

    return grid_area   

def generate_excel_file(folder_path, file_name):
    # Actual dimensions of the paper in mm 
    paper_width_mm, paper_height_mm = 20, 16 
    paper_area_mm = paper_width_mm * paper_height_mm
    
    # Variables required to create the excel file 
    excel_file_name = file_name + ".xlsx"
    workbook = xlsxwriter.Workbook(excel_file_name)
    worksheet = workbook.add_worksheet()
    
    # Creating the headers
    header_data = ["File name", "Sample name", "Grid area (px)", "Pixels per mm^2", "Green area (px)", "Total area (px)", "Green area (mm^2)"]
    header_format = workbook.add_format({'bold': True,'bottom': 2,})
    # Writing the headers of the excel file
    for col_num, data in enumerate(header_data): 
        worksheet.write(0, col_num, data, header_format)
        
    # Processing the image file 
    image_files = glob(os.path.join(folder_path, "*.jpg"))
    row = 1
    col = 0
    for cur_img_path in image_files: 
        img = cv.imread(cur_img_path)
        row_data = [] 
        file_name = os.path.basename(cur_img_path)
        
        # Getting data from file 
        sample_name = get_sample_name(cur_img_path)
        
        # Getting paper area in pixels 
        paper_area_px = get_paper_area_px(cur_img_path)
        
        # How many pixels is 1 mm^2? 
        single_mm_px = round((paper_area_px / paper_area_mm), 5)
        
        # Getting data from image 
        white_pixels = getting_pixel_counts(cur_img_path, show_images = False)
        total_pixels = img.shape[0] * img.shape[1]
        
        white_pixels_area_mm = round((white_pixels / single_mm_px), 5)
        
        row_data.extend([file_name, sample_name, paper_area_px, single_mm_px, white_pixels, total_pixels, white_pixels_area_mm])
        
        worksheet.write_row(row, 0, tuple(row_data))
        row += 1
    
    worksheet.autofit()
    workbook.close()


if __name__ == "__main__":
    # Path to folder with images 
    img_folder = r"C:\Users\HP\Desktop\Plant green area analysis\Images"
    
    start_time = time.time()
    generate_excel_file(img_folder, "Green area analysis")
    print("Excel file generated in ", int(time.time() - start_time), "seconds")