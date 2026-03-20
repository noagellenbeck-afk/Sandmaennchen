import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import yt_dlp
    import os

    return os, yt_dlp


@app.cell
def _(download_yt_video, os, yt_dlp):


    def get_playlist_info(url):
        ydl_opts = {
            'quiet': True,              # Keine Konsolenausgabe von yt-dlp
            'extract_flat': True,       # Nur Metadaten laden, nicht die Videos selbst
            'force_generic_extractor': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extrahiert Informationen der Playlist
            info = ydl.extract_info(url, download=False)

            # Titel der Playlist
            playlist_title = info.get('title', 'Unbekannt')
            print(f"Playlist: {playlist_title}\n" + "="*30)

            # Titel der einzelnen Videos in der Playlist
            if 'entries' in info:
                for entry in info['entries']:
                    video_title = entry.get('title')
                    path = f"/Users/noagellenbeck/Desktop/videoanalyse/data{video_title}.mp4"
                    if not (os.path.exists(path)):
                        #lädt nur ganze folgen mit Datumangabe und ohne Gebärdensprache
                        if (video_title[-4:] in "2025, 2026" and "(mit Gebärdensprache)" not in video_title):
                            print(video_title)
                            video_url = entry.get('url')
                            download_yt_video(video_url)



    # Beispiel-URL einsetzen
    get_playlist_info("https://www.youtube.com/playlist?list=PLmg8abQEyLpfVP00fN5aJPU-kJfmpX5aG")
    return


@app.cell
def _(os, yt_dlp):



    #dowloadfunktion von (youtubelink)
    def download_yt_video (url, output_path= "/Users/noagellenbeck/Desktop/videoanalyse/data"):
        try:
            if not os.path.exists(output_path) :
                os.makedirs(output_path)

            ytl_opts = {
                'format': 'best',
                #'cookiesfrombrowser': ('firefox',),
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'noplaylist' : True,
                # android simulation hilft sicherheitcheck zu umgehen
                'extractor_args': {'youtube': {'player_client': ['android']}},
            }

            print(f"Downloadversuch: {url}")
            with yt_dlp.YoutubeDL(ytl_opts) as ydl:
                ydl.download([url])
            print(f"Download abgeschlossen! Video in: {output_path}")

        except yt_dlp.utils.DownloadError as de:
            print (f"Downloadfehler: {str(de)}")
            print ("\nListing available formats...")
            try:
                with yt_dlp.YoutubeDL({'listformats':True}) as ydl:
                    ydl.download([url])
            except Exception as e:
                print(f"ein Fehler ist aufgetaucht: {str(e)}")

    download_yt_video("https://www.youtube.com/watch?v=HHL1H0tneVM")
    return (download_yt_video,)


if __name__ == "__main__":
    app.run()
