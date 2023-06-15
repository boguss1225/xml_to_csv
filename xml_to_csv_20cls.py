from xml.etree import ElementTree
import csv
import os,glob
from tqdm import tqdm

# For statistics of the classes

# SOURCE AND DESTINATION
path = '/Users/bogus/Documents/1_STUDY/4_Projects/sperm_20_cls/1-2/train' # Source Folder
dstpath = '/Users/bogus/Documents/1_STUDY/4_Projects/sperm_20_cls/1-2/' # Destination Folder
csv_name = 'train.csv'
Delete_extension = True
New_extension=".JPG"

# GET XML FILE LIST
os.chdir(path)
xml_files = glob.glob("*.xml")

# CREATE CSV FILE
csvfile = open(os.path.join(dstpath,csv_name),'w',encoding='utf-8')
csvfile_writer = csv.writer(csvfile)

# ADD THE HEADER TO CSV FILE
cols = ["filename", 
        "Normal", 
        "Normal_flapped", 
        "No_head", 
        "Small_head", 
        "Vacuolated_head",
        "Double_head",
        "Bend_neck",
        "Thick_midpiece",
        "Bend_midpiece",
        "Cytoplasmic_droplet",
        "No_tail",
        "Short_tail",
        "Coiled_tail",
        "Hairpin_tail",
        "Terminal_coiled_tail",
        "Aggregation",
        "Unfocusing",
        "Bacteria",
        "Bacteria_cluster",
        "Debris"]
csvfile_writer.writerow(cols)

for xml in tqdm(xml_files):
    # init xml tree
    tree = ElementTree.parse(xml)
    root = tree.getroot()

    # EXTRACT COMMON DETAILS
    filename = root.find("filename").text

    # Delete extension from filename
    if Delete_extension:
        filename = os.path.splitext(filename)[0]
        filename = filename+New_extension

    # init a line in csv
    csv_line = [filename, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0]
    
    # FOR EACH OBJECT
    for obj in root.findall("object"):
        # EXTRACT OBJECT DETAILS  
        label = obj.find("name").text

        # find index of the label
        index_seq = cols.index(label)

        # add 1 count
        csv_line[index_seq] += 1

    # ADD A NEW ROW TO CSV FILE
    csvfile_writer.writerow(csv_line)

csvfile.close()
print("result saved to ->",csv_name)