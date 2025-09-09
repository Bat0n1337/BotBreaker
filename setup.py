from setuptools import setup, find_packages
from botbreaker.version import __version__

setup(
    name='botbreaker',
    version=__version__,
    author='Bat0n1337',
    author_email='notbaton1337@gmail.com',
    description='A tool for searching for vulnerabilities in telegram bots',
    packages=find_packages(),
    install_requires=[
        'rich>=14.1.0',
        'click>=8.2.1',
        'Telethon>=1.41.2'
    ],
    entry_points={
        'console_scripts': [
            'botbreaker = botbreaker.botbreaker:main'
        ]
    },
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)