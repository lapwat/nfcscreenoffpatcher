import os, shutil, subprocess
from dotenv import dotenv_values

class Patcher:
  @staticmethod
  def factory(extract_dir):
    env = dotenv_values(f'{extract_dir}/.env')

    strategy = env.get('STRATEGY')
    apk_name = env.get('APK_NAME')
    manufacturer = env.get('MANUFACTURER')
    model = env.get('MODEL')
    device = env.get('DEVICE')
    rom = env.get('ROM')

    if strategy == 'odex':
      return PatcherOdex(extract_dir, apk_name, manufacturer, model, device, rom, 'odex')

    return Patcher(extract_dir, apk_name, manufacturer, model, device, rom, 'classic')

  def __init__(self, extract_dir, apk_name, manufacturer, model, device, rom, strategy):
    self.extract_dir = extract_dir
    self.apk_name = apk_name
    self.manufacturer = manufacturer
    self.model = model
    self.device = device
    self.rom = rom
    self.strategy = strategy

    self.smali_dir = None
    self.on_unlocked_value = None

  def disassemble(self):
    subprocess.run(['./disassemble.sh', self.extract_dir, self.apk_name])
    self.smali_dir = self.get_smali_dir()

  def assemble(self):
    subprocess.run(['./assemble.sh', self.extract_dir, self.apk_name])

  def get_smali_dir(self):
    possible_folders = ['smali', 'smali_classes2']
    for folder in possible_folders:
      path = f'{self.extract_dir}/{self.apk_name}/{folder}'
      if os.path.exists(f'{path}/com'):
        return path 

    return None

  def is_successfully_disassembled(self):
    return self.smali_dir is not None

  def clean(self):
    # os.remove(f'{self.extract_dir}/framework-res.apk')
    # os.remove(f'{self.extract_dir}/{self.apk_name}.apk')
    # os.remove(f'{self.extract_dir}/{self.apk_name}_mod.apk')
    # shutil.rmtree(f'{self.extract_dir}/{self.apk_name}')
    shutil.rmtree(f'{self.extract_dir}')

  def log_stats(self, status='success'):
    # write headers
    if not os.path.exists('data/stats.csv'):
      with open('data/stats.csv', 'a') as fd:
        fd.write('"timestamp","manufacturer","model","rom","apk_name","on_unlocked_value","smali_dir","device","strategy","status"\n')

    with open('data/stats.csv', 'a') as fd:
      fd.write(f'"{os.path.basename(self.extract_dir)}","{self.manufacturer}","{self.model}","{self.rom}","{self.apk_name}","{self.on_unlocked_value}","{os.path.basename(self.smali_dir)}","{self.device}","{self.strategy}","{status}"\n')

  def patch_ScreenStateHelper(self):
    path = f'{self.smali_dir}/com/android/nfc/ScreenStateHelper.smali'
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
    path = f'{self.smali_dir}/com/android/nfc/NfcService.smali'
    with open(path) as fd:
      lines = fd.readlines()
      for i, line in enumerate(lines):
        if 'playSound' in line:
          insert_index = i + 2

        line = line.replace('SCREEN_OFF', 'SCREEN_OFF_DISABLED')
        line = line.replace('SCREEN_ON', 'SCREEN_ON_DISABLED')
        line = line.replace('USER_PRESENT', 'USER_PRESENT_DISABLED')
        line = line.replace('USER_SWITCHED', 'USER_SWITCHED_DISABLED')
        lines[i] = line

      # patch sound
      if insert_index:
        lines = lines[:insert_index] + ['return-void\n'] + lines[insert_index:]

    with open(path, 'w') as fd:
      fd.writelines(lines)

class PatcherOdex(Patcher):
  def disassemble(self):
    subprocess.run(['./disassemble_odex.sh', self.extract_dir, self.apk_name])
    self.smali_dir = self.get_smali_dir()

  def assemble(self):
    subprocess.run(['./assemble_odex.sh', self.extract_dir, self.apk_name])

  def get_smali_dir(self):
    return f'{self.extract_dir}/{self.apk_name}'

  # def clean(self):
    # os.remove(f'{self.extract_dir}/classes.dex')
    # os.remove(f'{self.extract_dir}/{self.apk_name}.odex')
    # os.remove(f'{self.extract_dir}/{self.apk_name}.vdex')
    # os.remove(f'{self.extract_dir}/{self.apk_name}.apk')
    # os.remove(f'{self.extract_dir}/{self.apk_name}_mod.apk')
    # shutil.rmtree(f'{self.extract_dir}/arm64')
    # shutil.rmtree(f'{self.extract_dir}/{self.apk_name}')
    # shutil.rmtree(f'{self.extract_dir}')

