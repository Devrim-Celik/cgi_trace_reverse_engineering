import requests
import json
import matplotlib.pyplot as plt

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
    url = "https://icg.neurotheory.ox.ac.uk:443/api/app/chs/" + \
            str(channel_id) + "/traces"
    response = requests.get(url)

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

    # get all ids of corresponding channels
    id_list = channel_id_getter(family_id)
    # go through every id and get it trace, save it in a dictionary
    for _id in id_list:
        #trace_plotter_complete(trace_getter(_id))
        big_dict[_id] = trace_getter(_id)

    # create file name
    file_name = family_id_to_name[family_id] + "_family.json"
    # dump finished dictionary in json file
    with open(file_name, 'w') as fp:
        json.dump(big_dict, fp)

    print("[+] Saved " + family_id_to_name[family_id] + \
            " Family Trace in:", file_name)



if __name__=="__main__":
    dump_family_as_json_with_trace(2)
