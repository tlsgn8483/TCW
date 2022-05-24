# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['D:\\Smart_PCRSetup\\Smart_PCRSetup\\Make_Worklist.py'],
             pathex=['D:\\Smart_PCRSetup\\Smart_PCRSetup\\bin', 'C:\\WorkList'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt6.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Make_Worklist',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Make_Worklist')
