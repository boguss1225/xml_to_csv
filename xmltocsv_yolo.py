from xml.etree import ElementTree
import csv
import os,glob
from tqdm import tqdm

# SOURCE AND DESTINATION
path = '/Users/bogus/Desktop/test' # Source Folder
dstpath = '/Users/bogus/Desktop/dst' # Destination Folder
csv_name = 'data_test.csv'
Delete_extension = True

# GET XML FILE LIST
os.chdir(path)
xml_files = glob.glob("*.xml")

# CREATE CSV FILE
csvfile = open(os.path.join(dstpath,csv_name),'w',encoding='utf-8')
csvfile_writer = csv.writer(csvfile)

# ADD THE HEADER TO CSV FILE
cols = ["filename", "x", "y", "width", "height", "label"]
csvfile_writer.writerow(cols)

for xml in tqdm(xml_files):
    tree = ElementTree.parse(xml)
    root = tree.getroot()

    # EXTRACT COMMON DETAILS
    filename = root.find("filename").text
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    # Delete extension from filename
    if Delete_extension:
        filename = os.path.splitext(filename)[0]
    
    # FOR EACH OBJECT
    for obj in root.findall("object"):
        # EXTRACT OBJECT DETAILS  
        label = obj.find("name").text
        bndbox = obj.find("bndbox")
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)

        # GET object's position and size
        x_center = (xmax+xmin)/2
        y_center = (ymax+ymin)/2
        obj_w = xmax-xmin
        obj_h = ymax-ymin

        # CONVERT TO YOLO FORMAT 0~1
        x = str(round(x_center/width,6))
        y = str(round(y_center/height,6))
        w = str(round(obj_w/width,6))
        h = str(round(obj_h/height,6))

        csv_line = [filename, x, y, w, h, label]

        # ADD A NEW ROW TO CSV FILE
        csvfile_writer.writerow(csv_line)

csvfile.close()
print("result saved to ->",csv_name)
