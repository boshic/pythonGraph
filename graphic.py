import os, fnmatch
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

graph_params = {
    "min_trsh_val" : 0.5,
    "min_trsh_color" : 'r',
    "clnt_detected_color" : 'g',
    "clnt_detected_val" : 1,
    "size_multyplier" : 1000,
    "depth_corrector_in_kb": 145
}

def is_it_needed_file(entry, pattern):
    return True if (entry.is_file() and fnmatch.fnmatch(entry.name, pattern)) else False


def draw_graph(names, rng):
    fig, ax = plt.subplots(figsize=(19, 10))
    ax.stackplot(names, rng, labels=[graph_params["depth_corrector_in_kb"]])
    ax.legend(loc='upper left')
    plt.axhline(y = graph_params["clnt_detected_val"],
                color = graph_params["clnt_detected_color"],
                linestyle = '--')
    # plt.axhline(y = graph_params["min_trsh_val"],
    #             color=graph_params["min_trsh_color"],
    #             linestyle='--')
    plt.xticks(rotation=90)
    fig.tight_layout()
    plt.savefig(datetime.now().strftime("graphic_for_%m_%d_%Y"))
    # plt.show()

def calc_file_size(size):
    calculated_size = (size/graph_params["size_multyplier"] - graph_params["depth_corrector_in_kb"])/10
    return calculated_size if calculated_size > 0 else 0

def main():
    rng = []
    names = []
    path = os.getcwd()
    pattern = "*.jpg"
    list_of_entries = sorted(os.scandir(path), key=lambda d: d.stat().st_mtime)

    for entry in list_of_entries:
        if is_it_needed_file(entry, pattern):
            names.append(entry.name[15:20])
            rng = np.append(rng, os.stat(entry.name).st_size)

    # print(rng)
    # print(names)
    avrg = np.mean(rng)/graph_params["size_multyplier"]
    graph_params["depth_corrector_in_kb"] = round((avrg - avrg/30), 0)
    rng = list(map(lambda sz: calc_file_size(sz), rng))
    draw_graph(names, rng)

main()