from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='heiya',
    version='2.3.1',
    description='Convert between image and High Efficiency Image (HEIC/AVIF) with ease.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='Apache License 2.0',
    packages=find_packages(),
    author='Hongjun Wu',
    author_email='hw434@cornell.edu',
    keywords=['HEIC', 'AVIF', 'TIFF', "JPG",'ImageConversion'],
    url='https://github.com/wu-hongjun/heiya',
    download_url='https://pypi.org/project/heiya/'
)

install_requires = [
    'piexif',
    'pillow_heif',
    'pyperclip',
    'pathlib',
    'Pillow',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
