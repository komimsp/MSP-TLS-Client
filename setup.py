#!/usr/bin/env python
from setuptools.command.install import install
from setuptools import setup, find_packages, Command
from codecs import open
import os
import platform
import urllib.request

class DownloadBinaryCommand(Command):
    """A custom command to download the appropriate binary for the current OS."""
    description = 'Download the appropriate binary for the current operating system'
    user_options = []
    
    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        binary_url = None
        os_type = platform.system()
        architecture = platform.architecture()[0]
        
        URLS = {
            'Win32': 'https://github.com/xerusmsp/msp-tls-client/releases/download/0.1.0/tls-client-32.dll',
            'Win64': 'https://github.com/xerusmsp/msp-tls-client/releases/download/0.1.0/tls-client-64.dll',
            # 'DarwinArm64': '',
            # 'Darwinx86': ''
        }

        if os_type == 'Windows':
            if architecture == '32bit':
                binary_url = URLS.get('Win32')
            else:
                binary_url = URLS.get('Win64')
        elif os_type == 'Darwin':
            if architecture == '64bit':
                binary_url = URLS.get('DarwinArm64')
            else:
                binary_url = URLS.get('Darwinx86')

        if not binary_url:
            raise RuntimeError(f"Unsupported operating system: {os_type}")
        
        binary_name = binary_url.split('/')[-1]

        download_path = os.path.join(os.path.dirname(__file__), 'msp-tls-client', 'dependencies', binary_name)

        os.makedirs(os.path.dirname(download_path), exist_ok=True)

        print(f"Downloading {binary_name} for {os_type}...")
        urllib.request.urlretrieve(binary_url, download_path)

        print(f"{binary_name} downloaded and ready to use.")

class CustomInstallCommand(install):
    def run(self):
        self.run_command('download_binary')
        install.run(self)

setup(
    name="msp_tls_client",
    version="0.1.0",
    author="admin@xerus.lol",
    description="TLS client for MSP",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*'],
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
    project_urls={
        "Source": "https://github.com/xerusmsp/msp-tls-client",
    },
    cmdclass={
        'download_binary': DownloadBinaryCommand,
        'install': CustomInstallCommand,
    }
)