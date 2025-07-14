import os, sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('urls', help='Target url(s)')
parser.add_argument('-c', help='Retry count (default=1)', type=int, default=1)
parser.add_argument('-o', help='Output path', type=str, default='')
parser.add_argument('-f', help='File containing URLs to download', default=False, action='store_true')
parser.add_argument('-s', help='Rename video if exists the same name', default=False, action='store_true')
parser.add_argument('-g', help='Save video as the generic name', default=False, action='store_true')

bin_youtubedl = 'yt-dlp.exe'

class ytdl():
    url = ''

    def __init__(self, url, dst):
        self.url = url
        self.dst = dst
        self.append_id = False
        self.generic_name = False

        self.cookie = ''
        if os.path.exists('www.youtube.com_cookies.txt'):
             self.cookie = ' --cookies www.youtube.com_cookies.txt'

    def append_id_to_video_name(self, val: bool):
        self.append_id = val

    def save_generic_name(self, val: bool):
        self.generic_name = val

    def get_video_title(self) -> str:
        cmd = f'{bin_youtubedl}{self.cookie} --get-title {self.url}'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.stdout.replace('\n', '')
        
    def get_formats(self) -> list[str]:
        allFmt = []
        cmd = f'{bin_youtubedl}{self.cookie} -F {self.url}'
        result = subprocess.run(cmd, stdout=subprocess.PIPE)

        # for l in result.stdout.decode('ascii').split('\n'):
        for l in result.stdout.decode('utf-8').split('\n'):
            if l.find('mp4') > 0:
                allFmt.append(l.split(' ')[0])
            if l.find('webm') > 0:
                allFmt.append(l.split(' ')[0])

        preferFmts = [
            '628', '315', # 2160p, 60fps
            '625', '313', # 2160p, 30fps
            '623', '308', # 1440p, 60fps
            '620', '271', # 1440p, 30fps
            '617', '299', # 1080p, 60fps
            '614', '137', # 1080p, 30fps
        ]

        avaliableFmts = []
        for v in preferFmts:
            if v in allFmt:
                avaliableFmts.append(v)
        
        return avaliableFmts

    def download(self, vfmt):
        attr_vfmt = f' -f {vfmt}+bestaudio --merge-output-format mkv'
        if vfmt == '':
            attr_vfmt = ''

        if self.generic_name:
            cmd = f'{bin_youtubedl}{self.cookie}{attr_vfmt} {self.url} -o "{self.dst}/youtube video #%(id)s.mkv"'
        elif self.append_id:
            cmd = f'{bin_youtubedl}{self.cookie}{attr_vfmt} {self.url} -o "{self.dst}/%(title)s [%(id)s].mkv"'
        else:
            cmd = f'{bin_youtubedl}{self.cookie}{attr_vfmt} {self.url} -o "{self.dst}/%(title)s.mkv"'
        return os.system(cmd)
    
    def autoRetryDownload(self, vfmt, count) -> bool:
        for i in range(count):
            if self.download(vfmt) == 0:
                return True
        return False


def is_url(text) -> bool:
    return len(text) > 0

if __name__ == '__main__':
    args = parser.parse_args()

    urls = []
    if args.f:
        with open(args.urls, 'r') as f:
            urls = f.read().split('\n')
    else:
        urls = args.urls.split(',')

    # parse downlaod destination
    if len(args.o) == 0:
        if os.path.exists('default_dl_path.txt'):
            with open('default_dl_path.txt') as fr:
                args.o = fr.readline().replace('\n', '')
        else:
            args.o = 'dl'
    
    if not os.path.exists(args.o):
        os.mkdir(args.o)


    dlFailed = []
    downgrade = []

    for url in urls:
        if not is_url(url):
            continue

        dlFailed.append(url)

        d = ytdl(url, args.o)
        vfmts = d.get_formats()

        if args.g:
            d.save_generic_name(True)

        # check existence
        if args.s:
            title = d.get_video_title()
            if os.path.exists(os.path.join(args.o, title+'.mkv')):
                d.append_id_to_video_name(True)

        for i in range(len(vfmts)):
            print(f'select vidoe format: {vfmts[i]}')

            if d.autoRetryDownload(vfmts[i], args.c+1):
                # download successfull
                dlFailed.pop()
                if i > 0:
                    downgrade.append(f'{url}\t{vfmts[0]} -> {vfmts[i]}')
                break

    if len(downgrade) > 0:
        print('\n---- downgrade videos ----')
        for v in downgrade:
            print(v)

    if len(dlFailed) > 0:
        print('\n---- download failed ----')
        for v in dlFailed:
            print(v)
