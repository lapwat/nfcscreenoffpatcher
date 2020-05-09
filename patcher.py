from dotenv import dotenv_values

class Patcher:
  def __init__(self, extract_dir):
    self.extract_dir = extract_dir
    self.env = dotenv_values(f'{extract_dir}/.env')
    print(f'Working with {self.env}')

  def patch_ScreenStateHelper(self):
    path = f"{self.extract_dir}/{self.env['APK_NAME']}/smali/com/android/nfc/ScreenStateHelper.smali"
    with open(path) as fd:
      lines = fd.readlines()
      for i, line in enumerate(lines):
        if 'SCREEN_STATE_ON_UNLOCKED' in line:
          on_unlocked_value = line.strip().split(' ')[-1]
        if 'checkScreenState' in line:
          insert_index = i + 2

      lines = lines[:insert_index] + [f'const/16 v0, {on_unlocked_value}\n', 'return v0\n'] + lines[insert_index:]
    
    with open(path, 'w') as fd:
      fd.writelines(lines)

  def patch_NfcService(self):
    path = f"{self.extract_dir}/{self.env['APK_NAME']}/smali/com/android/nfc/NfcService.smali"
    with open(path) as fd:
      lines = fd.readlines()
      for i, line in enumerate(lines):
        line = line.replace('SCREEN_OFF', 'SCREEN_OFF_DISABLED')
        line = line.replace('SCREEN_ON', 'SCREEN_ON_DISABLED')
        line = line.replace('USER_PRESENT', 'USER_PRESENT_DISABLED')
        line = line.replace('USER_SWITCHED', 'USER_SWITCHED_DISABLED')

#        if 'if-lt' in line:
#          line = f'#{line}'

        lines[i] = line
    
    with open(path, 'w') as fd:
      fd.writelines(lines)
