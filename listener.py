import time
import win32serviceutil
import win32service
import win32event
import subprocess
import wmi
import os
import shutil
import config

class EGPUListener(win32serviceutil.ServiceFramework):
    _svc_name_ = "EGPUListener"
    _svc_display_name_ = "eGPU Listener Auto Game Config"
    _svc_description_ = "eGPU Connection Listener and apply game config automatically"
    
    def __init__(self):
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.LAST_APPLIED = None

    def app_launcher(self):
        subprocess.Popen([config.APP_PATH])

    def replace_files(self, config, key):
        for config_entry in config:
            to_copy_path = config_entry[key]
            to_copy_path = os.path.abspath(os.path.join(to_copy_path, os.pardir))
            dest_path = config_entry['destination']

            shutil.copytree(to_copy_path, dest_path, dirs_exist_ok=True)

    def config_executor(self, gpu):
        if gpu == 'eGPU':
            self.replace_files(config.GAME_PROFILES, 'd_config_path')
            print('eGPU Profile Applied')
            with open("C:\\egpu_listener.log", "a") as log_file:
                log_file.write("eGPU Profile Applied\n")

        elif gpu == 'iGPU':
            self.replace_files(config.GAME_PROFILES, 'i_config_path')
            print('iGPU Profile Applied')
            with open("C:\\egpu_listener.log", "a") as log_file:
                log_file.write("iGPU Profile Applied\n")

        self.LAST_APPLIED = gpu

        if config.APP_AUTO_LAUNCH == True:
            self.app_launcher()

    def gpu_detector(self):
        c = wmi.WMI()
        for gpu in c.Win32_VideoController():
            if config.EGPU_NAME in gpu.name:
                return 'eGPU'

        return 'iGPU'
        
    def main(self):
        gpu = self.gpu_detector()
        if self.LAST_APPLIED != gpu:
            self.config_executor(gpu)

    def SvcDoRun(self):
        while self.running:
            self.main()
            time.sleep(10)

    def SvcStop(self):
        self.running = False
        win32event.SetEvent(self.stop_event)

gpus = EGPUListener()
gpus.SvcDoRun()
