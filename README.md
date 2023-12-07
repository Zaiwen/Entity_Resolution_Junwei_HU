# When GDD meets GNN: A Knowledge-driven Neural Connection for Effective Entity Resolution
Entity Resolution(ER) is the process of identifying and linking different records that refer to the same real-world entity. It is commonly used in data integration, data cleansing, fraud detection, and other applications where it is important to have accurate and consistent data. This work investigates the ER problem in property graphs. Our proposed ER framework is divided into three parts: blocking, pruning, and matching. As shown in the following figure.  
![image](https://github.com/Zaiwen/Entity_Resolution_Junwei_HU/blob/main/GraphER/Figure/framework.png)

## Input data
The source data can be obtained from here：https://github.com/hujunnwei/data-conversion  
We also provide code for data conversion to convert relational data and graph data into each other.

## Blocking
Blocking includes structural embedding, attribute embedding, and vector computation, respectively.  
### 1. Structural Embedding
structural reference https://ericdongyx.github.io/metapath2vec/m2v.html  
'''
cd Blocking/metapath2vec/ && make
'''
### 2. Attribute Embedding
attribute embedding reference https://github.com/rcap107/embdi and https://github.com/qcri/DeepBlocker  
### 3. LSH algorithm
By using the above embedding methods, vectorization of the property graph is completed based on its structure and attribute. The obtained embedding vector will be input into the LSH algorithm *FALCONN*, which is a commonly used nearest neighbor search method in high-dimensional spaces.  
vector computation reference https://github.com/falconn-lib/falconn  
Through the above operations, we will obtain blocks based on structural similarity and blocks based on attribute similarity respectively, and then merge them to obtain new blocks.

## Pruning
We provide two pruning strategies to remove significantly mismatched entity pairs in each block, one through edge weighting and the other through similarity. The calculation formula is described in the paper, and the code is in the Pruning folder. 

## Matching
The matching stage is to further verify the candidate matching pairs obtained after pruning operations. We will test the candidate pairs through the constraints carried by GDD rules. If all the constraints of any GDD are met, they will be considered for matching, otherwise they will not be considered for matching. GDD mining and ER algorithm, see paper *Certus: An effective entity resolution approach with graph differential dependencies (GDDs)*.

## Evaluation
In addition to recall, precision, and F1 score, we also provide purity and CSSR to measure the quality of candidate sets generated during the blocking, pruning, and matching phases, as shown in the formula in the paper.

