import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
from tsne import bh_sne
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from mpldatacursor import datacursor
from prettytable import PrettyTable

def dim_reduction(main_df, reduced_dim=2, perplexity=30, n_kmeans_clusters=10):

    # create a numpy array for voltage trace values
    n_channels = len(main_df['Conc_Trace'])
    n_trace_values = len(main_df['Conc_Trace'][0])
    data_array = np.zeros((n_channels, n_trace_values))

    # copy values
    for row in range(n_channels):
        data_array[row] = main_df['Conc_Trace'][row]

    """
    "we normalized each column by Z-scoring: we substracted its mean and
    then divided by its standard deviation"
    """
    for column in range(n_trace_values):
        data_array[:,column] = (data_array[:,column] - \
                                np.mean(data_array[:,column])) / \
                                np.std(data_array[:,column])

    # apply t-SNE on data
    data2d = bh_sne(data_array, d=reduced_dim, perplexity=perplexity)

    # apply kmeans and save its labels for colorization
    kmeans = KMeans(n_clusters=n_kmeans_clusters)
    kmeans.fit(data2d)
    labels = kmeans.labels_

    # create list of labels, which will be displayed when clicking
    # on a datapoint
    text_list = [create_label_for_matplotlib(main_df.loc[counter])      \
    for counter in range(n_channels)]

    # plot
    plt.figure("Interactive Plot", figsize=(20,10))
    plt.title("Interactive Plot of Channels, click on Datapoints for Info")

    # for assigning different colors to different clusters
    nr_to_color = ["b", "g", "r", "c", "y", "m", "k", "fuchsia",        \
                    "gray", "navy", "coral"]

    # plot every datapoint with its corresponding text ("label")
    # dont iterative, to assign labels correctly
    for dp in range(n_channels):
        plt.scatter(data2d[dp,0], data2d[dp,1], linewidths=0.1,         \
        c=nr_to_color[labels[dp]], label=text_list[dp])

    # add datacursor, basically enabling "clickability" of datapoints
    datacursor(formatter='{label}'.format, bbox=dict(fc='white'),       \
                 arrowprops=dict(arrowstyle='simple', fc='black', alpha=0.5))

    plt.show()
    return 0

def create_label_for_matplotlib(series_of_dp):
    label = PrettyTable(["Attribute", "Value"])
    exclude = ["Conc_Trace", "Temperature"]
    for attribute in series_of_dp.keys():
        if (attribute not in exclude):
            label.add_row([attribute, series_of_dp[attribute]])


    return str(label)

if (__name__=="__main__"):

    # number of dimensions the data was reduced too in the paper
    # corresponding to the ion
    ion_dim = {"K":16, "Na":21, "Ca":29, "IH":16, "KCa":16}

    # Get traces
    file_name = "Na_family_dataframe.pickle"
    """
    with open(file_name, 'r') as f:
        channel_dict = json.load(f)
    """

    main_df = pd.read_pickle(file_name)
    pp_channel_dict = dim_reduction(main_df)
