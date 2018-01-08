import requests
import json
import matplotlib.pyplot as plt

def trace_getter(gate_id=2706):
    """
    Returns all 5 traces of a gate id (corresponding to a gate on
    https://icg.neurotheory.ox.ac.uk) in a dictionary.

    Args:
        gate_id (int):  id of the gate on icg

    Outputs:
        trace_dict (dict): dictionary with 5 traces: Action Potential,
                            Inactivation, Activation, Ramp, Deactivation
    """
    # all 5 available trace names
    trace_dict = {'Action Potential':[], 'Inactivation':[], 'Activation':[], \
                'Ramp':[], 'Deactivation':[]}

    # get response
    url = "https://icg.neurotheory.ox.ac.uk:443/api/app/chs/" + \
            str(gate_id) + "/traces"
    response = requests.get(url)

    # check for right response status
    if (response.status_code != 200):
        raise ValueError("Response Status from API is not 200, but instead {}!".\
        format(response.status_code))

    # from byte to json object to pure data lists
    my_json = response.content.decode("utf8")
    data = json.loads(my_json)
    traces = data["traces"][0]["traces"] # get traces
    # TODO not only action potential
    for dict_key in trace_dict.keys():
        trace_dict[dict_key] = traces[dict_key]["data"][0]

    return trace_dict

def trace_plotter_complete(trace_dict, trace_id=-1):
    """
    Plots all 5 traces of a gate id (corresponding to a gate on
    https://icg.neurotheory.ox.ac.uk) in a dictionary.

    Args:
        trace_dict (dict):  dictionary with all traces of a gate
        gate_id (int):      id of the gate on icg
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


gate_trace_dict = trace_getter()
trace_plotter_complete(data1, 1504)
