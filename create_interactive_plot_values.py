import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import pickle
from tsne import bh_sne
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from mpldatacursor import datacursor
from prettytable import PrettyTable

def collect_and_save_plot_information(main_df, reduced_dim=2, perplexity=30, \
                                        n_kmeans_clusters=10):
    """
    Definition
        Reduces Dimensionality of Voltage Traces via t-SNE. Then applies
        K-means clustering. Also creates information strings for each datapoint
        containing its metadata. Finally saves it all in a pickle, for the
        script "display_interactive_plot.py" to use.
    """


    # dataframe for saving plotting values later on
    plot_df = pd.DataFrame(columns=["Value1", "Value2", "Color", "Label"])

    # create a numpy array for voltage trace values to apply dim reduction
    # and clustering
    n_channels = len(main_df['Conc_Trace'])
    n_trace_values = len(main_df['Conc_Trace'][0])
    data_array = np.zeros((n_channels, n_trace_values))

    # copy values into numpy array from dataframe
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
    plot_df["Value1"] = data2d[:,0] # ... and save in the dataframe
    plot_df["Value2"] = data2d[:,1] # ... and save in the dataframe


    # apply kmeans and save its labels for colorization
    kmeans = KMeans(n_clusters=n_kmeans_clusters)
    kmeans.fit(data2d)
    labels = kmeans.labels_
    # for assigning different colors to different clusters
    nr_to_color = ["b", "g", "r", "c", "y", "m", "k", "fuchsia",        \
                    "gray", "navy", "coral"]
    # convert clusters to colors
    colors = [nr_to_color[cluster] for cluster in labels]
    plot_df["Color"] = colors # ... and save in the dataframe


    # create list of labels, which will be displayed when clicking
    # on a datapoint
    text_list = [create_label_for_matplotlib(main_df.loc[counter])      \
    for counter in range(n_channels)]
    plot_df["Label"] = text_list # ... and save in the dataframe

    # now that we got all we need, save in pickle
    plot_df.to_pickle("Interactive_Plot_Values.pickle")



def create_label_for_matplotlib(series_of_dp):
    """
    Definition
        Creates a nice formatted string of all the value and they keys of a
        panda series.
    """
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
    main_df = pd.read_pickle(file_name)

    collect_and_save_plot_information(main_df)
