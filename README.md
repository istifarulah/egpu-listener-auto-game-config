
# eGPU Listener and Auto Game Config Changer
This project is to solve my problem while using Lenovo Legion Go with an eGPU, if I'm using eGPU I tends to maximize resolution at 3440X1440 and having High / Ultra setting on game, but occasionally I want to play on handheld mode, changing game resolution and graphics options everytime I play in different settings (using eGPU or handheld mode) is too tedious. This script solve the issue by copying different game setting file by detecting whether eGPU is connected or not.

The basic idea is from this project https://github.com/diego351/handheld-config/tree/master but it only support Nvidia Graphics Card, while I'm using AMD Graphics Card, so I re-create the project using a portion of code from that project to be used here, changing from GPUtil to WMI to detect eGPU, it should support all Graphics Card whether Nvidia, AMD or Intel, and I add functionality so this script could running in background as Windows Service.

In the latest update, I'm adding a feature if whether iGPU or eGPU is connected, this script could also auto launch an application, this is useful because in my experience after I plugin the eGPU or unplug it, the AMD Software Adrenaline would unexpectedly closed or crashing, whereas I need the OSD performance metrics from AMD Software to measure eGPU performance.

# Requirements
- eGPU is running well and graphics drivers are installed
- NSSM (Non-Sucking Service Manager) downloaded
- Python3 Installed

# Installation
- Download this project to C:/egpu-listener-auto-game-config
- Change EGPU_NAME to yours at config.py, you could get your eGPU name from Device Manager -> Display adapters
- Change GAME_PROFILES according to your needs
```
d_config_path = game config file that would copied to destination while using eGPU.
i_config_path = game config file that would copied to destination while using iGPU.
destination = location where the game config file that will be overwritten.
```
- Change APP_AUTO_LAUNCH to `True` if you want auto launch app feature, or `False` if you don't want auto launch app feature
- Change APP_PATH to your desired application path that needs to be opened after iGPU or eGPU is connected
- Open Terminal, Run as administrator
- `pip install -r requirements.txt`
- Go to your NSSM directory or just copy nssm.exe to this project directory at C:/egpu-listener-auto-game-config
- Look for your python3 executable path, and run the command below
- `.\nssm.exe install EGPUListener "C:\Program Files\Python\python.exe" "C:\egpu-listener-auto-game-config\listener.py"`
- `.\nssm.exe start EGPUListener`
- Service "EGPUListener" installed successfully! and will automatically started after reboot
- If service is successfully installed and running, log file would be created at C:/egpu_listener.log

# Usage
- Start Service
```
.\nssm.exe start EGPUListener
```
- Stop Service
```
.\nssm.exe stop EGPUListener
```
- Remove Service
```
.\nssm.exe remove EGPUListener
```
