# -*- mode: python ; coding: utf-8 -*-


pyms_a = Analysis(
    ['..\\PyMS.pyw'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyms_pyz = PYZ(pyms_a.pure)

pyms_exe = EXE(
    pyms_pyz,
    pyms_a.scripts,
    exclude_binaries=True,
    name='PyMS',
    icon='..\\UI Resources\\iconPyMSRun.ico',
    version='.\\pyms-version.txt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

cycle_a = Analysis(
    ['..\\CycleEditor.pyw'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
cycle_pyz = PYZ(cycle_a.pure)

cycle_exe = EXE(
    cycle_pyz,
    cycle_a.scripts,
    exclude_binaries=True,
    name='CycleEditor',
    icon='..\\UI Resources\\iconPyMSRun.ico',
    version='.\\cycle-version.txt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


ncc_a = Analysis(
    ['..\\NccViewer.pyw'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
ncc_pyz = PYZ(ncc_a.pure)

ncc_exe = EXE(
    ncc_pyz,
    ncc_a.scripts,
    exclude_binaries=True,
    name='NccViewer',
    icon='..\\UI Resources\\iconNccCalc.ico',
    version='.\\ncc-version.txt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)





coll = COLLECT(
    pyms_exe,
    pyms_a.binaries,
    pyms_a.datas,
    ncc_exe,
    ncc_a.binaries,
    ncc_a.datas,
    cycle_exe,
    cycle_a.binaries,
    cycle_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PyMS',
)
