import logging
import shutil
import os
from random import shuffle
import glob
from tqdm import tqdm
from utils import parse_json

# Initialize
logging.basicConfig(level=logging.DEBUG)
logging.info('Initialize ... ')

dataset = parse_json('./map_table.json')[0]
split_path = os.path.join('./', 'split')

train_img_dir = os.path.join(split_path, 'train/images')
test_img_dir = os.path.join(split_path, 'test/images')
val_img_dir = os.path.join(split_path, 'val/images')

train_lbl_dir = os.path.join(split_path, 'train/labels')
test_lbl_dir = os.path.join(split_path, 'test/labels')
val_lbl_dir = os.path.join(split_path, 'val/labels')

## Check and Create All Directory
logging.info('Update split folder ... ')
list_dir = [train_img_dir, test_img_dir, val_img_dir, train_lbl_dir, test_lbl_dir, val_lbl_dir]

for d in list_dir:
    if os.path.exists(d):        
        shutil.rmtree(d)
        os.makedirs(d)
        logging.info(f'Clear directory ({d})')  
    else:
        os.makedirs(d)
        logging.info(f'Create directory ({d})')

logging.info('Split custom data is starting')

##################################################################

# Get All Images in label_dir
img_list = glob.glob( os.path.join(dataset, '*.jpg' ))
shuffle(img_list)    # Shuffle data

# Split train/val/test with 8/1/1
range_total = len(img_list)
range_1 = int(range_total*0.8)
range_2 = int(range_total*0.9)

for idx in range(range_1):
    name, ext = os.path.splitext(img_list[idx])
    img_path=name+'.jpg'
    lbl_path=name+'.txt'
    shutil.copy2(img_path, train_img_dir)
    shutil.copy2(lbl_path, train_lbl_dir)

for idx in range(range_1, range_2):
    name, ext = os.path.splitext(img_list[idx])
    img_path=name+'.jpg'
    lbl_path=name+'.txt'
    shutil.copy2(img_path, test_img_dir)
    shutil.copy2(lbl_path, test_lbl_dir)

for idx in range(range_2, range_total):
    name, ext = os.path.splitext(img_list[idx])
    img_path=name+'.jpg'
    lbl_path=name+'.txt'
    shutil.copy2(img_path, val_img_dir)
    shutil.copy2(lbl_path, val_lbl_dir)         
    
logging.info('Split data finished')

for dir in list_dir:
    
    nums = len(os.listdir(dir))
    logging.info("Found {:>5} data in {}".format(nums, dir)) 
        
logging.info("All Done.")