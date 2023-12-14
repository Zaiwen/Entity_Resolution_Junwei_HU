# When GDD meets GNN: A Knowledge-driven Neural Connection for Effective Entity Resolution
Entity Resolution(ER) is the process of identifying and linking different records that refer to the same real-world entity. It is commonly used in data integration, data cleansing, fraud detection, and other applications where it is important to have accurate and consistent data. This work investigates the ER problem in property graphs. Our proposed ER framework, called **GraphER**, is divided into three parts: blocking, pruning, and matching. As shown in the following figure.  
![image](https://github.com/Zaiwen/Entity_Resolution_Junwei_HU/blob/main/framework.png)

## Requirements
* python3.6
* g++

## Installation
First, you can install the external libraries in requirements.txt through:  
```
pip install -r requirements.txt
```
Second, you can build the program metapath2vec.cpp through:  
```
cd metapath2vec
g++ -o metapath2vec.so -shared -fPIC metapath2vec.cpp
```
Then the metapath2vec.so dynamic library file will be generated.    

## Dataset
**GraphER** requires the input of a graph dataset, and here we show how to use **GraphER** to conduct experiments on the benchmark ER dataset fodors-zagats. Its original dataset can be found in `dataset/relational-dataset`. First, we convert the relational data into graph data by executing `dataset/preprocessing.py`, and then execute `txt2csv.py` to save the attribute values carried by the entity types that need to be resolved, all files will be saved in `dataset/network`.


## Input data
The source data can be obtained from here：https://github.com/hujunnwei/data-conversion  
We also provide code for data conversion to convert relational data and graph data into each other.

## Blocking
Blocking includes structural embedding, attribute embedding, and vector computation, respectively.  
### 1. Structural Embedding
structural reference https://ericdongyx.github.io/metapath2vec/m2v.html  
run ```meta_paths.py``` generates a sequence and inputs it into metapath2vec for training.
```
cd metapath2vec/ && make
./metapath2vec -train input_file -output output_file
``` 
### 2. Attribute Embedding
attribute embedding reference https://github.com/rcap107/embdi and https://github.com/qcri/DeepBlocker  
Firstly, create a heterogeneous tripartite graph to guide random walks and learn the distributed representation of attribute values.  
```
cd embdi/
python main.py -f path/to/config/file
```
Secondly, use an encoder-decoder feedforward neural network to learn the potential representations of nodes.  
```
cd autoencoder/
python main.py
```
Finally, each node will have two embeddings: a structural embedding and an attribute embedding.
### 3. LSH Algorithm
vector computation reference https://github.com/falconn-lib/falconn  
The obtained embedding vector will be input into the LSH algorithm *FALCONN*, which is a commonly used nearest neighbor search method in high-dimensional spaces.  
```
pip install FALCONN
```
For detailed usage instructions, please refer to https://github.com/FALCONN-LIB/FALCONN/wiki/How-to-Use-FALCONN, we will obtain blocks based on structural similarity and blocks based on attribute similarity respectively, and then merge them through run ```merge_blocks.py```.

## Pruning
We provide two pruning strategies to remove significantly mismatched entity pairs in each block, one through edge weighting ```edge_weighting.py``` and the other through similarity ```dice_calculation.py```. 

## Matching
The matching stage is to further verify the candidate matching pairs obtained after pruning operations. We will test the candidate pairs through the constraints carried by GDD rules ```match_prediction.py```. If all the constraints of any GDD are met, they will be considered for matching, otherwise they will not be considered for matching. GDD mining and ER algorithm, see paper *Certus: An effective entity resolution approach with graph differential dependencies (GDDs)*.

## Evaluation
In addition to recall, precision, and F1 score, we also provide purity and CSSR to measure the quality of candidate sets generated during the blocking, pruning, and matching phases, as shown in the folder ```Evaluation```.

