from convertToDb import generatePVDB
import argparse
from numberdetection import numberDetection
from officialshapedetection import shapeDetection

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-r", "--reference", required=False,
                help="path to reference OCR-A image",
                default="./images/digitreference.png")
args = vars(ap.parse_args())
shapeDetection(args["image"])

generatePVDB(10, 96)
