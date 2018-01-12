import numpy as np
import matplotlib.pyplot as plt
import json
from tsne import bh_sne
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def dim_reduction(channel_dict, reduced_dim=2):

    """
    "we normalized each column by Z-scoring: we substracted its mean and
    then divided by its standard deviation"

    since we are having a dictionary here, i will for now convert it into
    a numpy array and at the end just assign it again to the dictionary keys
    """

    n_channels = len(channel_dict.keys())
    n_trace_values = len(list(channel_dict.values())[0])
    data_array = np.zeros((n_channels, n_trace_values))

    for counter, key in enumerate(channel_dict.keys()):
        data_array[counter,:] = channel_dict[key]

    for column in range(n_trace_values):
        data_array[:,column] = (data_array[:,column] - \
                                np.mean(data_array[:,column])) / \
                                np.std(data_array[:,column])



################################################################################
############################ DEMO FOR VISUALIZATION ############################
################################################################################
    # apply tsne with 5 different levels of perplexity
    # and then apply kmeans clustering
    # TODO Demo Version, find one perplexity you wanna use
    kmeans = KMeans(n_clusters=20)
    plt.figure("TSNE Results", figsize=(20,10))
    print('\n\n\n\n\n\n START \n\n\n\n\n\n')
    for counter, i in enumerate(range(5,46,10)):
        print('\n\n\n HEHHEJKSHLHDLKAJSDH \n\n\n')
        # dimensionality reduction
        data2d = bh_sne(data_array, perplexity=i)

        # apply clustering and retrieve resulting labels
        kmeans.fit(data2d)
        if counter == 0:
            labels = kmeans.labels_

        # generate plot
        plt.subplot(2,3,counter+1)
        plt.title("t-SNE with perplexity of " + str(i))
        plt.scatter(data2d[:,0], data2d[:,1], linewidths=0.1, c=labels)


    # apply pca for comparison
    pca = PCA(n_components=2)
    data2d = pca.fit_transform(data_array)

    kmeans.fit(data2d)
    labels = kmeans.labels_

    plt.subplot(2,3,6)
    plt.title("PCA")
    plt.scatter(data2d[:,0], data2d[:,1], linewidths=0.1, c=labels)

    # plot results
    plt.show()
################################################################################
################################################################################

    data2d = bh_sne(data_array, d=reduced_dim, perplexity=30)

    # TODO transform into panda dataframe or something, keep the ids!
    return 0

if (__name__=="__main__"):

    # number of dimensions the data was reduced too in the paper
    # corresponding to the ion
    ion_dim = {"K":16, "Na":21, "Ca":29, "IH":16, "KCa":16}

    # Get traces
    file_name = "Na_family.json"
    with open(file_name, 'r') as f:
        channel_dict = json.load(f)

    pp_channel_dict = dim_reduction(channel_dict)
