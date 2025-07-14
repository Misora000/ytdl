# ytdl: A lazy youtube-dl launcher

Feature
- Auto select the highest resolution (up to 4k 2160p 60fps)
- Auto retry for network error and customize retry num by attribe `-c`
- Specify saving path by attribute `-o`
- Auto rename when collision by attribute `-s`
- Auto use cookie from `www.youtube.com_cookies.txt` (by [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc))
- Optional to save video as generic name `youtube video #XXXXXXXXXXX`.mkv by attribe `-g`
- Batch mode & file mode (similar to `yt-dlp -a`)
- Summarize list of download failed & qulity downgraded videos

## Requirement
Make sure you have the following executable in your `PATH`
- [ffmpeg](https://www.ffmpeg.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp/releases)


## Usage
```sh
usage: main.py [-h] [-c C] [-o O] [-f] [-s] [-g] urls

positional arguments:
  urls        Target url(s)

options:
  -h, --help  show this help message and exit
  -c C        Retry count (default=1)
  -o O        Output path
  -f          File containing URLs to download
  -s          Rename video if exists the same name
  -g          Save video as the generic name
```

Example
```sh
# download an url
python main.py 'https://www.youtube.com/watch?v=0123456789A'

# download multiple urls (separate by comma)
python main.py 'https://www.youtube.com/watch?v=0123456789A,https://www.youtube.com/watch?v=0123456789B'

# download multiple urls from file (one line one url)
python main.py -f 'url_list.txt'

# auto rename video when collision
python main.py -s 'https://www.youtube.com/watch?v=0123456789A'

# download to a specific folder
python main.py -o 'download' 'https://www.youtube.com/watch?v=0123456789A'
```

You can pre-define default download folder in `default_dl_path.txt`