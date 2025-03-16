import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def load_normal():
    N = 20
    dists = {name:{'center':c, 
        'p':np.random.default_rng(seed).normal(size=(N,2))} 
        for name,c,seed in zip(
            ['A','B','C','D'],
            [(5,0),(0,-5),(-5,0),(0,5)],
            [320893160789365868340998054487457939632,
            215439026711583641876755721646163960581,
            208011755429501166934099738140089681345,
            260030451776685333648244439464574707322]) }

    dfs = []
    for (name,h) in dists.items():
        pts = np.array(h['center']) + h['p']
        _df = pd.DataFrame(pts,columns=['x','y'])
        _df['cls'] = name
        dfs.append(_df)
    return pd.concat(dfs)

def load_breast():
    features = ['id', 'clump', 'uniformity_cell_size', 'uniformity_cell_shape', 'marginal_adhesion','single_epithelial_cell_size', 'bare_nuclei', 'chromatin', 'normal_nucleoli', 'mitoses']
    cls_att = 'class'
    df = pd.read_csv('./corriges/data/breast-cancer-wisconsin.data.with_null',names=features+[cls_att])
    df = df.set_index('id')
    df = df.dropna()
    return df

datasets = {
    'iris':sns.load_dataset('iris'),
    'breast':load_breast(),
    'normal':load_normal()
}

if __name__ == "__main__":
    """
    Usage :
        python main.py --data Iris 

    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--data", type=str, help="the name of the dataset"
    )

    args = parser.parse_args()
    print(args.data)

    df = load_normal()

    X,y = (df.iloc[:,:-1].values,df.iloc[:,-1:].values)

    pca = PCA(n_components=2).fit(X)
    X_reduced = pca.transform(X)

    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot()
    ax.set_axis_off()
    ax.scatter(
        X_reduced[:, 0],
        X_reduced[:, 1],
        c=np.unique(y,return_inverse=True)[1],
        s=80,
        cmap='coolwarm'
    )
    plt.show()