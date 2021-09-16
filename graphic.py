import os, fnmatch
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

graphParams = {
    "minTrshVal" : 0.5,
    "minTrshColor" : 'r',
    "clntDetectedColor" : 'g',
    "clntDetectedVal" : 1,
    "sizeMultyplier" : 100000,
    "depthCorrectorKb": 145
}

def isItNeededFile(entry, pattern):
    return True if (entry.is_file() and fnmatch.fnmatch(entry.name, pattern)) else False


def drawGraph(names, rng):
    fig, ax = plt.subplots(figsize=(19, 10))
    ax.stackplot(names, rng, labels=['Katuh'])
    ax.legend(loc='upper left')
    plt.axhline(y = graphParams["clntDetectedVal"],
                color = graphParams["clntDetectedColor"],
                linestyle = '--')
    plt.axhline(y = graphParams["minTrshVal"],
                color=graphParams["minTrshColor"],
                linestyle='--')
    plt.xticks(rotation=90)
    fig.tight_layout()
    plt.savefig(datetime.now().strftime("graphic_for_%m_%d_%Y"))
    plt.show()

def calcFileSize(size):
    calculatedSize = (size/1000 - graphParams["depthCorrectorKb"])/10
    return calculatedSize if calculatedSize > 0 else 0

def main():
    rng = []
    names = []
    path = os.getcwd()
    pattern = "*.jpg"
    listOfEntries = sorted(os.scandir(path), key=lambda d: d.stat().st_mtime)
    # graphParams["depthCorrectorKb"] = np.mean(map(lambda entry: os.stat(entry.name).st_size if isItNeededFile(entry, pattern) else Next, listOfEntries)
    for entry in listOfEntries:
        if isItNeededFile(entry, pattern):
            names.append(entry.name[15:20])
            rng = np.append(rng, calcFileSize(os.stat(entry.name).st_size))

    print(rng)
    # print(names)

    drawGraph(names, rng)

main()