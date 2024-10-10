import os, sys
import subprocess

bin_youtubedl = 'yt-dlp.exe'
dst = 'E:/動畫/YoutubeDL'

class ytdl():
    url = ''

    def __init__(self, url):
        self.url = url

    def get_format(self):
        allFmt = []
        cmd = [bin_youtubedl, '-F', self.url]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)

        for l in result.stdout.decode('ascii').split('\n'):
            if l.find('mp4') > 0:
                allFmt.append(l.split(' ')[0])
            if l.find('webm') > 0:
                allFmt.append(l.split(' ')[0])

        # prefer video format:
        #   315: 2160p, 60fps
        #   313: 2160p, 30fps
        #   308: 1440p, 60fps
        #   271: 1440p, 30fps
        #   299: 1080p, 60fps
        #   137: 1080p, 30fps
        for v in ['315', '313', '308', '271', '299', '137']:
            if v in allFmt:
                return v
        
        return ''

    def download(self, vfmt):
        if vfmt == '':
            cmd = '{} {} -o {}/%(title)s.mkv'.format(bin_youtubedl, self.url, dst)
        else:
            cmd = '{} -f {}+bestaudio --merge-output-format mkv {} -o {}/%(title)s.mkv'.format(bin_youtubedl, vfmt, self.url, dst)
        return os.system(cmd)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('insufficient parameters')
        exit

    urls = sys.argv[1]
    for url in urls.split(','):
        d = ytdl(url)
        bestVideo = d.get_format()
        print('select vidoe format: {}'.format(bestVideo))
        
        while True:
            status = d.download(bestVideo)
            if status == 0:
                break
