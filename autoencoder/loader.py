import numpy as np
import pandas as pd
from pathlib import Path


class Loader:
    def __init__(self, tuple_embedding_model):
        self.tuple_embedding_model = tuple_embedding_model

    def validate_columns(self):
        #Assumption: id column is named as id
        if "id" not in self.cols_to_block:
            self.cols_to_block.append("id")
        self.cols_to_block_without_id = [col for col in self.cols_to_block if col != "id"]

        #Check if all required columns are in left_df
        check = all([col in self.df.columns for col in self.cols_to_block])
        if not check:
            raise Exception("Not all columns in cols_to_block are present in the dataset")



    def preprocess_datasets(self):
        self.df = self.df[self.cols_to_block]

        self.df.fillna(' ', inplace=True)

        self.df = self.df.astype(str)

        self.df["_merged_text"] = self.df[self.cols_to_block_without_id].agg(' '.join, axis=1)

        #Drop the other columns
        self.df = self.df.drop(columns=self.cols_to_block_without_id)



    def datasets(self, df, cols_to_block, out_embedding):
        self.df = df
        self.cols_to_block = cols_to_block

        self.validate_columns()
        self.preprocess_datasets()
        outfile=open(out_embedding, 'w', encoding='utf-8')

        self.tuple_embedding_model.preprocess(self.df["_merged_text"])

        print("Obtaining node embeddings")
        self.tuple_embeddings = self.tuple_embedding_model.get_tuple_embedding(self.df["_merged_text"])
        for i in range(len(self.tuple_embeddings)):
            outfile.write(str(self.df.values[i][0]))
            outfile.write(" ")
            for j in range(len(self.tuple_embeddings[i])):
                outfile.write(str(self.tuple_embeddings[i][j]))
                outfile.write(" ")
            outfile.write("\n")

