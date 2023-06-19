from xml.etree import ElementTree
import csv
import os,glob
from tqdm import tqdm

# SOURCE AND DESTINATION
path = '/Users/bogus/SynologyDrive2/SynologyDrive/230526_sperm_morphology_labeling_JS_TH_JW/1-2/test' # Source Folder
dstpath = '/Users/bogus/SynologyDrive2/SynologyDrive/230526_sperm_morphology_labeling_JS_TH_JW/1-2/' # Destination Folder
csv_name = 'test.csv'
Delete_extension = True

# GET XML FILE LIST
os.chdir(path)
xml_files = glob.glob("*.xml")

# CREATE CSV FILE
csvfile = open(os.path.join(dstpath,csv_name),'w',encoding='utf-8')
csvfile_writer = csv.writer(csvfile)

# ADD THE HEADER TO CSV FILE
cols = ['filename', 'width', 'height', 'class','xmin', 'ymin', 'xmax', 'ymax']
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

        csv_line = [filename, width, height, label, xmin, ymin, xmax, ymax]

        # ADD A NEW ROW TO CSV FILE
        csvfile_writer.writerow(csv_line)

csvfile.close()
print("result saved to ->",csv_name)
