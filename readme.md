

* easy map simulator
* memory dumper
* 010ed: learn templates


export STEAM_COMPAT_DATA_PATH=/home/kpi/games/SteamLibrary/steamapps/compatdata/230410
export STEAM_COMPAT_CLIENT_INSTALL_PATH=/home/kpi/.local/share/Steam
python3 /home/kpi/.local/share/Steam/compatibilitytools.d/GE-Proton7-29/proton run /home/kpi/games/SteamLibrary/steamapps/compatdata/230410/pfx/drive_c/Program\ Files/Cheat\ Engine\ 7.4/cheatengine-x86_64.exe 

python3 /home/kpi/.local/share/Steam/compatibilitytools.d/GE-Proton7-29/proton run


spawn: 9.499986649
down: 1.000005841
ramp: 4.5


gdb --batch --pid $(pgrep -f Warframe.x) -ex "handle SIGUSR1 SIGUSR2 nostop ; awatch 0x50997D50"
