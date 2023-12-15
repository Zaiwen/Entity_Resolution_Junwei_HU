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
**GraphER** requires the input of a graph dataset, and here we show how to use **GraphER** to conduct experiments on the benchmark ER dataset fodors-zagats. Its original dataset can be found in `dataset/relational-dataset`. First, we convert the relational data into graph data by executing `dataset/preprocessing.py`, and then execute `dataset/txt2csv.py` to save the attribute values carried by the entity types that need to be resolved, all files will be saved in `dataset/network`. You can find other datasets and preprocessed files here：https://github.com/hujunnwei/data-conversion.  

## Preliminaries
### Word embedding
We used fastText for word embedding that is pre-trained on Wikipedia. You can download it from here：https://fasttext.cc/docs/en/pretrained-vectors.html and unzip it to the path specified in `autoencoder/configurations.py`.  
### Rule mining
You can obtain detailed rule definitions and mining processes from these two papers：*Discovering Graph Differential Dependencies* and *Certus: An effective entity resolution approach with graph differential dependencies (GDDs)*. Here we show the example of frequent graph patterns such as `GDDs/frequency_ patterns/pattern0.txt` and linking rules such as `GDDs/linking_ rules/rule0.txt`.

## Running example
We use the default dataset fodors-zagats, and you can directly run the `main.py` file to perform entity resolution using the following command:  
```
python main.py
```
When run successfully, the following information appears in the terminal.
```
(python3.6)[hujw@localhost hujw]$ python main.py
--random walk guided by graph pattern done
Starting training using file output_file/FZ.RACAR.w10.l100.txt
Alpha: 0.000002  Progress: 100.08%  Words/thread/sec: 5.03k  
--structural embedding done
--attribute mapping in rules done
Loading FastText model
Training AutoEncoder model
Obtaining node embeddings
--attribute embedding done
--vector transformation done
--blocking phase done
--put blocks together done
--pruning phase done
--matching phase done
Total time: 183.64s
```
You can find all the parameters in `main.py`, and the structural embedding and attribute embedding vectors can be found in the `embedding` folder. The intermediate files generated during this execution process will be saved in `output_file`, the final ER result is saved in `output_file/matching_pairs.txt`, as shown below, predicts that the two entities appearing in each row are the same entity.  
```
821|70
67|818
843|92
78|829
81|832
99|850
762|11
87|838
74|825
751|0
...
```









