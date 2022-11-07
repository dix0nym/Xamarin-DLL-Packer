# Xamarin DLL Packer

Extract and compress DLLs for Xamarin apps.
Initial version and inspired by [x41sec/tools](https://github.com/x41sec/tools/blob/master/Mobile/Xamarin/Xamarin_XALZ_decompress.py) and their [blog article](https://www.x41-dsec.de/security/news/working/research/2020/09/22/xamarin-dll-decompression/)

## Installation

```bash
$ git clone https://github.com/dix0nym/Xamarin-DLL-Packer.git
$ cd Xamarin-DLL-Packer
```

**Dependencies**:
- [lz4](https://pypi.org/project/lz4/)

```bash
$ pip install lz4
```

## Usage

```bash
usage: xamarin_dll.py [-h] [-o OUTPUT] input

compress and decompress Xamarin DLLs

positional arguments:
  input                 path to dll or directory containing multiple DLLs

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        path to output directory
```

### Examples

```bash
# one dll -> will extract to current folder as test.decompressed.dll
$ python xamarin_dll.py test.dll

# multiple dlls - specified as input folder -> extract to current folder with [filename].decompressed.dll
$ python xamarin_dll.py test_folder

# one dll with specified output folder
$ python xamarin_dll.py -o output_folder test.dll

# multiple dll with specified output folder
$ python xamarin_dll.py -o output_folder test_folder
```