# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=['src\\components\\submenu_file.py',
                     'src\\components\\submenu_about.py',
                     'src\\components\\menu.py',
                     'src\\components\\main_window.py',
                     'src\\components\\distance_func_frame.py',
                     'src\\components\\display_panel.py',
                     'src\\components\\control_panel.py',
                     'src\\event\\event_dispatcher.py',
                     'src\\event\\event_ids.py',
                     'src\\model\\constances.py',
                     'src\\model\\data_parser.py',
                     'src\\model\\path_calculator.py'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          name='MapDesigner',
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
               name='MapDesigner')
