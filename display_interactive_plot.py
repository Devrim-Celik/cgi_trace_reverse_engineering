import matplotlib.pyplot as plt
import pandas as pd
import operator
from mpldatacursor import datacursor
from bokeh.plotting import figure, output_file, show

def interactive_plot_plt(file_name):
    """
    Defintion:
        Function which plots all datapoints of a beforehand finished channel
        selection.
        Additionally, the plot is interactive in that regard, that you will be
        able click on the datapoints in the resulting plot for more information
    """

    # get plot values from beforehand created pickle
    df = pd.read_pickle(file_name)

    # plot
    fig = plt.figure("Interactive Plot", figsize=(20,10))
    plt.title("Interactive Plot of Channels, click on Datapoints for Info")

    # plot with all available information of the pickle file
    for dp in range(len(df)):
        plt.scatter(df['Value1'][dp], df['Value2'][dp], linewidths=0.1,         \
        c=df['Color'][dp], label=df['Label'][dp])

    # add datacursor, basically enabling "clickability" of datapoints
    datacursor(formatter='{label}'.format, bbox=dict(fc='white'),       \
                 arrowprops=dict(arrowstyle='simple', fc='black', alpha=0.5))

    plt.show()



def mscatter_basic(p, x, y):
    """
    Definition:
        Takes a bekoh plot object and 2 values (coordinates) and plots black
        circles at the according position on the plot object
    """
    p.scatter(x, y, marker='circle', size=7,
            line_color="black", fill_color="black")



def mscatter(p, x, y, allowed, value_list):
    """
    Definition:
        Takes a bekoh plot object and 2 values (coordinates), a dictionary of
        allowed values, and a value list.
        It first checks which values the datapoint (x,y) has and whether they
        are in the dictionary of allowed values.
        In case they are, a red circle is plotted.
    """
    for value in value_list:
        if value in allowed.keys():
            p.scatter(x, y, marker='circle', size=6.5,
                    line_color="red", fill_color="red", legend=allowed[value])




def interactive_plot_bokeh(file_name, meta_name, attribute="Animal_Model"):
    """
    Defintion:
        Creates a Bokeh plot in which it first plots a black dot for every
        channel. Furthermore, depending on the attribute we are looking at,
        we will see which are the 30 most common values for this particular
        attribute, and each datapoint (black ones) which has one of those
        values, will be covered by a red one, which a hideable.

        Note:   possible values for attribute argument:
            'Animal_Model'
            'Brain_Area'
            'Neuron_Region'
            'Neuron_Type'
            'Runtime_Q'
            'Subtype'
            'Age',
            'Author'
            'Temperature'
    """

    #get plot values
    df = pd.read_pickle(file_name)
    #get metadata
    df_m = pd.read_pickle(meta_name)


    # because I can only visualize 30 values in the legend, find the the top 30
    # values of an attribute
    counting_dict = {}
    legend_allowed = {}

    for i in range(len(df)):
        value_list = df_m[attribute][i]
        for value in value_list:
            # if a value is not yet in our dictionary, add it with amount 1
            if value not in counting_dict.keys():
                counting_dict[value] = 1
            else:
                counting_dict[value] += 1

    # sort them from small to large as tuples!
    sorted_list = sorted(counting_dict.items(), key=operator.itemgetter(1))

    # in case less than 30 unique values
    try:
        go_over = sorted_list[-30:]
    else:
        go_over = sorted_list

    # go over all of the 30 most common tuple pairs
    for tuple_val in go_over:
        # create a dictionary of form value:str(value (amount))
        legend_allowed[tuple_val[0]] = tuple_val[0] + " (" + \
            str(tuple_val[1]) + ")"


    # create bokeh plot
    p = figure(plot_width=1200, plot_height=800)
    p.title.text = 'Click on legend entries to mute the corresponding points'

    # create one black circle. create one red circle for every point, for
    # every value of the chosen attributes
    for i in range(len(df)):
        print(i)
        mscatter_basic(p, df['Value1'][i], df['Value2'][i])
        mscatter(p, df['Value1'][i], df['Value2'][i],
            legend_allowed, df_m[attribute][i])


    # define legend and action when click on a legend value
    p.legend.location = "top_left"
    p.legend.click_policy="hide"


    # save in interactive html
    output_file("cgi_channels_interactive_" + attribute + ".html",
        title="CGI Channels")

    # open html in browser
    show(p)



if (__name__=='__main__'):
    file_name = "Interactive_Plot_Values.pickle"
    meta_name = "Na_family_dataframe.pickle"

    #interactive_plot_plt(file_name)
    interactive_plot_bokeh(file_name, meta_name)
