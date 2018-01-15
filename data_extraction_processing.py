import requests
import json
import matplotlib.pyplot as plt
import pprint
import pandas as pd

def channel_id_getter(family_id=2):
    # TODO check if 4/IH = Hyperpolarization-activated Channel
    """
    Given a family id (with 1=Potassium Channel, 2=Sodium Channel,
    3=Calcium Channel, 4:Hyperpolarization-activated Channel,
    5:Calcium-dependent Potassium Channel) returns a list with all
    corresponding channel ids from icg

    Args:
        family_id (int): family id

    Outputs:
        id_list (list): list with all ids corresponding to the given family_id
    """

    id_list = []

    # get response
    url = "https://icg.neurotheory.ox.ac.uk:443/api/app/families/" + \
            str(family_id) + "/"
    response = requests.get(url)

    # check for right response status
    if (response.status_code != 200):
        raise ValueError("[!] Response Status from API is not 200, \
        but instead {}!".format(response.status_code))

    # from byte to json object to pure id lists
    my_json = response.content.decode("utf8")
    data = json.loads(my_json)


    for counter in range(data["count"]):
        id_list.append(data["chans"][counter]["id"])

    return id_list



def trace_getter(channel_id=2706):
    """
    Returns all 5 traces of a channel id (corresponding to a channel on
    https://icg.neurotheory.ox.ac.uk) in a dictionary.

    Args:
        channel_id (int):  id of the channel on icg

    Outputs:
        trace_dict (dict): dictionary with 5 traces: Action Potential,
                            Inactivation, Activation, Ramp, Deactivation
    """
    # all 5 available trace names
    trace_dict = {'Action Potential':[], 'Inactivation':[], 'Activation':[], \
                'Ramp':[], 'Deactivation':[]}
    trace_list = []

    # get response
    url_trace = "https://icg.neurotheory.ox.ac.uk:443/api/app/chs/" + \
            str(channel_id) + "/traces"
    response = requests.get(url_trace)

    # check for right response status
    if (response.status_code != 200):
        raise ValueError("[!] Response Status from API is not 200, \
        but instead {}!".format(response.status_code))

    # from byte to json object to pure data lists
    my_json = response.content.decode("utf8")
    data = json.loads(my_json)
    traces = data["traces"][0]["traces"] # get traces

    """
    # iterate through every trace --> produces dict with 5 keys
    for dict_key in trace_dict.keys():
        trace_dict[dict_key] = traces[dict_key]["data"][0]
    """

    # iterate through every channel and append them to one big list
    # TODO done differently in the paper, depending on whether
    # it was a Ca channel
    for dict_key in trace_dict.keys():
        trace_list.extend(traces[dict_key]["data"][0])

    return trace_list



def metadata_getter(channel_id=2706):
    """
    Returns metadata of a channel id (corresponding to a channel on
    https://icg.neurotheory.ox.ac.uk) in a dictionary.

    Args:
        channel_id (int):  id of the channel on icg

    Outputs:
        TODO
    """

    # specify all category names you want to include in meta data
    index_list = {'Animal Model':0, 'Brain Area':1, 'Neuron Region':2, \
                 'Neuron Type':3, 'Runtime Q':4, 'Subtype':5,  'Age':6, \
                 'Authors':7, 'Temperature':8}
    # specify an list for the actual attributes
    # Note: index of the dictionary above will be used to reference elements
    # of this list
    attr_list = [[]]*len(index_list.keys())

    # get response
    url_meta = "https://icg.neurotheory.ox.ac.uk:443/api/app/chs/" + \
            str(channel_id)
    response = requests.get(url_meta)

    # check for right response status
    if (response.status_code != 200):
        raise ValueError("[!] Response Status from API is not 200, \
        but instead {}!".format(response.status_code))

    # from byte to json object to pure data lists
    my_json = response.content.decode("utf8")
    # data is a list of dictionaries, each with different properties
    data_cls = json.loads(my_json)['cls']
    data_meta = json.loads(my_json)['metadata']

    # for visualization of the json object
    #pprint.pprint(data)

    # go through all the attribute dictionaries of cls data
    for attribute_dic in data_cls:
        # if we are intrested in the category
        if (attribute_dic['name'] in index_list.keys()):
            # add, at the corresponding position on our attr_list, all the
            # 'name' values of all dictionaries in the 'cls' attribute
            attr_list[index_list[attribute_dic['name']]] = \
                [thing['name'] for thing in attribute_dic['cls']]

    # do the same for metadata informations
    for attribute_dic in data_meta:
        # if we are intrested in the category
        if (attribute_dic['name'] in index_list.keys()):
            # add, at the corresponding position on our attr_list, all the
            # 'name' values of all dictionaries in the 'cls' attribute
            attr_list[index_list[attribute_dic['name']]] = \
                [attribute_dic['value']]

    return attr_list




