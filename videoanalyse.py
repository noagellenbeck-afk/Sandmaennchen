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

    return Image, KMeans, Path, np


@app.cell
def _(Path):
    PATH = Path("/Users/noagellenbeck/Desktop/sandmann/data")
    path = Path("/Users/noagellenbeck/Desktop/sandmann/beispielvideo")
    return PATH, path


@app.cell
def _(data, path, videocenters):
    videocenters(path)
    beispiel = data
    return (beispiel,)


@app.cell
def _(beispiel):
    print(beispiel)
    return


@app.cell
def _(beispiel, np):
    np.savez("beispielvideo.npz", data=beispiel)
    return


@app.cell
def _(KMeans):
    kmeans = KMeans(
        n_clusters=1,
        random_state=0)
    return (kmeans,)


@app.cell
def _(Image, kmeans, np):
    def farbcenter(path):
        img = Image.open(path)
        w, h = img.size
        img = np.array(img.resize((512, int(360 * (512 / 640))), resample=Image.Resampling.HAMMING).convert("RGB"))
        img = img.reshape(-1,3)
        #print(img)
        kmeans.fit(img)
        return(kmeans.cluster_centers_)

    return (farbcenter,)


@app.cell
def _(np):
    #loaddata = np.load("rgb.npz", allow_pickle=True)
    #print(loaddata.files)
    #data = loaddata["data"]
    #print(data['videoname'])
    #print(data['values'][1])
    data = np.array([], dtype=[('videoname', 'U100'), ('values', 'O')])
    def add_row(values):
        global data
        print("füge video hinzu")
        data = np.append(data, values)

    return add_row, data


@app.cell
def _(data):
    print(data['videoname'])
    return


@app.cell
def _(np):
    def farbunterschied(array):
        #eukl = np.empty(shape=(len(array)-1,2))
        eukl = np.delete(array, 0, axis=0).astype(np.int32) - np.delete(array, -1, axis=0).astype(np.int32) #jeder rgb-wert wird mit dem vorgängerwert substrahiert -> abstandsvektor
        eukl = np.sqrt(np.sum(np.square(eukl), axis=1)) #betrag der vektoren, für eukl.dis
        return(eukl)

    return


@app.cell
def _(np):
    def helligkeit(array):
        mean = np.mean(array, axis=1) 
        print(mean)
        return(mean)

    return


@app.cell
def _(add_row, data, farbcenter, np):

    def videocenters(path):
        global data
        for x in path.iterdir():
            if (x.is_dir()==True and x.stem not in data['videoname']):
                print(x.stem)
                for y in x.iterdir():
                    if y.is_dir()==True:
                        image_indices = [int(z.stem) for z in y.iterdir() if z.suffix == ".jpeg"]
                        image_indices.sort()
                        centers = np.zeros((len(image_indices), 3), dtype=np.uint8)
                        for i in image_indices:
                            path = y / (str(i)+".jpeg")
                            centers[i-1] = farbcenter(path)
                        #centers = farbunterschied(centers)
                        #centers = helligkeit(centers)
                        new_row = np.array((str(x.stem), centers), dtype=data.dtype)
                        add_row(new_row)

    #videocenters(PATH)  
    return (videocenters,)


@app.cell
def _(data):
    print(data['values'])
    return


@app.cell
def _():
    #np.savez("rgb.npz", data=data)
    return


@app.cell
def _(PATH, data):
    for x in PATH.iterdir():
        if (x.is_dir()==True and x.stem not in data['videoname']):
            print(x.stem)
    return


if __name__ == "__main__":
    app.run()
