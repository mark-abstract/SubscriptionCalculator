# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['SubscriptionCalculator.py'],
    pathex=[],
    binaries=[],
    datas=[('/opt/anaconda3/lib/tcl8.6', 'tcl'), ('/opt/anaconda3/lib/tk8.6', 'tk')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SubscriptionCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.icns'],
)
app = BUNDLE(
    exe,
    name='SubscriptionCalculator.app',
    icon='icon.icns',
    bundle_identifier=None,
)