def trace_plotter_complete(trace_dict, trace_id=-1):
    """
    Plots all 5 traces of a channel id (corresponding to a channel on
    https://icg.neurotheory.ox.ac.uk) in a dictionary.

    Args:
        trace_dict (dict):  dictionary with all traces of a channel
        channel_id (int):      id of the channel on icg
    """

    trace_names = ['Activation', 'Inactivation', 'Deactivation',  \
                'Action Potential', 'Ramp']

    # add id in window title if possible
    plot_name = "5 Traces"
    if (trace_id != -1):
        plot_name += " of channel with id = {}".format(trace_id)

    # build plot
    plt.figure(plot_name, figsize=(20,10))
    plt.title(plot_name)
    for counter, trace_key in enumerate(trace_names):
        plt.subplot(2, 3, counter+1)
        plt.title(trace_key)
        plt.plot(trace_dict[trace_key])

    plt.show()



def dump_family_as_json_with_trace(family_id=2):
    # TODO check if 4/IH = Hyperpolarization-activated Channel
    """
    Given a family id (with 1=Potassium Channel, 2=Sodium Channel,
    3=Calcium Channel, 4:Hyperpolarization-activated Channel,
    5:Calcium-dependent Potassium Channel) it dumps a big dictionary in a
    json file, which contains all 5 traces of each channel, corresponding
    to the family

    Args:
        family_id (int): family id
    """

    family_id_to_name = {1:"K", 2:"Na", 3:"Ca", 4:"IH", 5:"KCa"}
    big_dict = {}

    # create pandas dataframe
    channel_df = pd.DataFrame()

    # get all ids of corresponding channels
    id_list = channel_id_getter(family_id)
    # add ids to the dataframe and its family
    channel_df['ID'] = id_list
    channel_df['Family'] = [family_id_to_name[family_id] for i in range(len(id_list))]


    # go through every id and get its metadata, and create a new dataframe with
    # those informations
    meta_df = pd.DataFrame(columns=['Animal_Model', 'Brain_Area',              \
                'Neuron_Region', 'Neuron_Type', 'Runtime_Q', 'Subtype', 'Age', \
                'Author', 'Temperature'])

    for counter, _id in enumerate(id_list):
        if (counter % 100 == 0):
            print(counter, "of", len(id_list))
        meta_df.loc[len(meta_df)] = metadata_getter(_id)



    # go through every id and get it trace, save it in a dataframe
    for counter, _id in enumerate(id_list):
        # What basically is done here:
        #   For every id, localise the entry where the id is in the column
        #   "ID" and set its attribute "Conc_Trace" to the extracted voltage
        #   trace (hacked)
        if (counter % 100 == 0):
            print(counter, "of", len(id_list))
        channel_df.loc[channel_df['ID']==_id, 'Conc_Trace'] =            \
            pd.Series([trace_getter(_id)],                               \
            index = [channel_df.loc[channel_df['ID']==_id].index[0]])

    final_df = pd.concat([channel_df, meta_df], axis=1)

    print(final_df)
    print(len(final_df['Conc_Trace'][0]))
    # create file name
    """
    file_name = family_id_to_name[family_id] + "_family.json"
    # dump finished dictionary in json file
    with open(file_name, 'w') as fp:
        json.dump(big_dict, fp)
    """
    file_name = family_id_to_name[family_id] + "_family_dataframe.pickle"
    final_df.to_pickle(file_name)
    # NOTE: To read data use: .kpd.read_pickle(file_name)

    print("[+] Saved " + family_id_to_name[family_id] + \
            " Family Trace in:", file_name)



if __name__=="__main__":
    dump_family_as_json_with_trace(2)
