import os, shutil
from dotenv import dotenv_values

class Patcher:
  def __init__(self, extract_dir):
    self.extract_dir = extract_dir

    env = dotenv_values(f'{self.extract_dir}/.env')
    self.manufacturer = env.get('MANUFACTURER')
    self.model = env.get('MODEL')
    self.rom = env.get('ROM')
    self.apk_name = env.get('APK_NAME')
    self.on_unlocked_value = None

  def is_successfully_disassembled(self):
    return os.path.exists(f'{self.extract_dir}/{self.apk_name}/smali')

  def clean(self):
    os.remove(f'{self.extract_dir}/framework-res.apk')
    os.remove(f'{self.extract_dir}/{self.apk_name}.apk')
    os.remove(f'{self.extract_dir}/{self.apk_name}_mod.apk')
    shutil.rmtree(f'{self.extract_dir}/{self.apk_name}')

  def log_stats(self):
    with open('/data/stats.csv', 'a') as fd:
      fd.write(f'{os.path.basename(self.extract_dir)},{self.manufacturer},{self.model},{self.rom},{self.apk_name},{self.on_unlocked_value}\n')

  def patch_ScreenStateHelper(self):
    path = f'{self.extract_dir}/{self.apk_name}/smali/com/android/nfc/ScreenStateHelper.smali'
    with open(path) as fd:
      lines = fd.readlines()
      for i, line in enumerate(lines):
        if 'SCREEN_STATE_ON_UNLOCKED' in line:
          self.on_unlocked_value = line.strip().split(' ')[-1]
        if 'checkScreenState' in line:
          insert_index = i + 2

      lines = lines[:insert_index] + [f'const/16 v0, {self.on_unlocked_value}\n', 'return v0\n'] + lines[insert_index:]
    
    with open(path, 'w') as fd:
      fd.writelines(lines)

  def patch_NfcService(self):
    path = f'{self.extract_dir}/{self.apk_name}/smali/com/android/nfc/NfcService.smali'
    with open(path) as fd:
      lines = fd.readlines()
      for i, line in enumerate(lines):
        line = line.replace('SCREEN_OFF', 'SCREEN_OFF_DISABLED')
        line = line.replace('SCREEN_ON', 'SCREEN_ON_DISABLED')
        line = line.replace('USER_PRESENT', 'USER_PRESENT_DISABLED')
        line = line.replace('USER_SWITCHED', 'USER_SWITCHED_DISABLED')
        lines[i] = line
    
    with open(path, 'w') as fd:
      fd.writelines(lines)

