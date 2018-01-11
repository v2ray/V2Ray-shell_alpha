# -*- mode: python -*-

block_cipher = None


a = Analysis(['bridge.py'],
             pathex=['./bridgehouse'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
icons = Tree('icons', 'icons')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          icons,
          name='v2ray-shell',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False, 
          icon="./icons/start.ico")
