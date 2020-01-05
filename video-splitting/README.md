

## Cut with ffmpeg

```
ffmpeg -i input.mp4 -filter_complex "[0:a]silencedetect=n=-30dB:d=5.0[outa]" -map [outa] -f s16le -y /dev/null |& F='-aq 70 -v warning' perl -ne 'INIT { $ss=0; $se=0; } if (/silence_start: (\S+)/) { $ss=$1; $ctr+=1; printf "ffmpeg -nostdin -i input.mp4 -ss %f -t %f $ENV{F} -y %03d.mp4\n", $se, ($ss-$se), $ctr; } if (/silence_end: (\S+)/) { $se=$1; } END { printf "ffmpeg -nostdin -i input.mp4 -ss %f $ENV{F} -y %03d.mp4\n", $se, $ctr+1; }' | bash -x
```
