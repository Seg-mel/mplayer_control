MPlayer Control
===============

###This is a cross-platform Python library for [MPlayer](http://www.mplayerhq.hu/) control.

The library was tested in Ubuntu linux and Windows.
The client-server system only works in Unix at this time.
But this feature is under development for Windows.

Mini example:
``` Python
from mplayer_control.player import Player

player = Player()
player.create_new_process()
player.loadfile("/home/user/music/sound.ogg")
print player.get_percent_pos()
print player.properties.volume
player.properties.volume = 90
player.quit()
```
and you will get the result in the terminal:
``` Python
EXECUTED VALUES COMMAND: loadfile /home/user/music/sound.ogg
EXECUTED GET COMMAND: get_percent_pos ANS_PERCENT_POSITION=1
1
EXECUTED GET PROPERTY: volume ANS_volume=100.000000
100.000000
EXECUTED SET PROPERTY: volume 90
EXECUTED SIMPLE COMMAND: quit
```
For more information look at example files 
[Linux test](https://github.com/Seg-mel/mplayer_control/blob/master/linux_test.py)
and
[Windows test](https://github.com/Seg-mel/mplayer_control/blob/master/win_test.py).
