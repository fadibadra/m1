import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
from abc import ABC, abstractmethod
from cbp import DATA_FOLDER

class Dataset(object):
    def __init__(self, name):
        self.name = name

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return (self.X[idx], self.y[idx])
    
    def __str__(self):
        return self.name


class Breast(Dataset):
    """ Breast Cancer Wisconsin Dataset."""
    def __init__(self):
        super().__init__('breast')
        self.features = ['clump', 'uniformity_cell_size', 'uniformity_cell_shape', 'marginal_adhesion','single_epithelial_cell_size', 'bare_nuclei', 'chromatin', 'normal_nucleoli', 'mitoses']
        self.cls_att = 'class'
        # df = pd.read_csv('../data/breast-cancer-wisconsin.data.with_null',names=self.features+[self.cls_att])
        df = pd.read_csv(DATA_FOLDER / 'breast-cancer-wisconsin.data.with_null',names=['id']+self.features+[self.cls_att]).loc[1:,:].dropna()
        self.X = df[self.features].values
        self.y = df[self.cls_att].values

class Images(Dataset, ABC):
    """ Abstract class for image datasets. """

    @classmethod
    def vect(cls,X):
        return X.reshape(len(X),-1)
    
    @classmethod
    @abstractmethod
    def im(cls,X):
        ...

    def as_vectors(self):
        d = copy.copy(self)
        d.X = Images.vect(d.X)
        return d
    
    def as_images(self):
        d = copy.copy(self)
        d.X = type(self).im(d.X)
        return d

    def afficher_images(self,indices):
        n = len(indices)
        if n == 1:
            plt.imshow(self.X[indices[0]]), self.y[indices[0]]
        else:
            fig, axes = plt.subplots(nrows=1, ncols=n,figsize=(2*n, n), dpi=100)
            for i,idx in enumerate(indices):
                axes[i].imshow(self.X[idx])
                axes[i].set_title(f'Image {idx} Label {self.y[idx]}')

class CT(Images):
    """ CT Images dataset. """
    def __init__(self):
        super().__init__('ct_images')
        data = np.load(DATA_FOLDER / 'ct_images/ct.npz', allow_pickle=True)
        self.X = Images.vect(data['X'])
        self.y = data['y'] # pd.read_csv('../data/ct_images/overview.csv', sep=',')['Contrast'].values.astype(np.int64)

    @classmethod
    def im(cls,X):
        return X.reshape(len(X),512,512,1)


class Lung(Images):
    """ Lung Cancer Dataset. """
    def __init__(self):
        super().__init__('lung')
        data = np.load(DATA_FOLDER / 'lung-cancer-smoking-dataset/lung_cancer.npz')
        self.X = Images.vect(data['images'])
        self.y = data['labels']

    @classmethod
    def im(cls,X):
        return X.reshape(len(X),512,512,3)



def load_dataset(name:str) -> Dataset:
    """ Loads a dataset given its name. """
    return {
        'breast':Breast,
        'ct_images':CT,
        'lung':Lung
    }[name]() 

