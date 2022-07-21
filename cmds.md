# trim video
```sh
ffmpeg.exe -i rt.mp4 -ss 00:16:22.3 -t 00:00:06 -async 1  r2.mp4
```

# merge videos
```sh
ffmpeg.exe -f concat -safe 0 -i merge.txt -c copy runa3_repeat.mp4
```

merge.txt
```
file 'r2.mp4'
file 'r2.mp4'
file 'r2.mp4'
file 'r2.mp4'
file 'r2.mp4'
file 'r2.mp4'
file 'r2.mp4'
file 'r2.mp4'
file 'r2.mp4'
file 'r2.mp4'
```
