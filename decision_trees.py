#data science modules
import pandas as pd
import numpy as np

#scikit learn (model building and evaluation)
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn import cross_validation

#scikit learn (tree drawing)
from sklearn import tree
from IPython.display import Image

#for plotting
import matplotlib.pyplot as plt

#remove the comment mark below if running this in IPython
#%matplotlib inline

if __name__ == '__main__':
    file_path = '/Users/devinjackson/Documents/data/titanic.csv'
    df_all = pd.read_csv(file_path, sep=',')
    df = pd.read_csv(file_path, sep=',').dropna()
    print len(df_all)
    print len(df)
    num_records_all = df_all.shape[0]
    num