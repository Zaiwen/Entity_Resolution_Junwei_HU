import ctypes
import numpy as np
import pandas as pd
import os
import time
import re
import copy
import merging_blocks
import edge_weight
import dice_coefficient
from ctypes import *
from match_prediction import matching
from blocks_generation import get_blocks
from convert import transformation
from meta_paths import sentence_generation
from autoencoder.loader import Loader
from autoencoder.sentence_embedding import AutoEncoderEmbedding

def get_metapath(pattern_path):
    type_mapping = dict()
    type_mapping['0'] = 'R'
    type_mapping['1'] = 'A'
    type_mapping['2'] = 'C'
    path = []
    with open(pattern_path, 'r', encoding='utf-8')as f:
        for line in f:
            line = re.findall(r':(.*?)\)', line.strip('\n'))
            if line not in path:
                path.append(line)
    # Select the longest path and generate the meta-path
    for i in range(len(path)):
        for j in range(len(path)):
            if i != j and path[i][1] == path[j][0]:
                path[i].append(path[j][1])
    metapath = copy.deepcopy(max(path, key=len))
    for i in range(len(max(path, key=len))):
        if i < len(max(path, key=len)) - 1:
            metapath.append(metapath[len(max(path, key=len)) - 2 - i])
    mapping_metapath = ""
    for i in range(len(metapath)):
        mapping_metapath += type_mapping[metapath[i]]

    return mapping_metapath
    
def get_attribute(table_txt, rule_path):
    all_attributes = []
    with open(table_txt, 'r', encoding='utf-8')as f:
        for line in f:
            line = line.strip('\n').split('\t')
            all_attributes = copy.deepcopy(line)
            break
    attributes = []
    with open(rule_path, 'r', encoding='utf-8')as f:
        for line in f:
            if '->' in line:
                line1 = line.strip('\n').split('->')[0].rsplit(' ', 1)[0]
                line2 = line1.split('=')[0].split('.')[1]
                if line2 not in attributes and line2 in all_attributes:
                    attributes.append(line2)
    
    return attributes

if __name__ == "__main__":

    start = time.time()

    network_path = "dataset/network"
    pattern_path = "GDDs/frequent_patterns/pattern0.txt"
    rule_path = "GDDs/linking_rules/rule0.txt"
    table_txt = "dataset/network/table.txt"
    table_csv = "dataset/network/table.csv"
    # Mapping_graph-patterns_to_meta-paths_and_meta-paths_based_sequence_generation
    numwalks = 10
    walklength = 100
    sentence_path = 'output_file/FZ.' + get_metapath(pattern_path) + '.w' + str(numwalks) + '.l' + str(walklength) + '.txt'
    sentence_generation(network_path, get_metapath(pattern_path), sentence_path, numwalks, walklength)
    print("--random walk guided by graph pattern done")

    # Metapath2vec_training_driven_by_graph-patterns
    structural_embedding = "embedding/FZ.structural.embedding"
    dll = ctypes.cdll.LoadLibrary
    metapath2vec = dll('./metapath2vec/metapath2vec.so')
    c1 = c_char_p(bytes("start", "utf-8"))
    c2 = c_char_p(bytes("-train", "utf-8"))
    c3 = c_char_p(bytes(sentence_path, "utf-8"))
    c4 = c_char_p(bytes("-output", "utf-8"))
    c5 = c_char_p(bytes(structural_embedding, "utf-8"))
    c6 = c_char_p(bytes("-pp", "utf-8"))
    c7 = c_char_p(bytes("1", "utf-8"))
    c8 = c_char_p(bytes("-size", "utf-8"))
    c9 = c_char_p(bytes("128", "utf-8"))
    c10 = c_char_p(bytes("-window", "utf-8"))
    c11 = c_char_p(bytes("7", "utf-8"))
    c12 = c_char_p(bytes("-negative", "utf-8"))
    c13 = c_char_p(bytes("5", "utf-8"))
    c14 = c_char_p(bytes("-threads", "utf-8"))
    c15 = c_char_p(bytes("32", "utf-8"))
    c = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15]
    c_arr = (c_char_p*len(c))(*c) 
    metapath2vec.main(len(c), ctypes.pointer(c_arr))
    print('\n' + "--structural embedding done")

    # Rule_carrying_knowledge_mapping
    attributes = get_attribute(table_txt, rule_path)
    print("--attribute mapping in rules done")

    # Autoencoder_training_driven_by_rules
    attribute_embedding = "embedding/FZ.attribute.embedding.txt"
    df = pd.read_csv(table_csv)
    Ae = Loader(AutoEncoderEmbedding())
    Ae.datasets(df, attributes , attribute_embedding)
    attribute_embedding = "embedding/FZ.attribute.embedding"
    print("--attribute embedding done")

    # Vector_transformation (txt->npy)
    sdimension = 128 # structural_embedding_dimension
    adimension = 150 # attribute_embedding_dimension
    convert_se = transformation(structural_embedding, sdimension)
    convert_ae = transformation(attribute_embedding, adimension)
    print("--vector transformation done")

    # Blocks_generation
    euclidean_distance = 0.1 # distance_threshold_in_the_blocking_phase
    sblocks_path = "output_file/structural_information_based_blocks.txt"
    get_blocks(structural_embedding + '.txt', convert_se, sblocks_path, euclidean_distance) 
    ablocks_path = "output_file/attribute_information_based_blocks.txt"
    get_blocks(attribute_embedding + '.txt', convert_ae, ablocks_path, euclidean_distance) 
    print("--blocking phase done")

    # Put_structure_based_blocks_and_attribute_based_blocks_together
    blocks_path = "output_file/put_together_blocks.txt"
    merging_blocks.readfile(sblocks_path, ablocks_path, blocks_path)
    print("--put blocks together done")

    # Pruning_blocks_with_edge_weight
    eblocks_path = "output_file/blocks_pruning_with_edge_weight.txt"
    edge_weight.pruning(blocks_path, eblocks_path)

    # Pruning_blocks_with_dice_coefficient
    dice_threshold = 0.2 # dice_threshold_in_the_pruning_phase
    dblocks_path = "output_file/blocks_pruning_with_dice_coefficient.txt"
    dice_coefficient.pruning(eblocks_path, dblocks_path, table_txt, dice_threshold) 
    print("--pruning phase done")

    # Using_rules_to_determine_whether_similar_entities_match
    matching_pairs_path = "output_file/matching_pairs.txt"
    matching(dblocks_path, matching_pairs_path, table_txt, rule_path)
    print("--matching phase done")

    end = time.time()
    print("Total time: %.2fs" %(end-start))