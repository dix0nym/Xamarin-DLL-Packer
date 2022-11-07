import lz4.block
import argparse
import struct
from pathlib import Path

def decompress(data):
    header_index = data[4:8]
    header_uncompressed_length = struct.unpack('<I', data[8:12])[0]
    payload = data[12:]
    
    print("header index: %s" % header_index)
    print("compressed payload size: %s bytes" % len(payload))
    print("uncompressed length according to header: %s bytes" % header_uncompressed_length)
    
    decompressed = lz4.block.decompress(payload, uncompressed_size=header_uncompressed_length)
    return decompressed

def compress(data):
    header_uncompressed_length = struct.pack('<I', len(data))
    compressed = lz4.block.compress(data, mode='high_compression')[4:]
    compressed_size = len(compressed)
    header_index = struct.pack('<I', 1)

    print("header index: %s" % header_index)
    print("compressed payload size: %s bytes" % compressed_size)
    print("uncompressed length according to header: %s bytes" % len(data))

    compressed = b'XALZ' + header_index + header_uncompressed_length + compressed
    return compressed

def start(inputPath, outputPath):
    header_expected_magic = b'XALZ'
    with inputPath.open('rb') as xalz_file:
        data = xalz_file.read()
        result = None
        if data[:4] != header_expected_magic:
            result = compress(data)
            outputPath = outputPath.joinpath(f"{inputPath.stem}.compressed{inputPath.suffix}")
        else:
            outputPath = outputPath.joinpath(f"{inputPath.stem}.decompressed{inputPath.suffix}")
            result = decompress(data)
        with outputPath.open('wb') as output_file:
            output_file.write(result)
        print(f"result written to {outputPath.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='compress and decompress Xamarin DLLs')
    parser.add_argument('input', type=Path, help='path to dll or directory containing multiple DLLs')
    parser.add_argument('-o', '--output', type=Path, help='path to output directory', default=Path(__file__).absolute().parent)
    args = parser.parse_args()
    
    inputPath = args.input
    outputPath = args.output
    if not outputPath.exists():
        outputPath.mkdir(exist_ok=True, parents=True)
    if inputPath.exists():
        if inputPath.is_dir():
            for inputFile in inputPath.glob('*.dll'):
                start(inputFile, outputPath)
        else:
            start(inputPath, outputPath)