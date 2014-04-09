MPlayer Control v1
==================

###This is a cross-platform Python 2.7 library for [MPlayer](http://www.mplayerhq.hu/) control.

The library was tested in Ubuntu Linux and Windows.
Connecting to already running mplayer process is currently not supported on Windows.
But this feature is in development for Windows.

Short example:
``` Python
from mplayer_control import Player

player = Player(debug=True)
player.create_new_process()
player.loadfile("/home/user/music/sound.ogg")
print player.get_percent_pos()
print player.properties.volume
player.properties.volume = 90
player.quit()
```
Output in the console:
``` Python
EXECUTED ARGS COMMAND: loadfile /home/user/music/sound.ogg
EXECUTED GET COMMAND: get_percent_pos ANS_PERCENT_POSITION=1
1
EXECUTED GET PROPERTY: volume ANS_volume=100.000000
100.000000
EXECUTED SET PROPERTY: volume 90
EXECUTED ARGS COMMAND: quit
```
For more information look at example file 
[example.py](https://github.com/Seg-mel/mplayer_control/blob/master/example.py) 
and [API Reference](https://github.com/Seg-mel/mplayer_control/wiki/API-Reference). 
MPlayer Control is licensed under the terms of the GPL. Please refer to the 
[LICENSE](https://github.com/Seg-mel/mplayer_control/blob/master/LICENSE) file. 
Authors of the project are listed in the 
[AUTHORS](https://github.com/Seg-mel/mplayer_control/blob/master/AUTHORS) file.