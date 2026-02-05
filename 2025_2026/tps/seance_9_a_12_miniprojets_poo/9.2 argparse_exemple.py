from sklearn.model_selection import train_test_split
from cbp.similarity.measures import euclidean_sim, cosin
from cbp.algo import knn, ctcoat
from cbp.data.datasets import load_dataset

def compute_accuracy(algo, data, sim, k=7):

    # Randomly split the dataset with reproducibility
    X_cb, X_test, y_cb, y_test = train_test_split(data.X, data.y, train_size=80, stratify=data.y, random_state=34)

    # Compute accuracy
    acc = 0.
    for x, y_true in zip(X_test,y_test):
        y_pred = algo.predict(x, X_cb, y_cb, sim, n_neighbors=k)
        print(f'y_true={y_true}, y_pred={y_pred}')
        if y_pred == y_true:
            acc += 1
    acc /= len(X_test)

    return acc

if __name__ == "__main__":
    """
    Usage :
        python exemple.py --data [breast|ct_images] -a [coat|knn]

    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--data", type=str, help="the name of the dataset"
    )
    parser.add_argument(
        "-a", "--algo", type=str, help="the prediction algorithm, either CoAT or kNN"
    )
    
    args = parser.parse_args()

    algo_name = args.algo if args.algo else 'knn'
    dataset_name = args.data if args.data else 'breast'

    print(f'== {algo_name} sur {dataset_name}')

    # load the dataset
    data = load_dataset(dataset_name)

     # choose a similarity measure
    sim = euclidean_sim if dataset_name == "breast" else cosin

    (algo, k) = (ctcoat,None) if algo_name == 'coat' else (knn,7)

    acc = compute_accuracy(algo, data, sim, k)

    print(f'La performance de {algo_name} sur {data} est {acc:.4f}%')

    
