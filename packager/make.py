"""
Build script for Python Mass Spectrometry (PyMS) Windows distribution packages.

This script handles the complete build process for PyMS Windows applications:
1. Updates version information in all application components
2. Builds executable files using PyInstaller
3. Creates Windows installation packages using SourceForge Install Forge

Dependencies:
- pyinstaller_versionfile: Creates Windows-format version files
- PyInstaller: Builds Windows executables
- SourceForge Install Forge: Creates Windows setup packages

Usage:
    python make.py
"""


import subprocess
import shutil
from datetime import datetime
import pyinstaller_versionfile
import PyInstaller.__main__
from app_control import VERSION

START_TIME = datetime.now()

print('Starting build for Version: %s' % VERSION)

# Install Forge executable for windows setup build
INSTALL_FORGE_EXECUTABLE = 'C:\\Program Files (x86)\\solicus\\InstallForge\\bin\\ifbuildx86.exe'
# set version information
WINDOWS_FORMAT_VERSION = '%s.0' % VERSION
LEGAL_COPYRIGHT = '© %s TS Technologies. All rights reserved.' % str(datetime.now().year)
COMPANY_NAME = 'TS Technologies https://github.com/westerlymerlin/'
PRODUCT_NAME = 'Python Mass Spectrometry (PyMS)'
print('Updating version info in build files to %s' % WINDOWS_FORMAT_VERSION)


pyinstaller_versionfile.create_versionfile(
    output_file="pyms-version.txt",
    version=WINDOWS_FORMAT_VERSION,
    company_name=COMPANY_NAME,
    file_description="PyMS Main application",
    internal_name="PyMS",
    legal_copyright=LEGAL_COPYRIGHT,
    original_filename="PyMS.exe",
    product_name=PRODUCT_NAME,
    translations=[0, 1200]
)
print('Finished updating version info in pyms-version.txt')


pyinstaller_versionfile.create_versionfile(
    output_file="ncc-version.txt",
    version=WINDOWS_FORMAT_VERSION,
    company_name=COMPANY_NAME,
    file_description="PyMS Ncc file viewer and calculator",
    internal_name="NccViewer",
    legal_copyright=LEGAL_COPYRIGHT,
    original_filename="NccViewer.exe",
    product_name=PRODUCT_NAME,
    translations=[0, 1200]
)
print('Finished updating version info in ncc-version.txt')

pyinstaller_versionfile.create_versionfile(
    output_file="cycle-version.txt",
    version=WINDOWS_FORMAT_VERSION,
    company_name=COMPANY_NAME,
    file_description="PyMS cycle editor",
    internal_name="CycleEditor",
    legal_copyright=LEGAL_COPYRIGHT,
    original_filename="CycleEditor.exe",
    product_name=PRODUCT_NAME,
    translations=[0, 1200]
)
print('Finished updating version info in cycle-version.txt')

pyinstaller_versionfile.create_versionfile(
    output_file="testgen-version.txt",
    version=WINDOWS_FORMAT_VERSION,
    company_name=COMPANY_NAME,
    file_description="PyMS test application",
    internal_name="PyMS",
    legal_copyright=LEGAL_COPYRIGHT,
    original_filename="testgen.exe",
    product_name=PRODUCT_NAME,
    translations=[0, 1200]
)
print('Finished updating version info in testgen-version.txt')


package_data = []
with open("package.ifp", "r", encoding='utf-8') as package_file:
    for line in package_file:
        package_data.append(line)
package_file.close()

with open("package.ifp", "w", encoding='utf-8') as packagefile:
    for line in package_data:
        if line[:13] == '    <Version>':
            line = '    <Version>%s</Version>\n' % VERSION
        packagefile.write(line)
packagefile.close()


# run pyinstaller
print('Starting Pyinstaller - this may take some time only warn logs are output')

PyInstaller.__main__.run(['package.spec', '--noconfirm', '--log-level=WARN'])

print('Pyinstaller Completed')

print('copying json files for testing')
shutil.copy('..\\settings.json', '.\\dist\\PyMS')
shutil.copy('..\\SECRETS', '.\\dist\\PyMS')
print('copy completed')

print('Starting Install forge')
subprocess.call(INSTALL_FORGE_EXECUTABLE + ' -i "package.ifp" -o "..\\distribution\\PyMS-installer.exe"')

print('make script finished after %s seconds' % (datetime.now() - START_TIME).seconds)
