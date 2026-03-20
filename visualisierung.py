import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    from pathlib import Path
    from PIL import Image
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    import matplotlib as mlp
    import matplotlib.pyplot as plt
    from dtaidistance import dtw
    from dtaidistance import dtw_visualisation as dtwvis
    import random
    from scipy import stats
    from tslearn.barycenters import dtw_barycenter_averaging

    return Image, dtw, dtw_barycenter_averaging, np, pd, plt


@app.cell
def _(beispiel, plt):
    fig3, ax = plt.subplots()
    ax.plot(list(range(len(beispiel['values']))), beispiel['values'])
    #plt.savefig('rgb.png')
    plt.show()
    return


@app.cell
def _(np):
    loaddata = np.load("rgb.npz", allow_pickle=True)
    #print(loaddata.files)
    data = loaddata["data"]
    print(data['videoname'])
    print(data['values'][0])
    return (data,)


@app.cell
def _(datadtw):
    filtered_values = [values for name, values in datadtw if "Jan & Henry" in name]
    print(filtered_values)
    return (filtered_values,)


@app.cell
def _(dtw_barycenter_averaging, filtered_values):
    dba_curve = dtw_barycenter_averaging(filtered_values)
    return (dba_curve,)


@app.cell
def _(dba_curve):
    print (dba_curve.shape)
    return


@app.cell
def _(Image, dba_curve, np):
    def display_colors(non_linear_arr):
        y = np.array([non_linear_arr]).astype(np.uint8)
        return Image.fromarray(y).resize((len(non_linear_arr) * 64, 5000), resample=Image.Resampling.NEAREST)

    display_colors(dba_curve)
    return


@app.cell
def _(dba_curve, plt):
    fig3, ax = plt.subplots()
    ax.plot(list(range(len(dba_curve))), dba_curve)
    #plt.savefig('rgb.png')
    #plt.show()
    return


@app.cell
def _(data, np):
    videoinfo = np.array([], dtype=[('videoname', 'U100'), ('timeinsek', 'double')])
    for video in data:
        name = video[0]
        time = (len(video[1])/3)/60
        new_row = np.array((name, time), dtype=videoinfo.dtype)
        videoinfo = np.append(videoinfo,new_row)

    print (videoinfo)
    return


@app.cell
def _(data, plt):
    fig, axs = plt.subplots((len(data['values'])-1))
    fig.suptitle('Vertically stacked subplots')
    for d in list(range(len(data['values'])-1)):
        lenfra = len(data['values'][d])
        x = list(range(lenfra))
        y = data['values'][d]
        axs[d].plot(x, y)

    plt.show()
    return


@app.cell
def _(data, np):
    datadtw = data
    for v in range(len(datadtw['values'])):
        indizes = np.linspace(0, len(datadtw['values'][v])-1, num=1000).astype(int)
        newvalues = np.zeros(1000)
        for i in range(1000):
            index = indizes[i]
            newvalues[i] = datadtw['values'][v][index]
            #newvalues = stats.zscore(newvalues)#normalization of values
        datadtw['values'][v] = newvalues
    return (datadtw,)


@app.cell
def _(datadtw):
    print(datadtw)
    return


@app.cell
def _(data, datadtw, plt):
    fig2, axs2 = plt.subplots(3)#((len(datadtw['values'])-1))
    fig2.suptitle('Vertically stacked subplots')
    for d2 in range(3):#list(range(len(datadtw['values'])-1)):
        lenfra2 = len(datadtw['values'][d2])
        x2 = list(range(lenfra2))
        y2 = data['values'][d2]
        axs2[d2].plot(x2, y2)

    plt.show()
    return


@app.cell
def _(datadtw):
    print(len(datadtw['values'][0]))
    return


@app.cell
def _(datadtw, dtw):
    ds = dtw.distance_matrix(datadtw['values'])
    return (ds,)


@app.cell
def _(ds, plt):
    leinwand, diagramm = plt.subplots()
    diagramm.imshow(ds)
    #plt.savefig('distance_matrix_rgb.png')
    return


@app.cell
def _():
    #np.savez("distance_matrix_rgb.npz", data=ds)
    return


@app.cell
def _(datadtw, ds, pd):
    df = pd.DataFrame(ds, columns=datadtw['videoname'], index=datadtw['videoname'])
    df = df.replace(0, None)
    return (df,)


@app.cell
def _(df):
    df.min()
    return


@app.cell
def _(df):
    print(df)
    return


if __name__ == "__main__":
    app.run()
