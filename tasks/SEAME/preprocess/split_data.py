'''
Generates train-dev-test split

To-do:
 - Add conversation data to split

Peter Wu
peterw1@andrew.cmu.edu
'''

import os
import pickle
import random


SEED = 0
TRAIN_FRAC = 0.8
DEV_FRAC = 0.1

TRAIN_PATHS_FILE = 'train_paths.txt'
DEV_PATHS_FILE = 'dev_paths.txt'
TEST_PATHS_FILE = 'test_paths.txt'
TRAIN_YS_FILE = 'train_ys.txt'
DEV_YS_FILE = 'dev_ys.txt'
TEST_YS_FILE = 'test_ys.txt'

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERVIEW_MFCC_DIR = os.path.join(parent_dir, 'data/interview/mfcc')
CONVERSATION_MFCC_DIR = os.path.join(parent_dir, 'data/conversation/mfcc')

SPLIT_DIR = os.path.join(parent_dir, 'split')
if not os.path.exists(SPLIT_DIR):
    os.makedirs(SPLIT_DIR)
train_paths_path = os.path.join(SPLIT_DIR, TRAIN_PATHS_FILE)
dev_paths_path = os.path.join(SPLIT_DIR, DEV_PATHS_FILE)
test_paths_path = os.path.join(SPLIT_DIR, TEST_PATHS_FILE)
train_ys_path = os.path.join(SPLIT_DIR, TRAIN_YS_FILE)
dev_ys_path = os.path.join(SPLIT_DIR, DEV_YS_FILE)
test_ys_path = os.path.join(SPLIT_DIR, TEST_YS_FILE)

interview_mfcc_files = os.listdir(INTERVIEW_MFCC_DIR)
interview_mfcc_files = [f for f in mfcc_files if f.endswith('.mfcc')]
conversation_mfcc_files = os.listdir(CONVERSATION_MFCC_DIR)
conversation_mfcc_files = [f for f in mfcc_files if f.endswith('.mfcc')]

interview_paths = [os.path.join(INTERVIEW_MFCC_DIR, f) for f in interview_mfcc_files]
conversation_paths = [os.path.join(CONVERSATION_MFCC_DIR, f) for f in conversation_mfcc_files]
paths = interview_paths+conversation_paths

random.seed(SEED)
random.shuffle(paths)

num_samples = len(paths)
num_train = int(TRAIN_FRAC*num_samples)
num_dev = int(DEV_FRAC*num_samples)

train_paths = paths[:num_train]
dev_paths = paths[num_train:num_train+num_dev]
test_paths = paths[num_train+num_dev:]

INTERVIEW_TEXT_DIR = os.path.join(parent_dir, 'data/interview/transcript_clean/phaseI')
CONVERSATION_TEXT_DIR = os.path.join(parent_dir, 'data/conversation/transcript_clean/phaseI')
interview_txt_files = os.listdir(INTERVIEW_TEXT_DIR)
interview_txt_files = [f for f in interview_txt_files if f.endswith('.txt')]
conversation_txt_files = os.listdir(CONVERSATION_TEXT_DIR)
conversation_txt_files = [f for f in conversation_txt_files if f.endswith('.txt')]
interview_txt_paths = [os.path.join(INTERVIEW_TEXT_DIR, f) for f in txt_files]
conversation_txt_paths = [os.path.join(CONVERSATION_TEXT_DIR, f) for f in txt_files]
txt_paths = interview_txt_paths+conversation_txt_paths
all_ys = {}
for f in txt_paths:
    with open(f, 'r') as inf:
        lines = inf.readlines()
    lines = [l.strip() for l in lines]
    for l in lines:
        tokens = l.split()
        fid = tokens[0]+'_'+tokens[1]+'_'+tokens[2]
        file_name = fid+'.mfcc'
        mfcc_dir = INTERVIEW_MFCC_DIR if 'interview' in f else CONVERSATION_MFCC_DIR
        file_path = os.path.join(mfcc_dir, file_name)
        start_i = len(fid)+1
        y_label = l[start_i:].strip()
        if len(y_label) > 0:
            all_ys[file_path] = y_label
train_ys = [all_ys[path] for path in train_paths if path in all_ys]
dev_ys = [all_ys[path] for path in dev_paths if path in all_ys]
test_ys = [all_ys[path] for path in test_paths if path in all_ys]

with open(train_paths_path, 'w+') as ouf:
    for path in train_paths:
        if path in all_ys:
            ouf.write('%s\n' % path)
with open(dev_paths_path, 'w+') as ouf:
    for path in dev_paths:
        if path in all_ys:
            ouf.write('%s\n' % path)
with open(test_paths_path, 'w+') as ouf:
    for path in test_paths:
        if path in all_ys:
            ouf.write('%s\n' % path)

with open(train_ys_path, 'w+') as ouf:
    for y in train_ys:
        ouf.write('%s\n' % y)
with open(dev_ys_path, 'w+') as ouf:
    for y in dev_ys:
        ouf.write('%s\n' % y)
with open(test_ys_path, 'w+') as ouf:
    for y in test_ys:
        ouf.write('%s\n' % y)
