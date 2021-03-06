import os
import sys
import glob
import cv2
import numpy
from tqdm import tqdm

from google_scraper import scrape
from face_extractor import extract_faces

def preprocess_faces(keyword):
    in_dir = './data/raw/'
    out_dir = './data/faces/'
    dataset = keyword.lower().replace(" ", "_")
    faces_dir = os.path.join(out_dir, dataset)

    # check directory and create if necessary
    if not os.path.exists(faces_dir):
        os.makedirs(faces_dir)
    # empty directory
    for f in glob.glob(os.path.join(faces_dir, "*.jpg")):
        os.remove(f)

    # loop through our previously scraped images
    files = glob.glob(os.path.join(in_dir, dataset, "*.jpg"))
    nFiles = len(files)
    counter = 1
    for i in tqdm(range(nFiles)):
        try:
            orig_image = cv2.imread(files[i])
            # extract faces and resize to 256x256 px
            facelist = extract_faces(orig_image, 256)
            
            # write all face images to disk
            for j in range(len(facelist)):            
                cv2.imwrite(os.path.join(faces_dir, "{0}_{1}.jpg".format(i, j)), facelist[j][1])
        except:
            print("Unexpected error:", sys.exc_info()[0])

if __name__ == "__main__":

    # check directory and create if necessary
    if not os.path.isdir("./data/raw/"):
        os.makedirs("./data/raw/")

    print("Step 1: scrape the images from google")
    name=input("enter name of a person:")
    limit=20
    scrape(name, int(limit))

    # check directory and create if necessary
    if not os.path.isdir("./data/faces/"):
        os.makedirs("./data/faces/")

    print("Step 2: extract the faces")
    preprocess_faces(name)
    
    print("\n===============================================\n")
    print("I'm done for now, you should quality check your \ngenerated datasets in \"data/faces/\"!")
    print("\n===============================================\n")
