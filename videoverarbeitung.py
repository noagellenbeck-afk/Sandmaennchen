import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from video2images import Video2Images
    import os
    from pathlib import Path


    return Path, Video2Images, os


@app.cell
def _(Path):
    PATH = Path("/Users/noagellenbeck/Desktop/sandmann/data")
    return (PATH,)


@app.cell
def _(PATH, vtof):
    for x in PATH.iterdir():
        if (x.suffix == ".mp4"):
            vtof(x)
    return


@app.cell
def _(PATH, Video2Images, os):
    def vtof (path):
        path = str(PATH / path.stem)
        if not (os.path.exists(path)):
            os.makedirs(path)
            videopath = f"{path}.mp4"
            print(videopath)
            outputpath = path
            print(path)
            Video2Images(video_filepath=f"{path}.mp4", save_format=".jpeg", capture_rate=3, out_dir=path)

    return (vtof,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
