import os
import time
import random
from tqdm import tqdm

FILE_SIZE = 1024 * 1024 * 1024  
KB_BLOCK_SIZE = 1024  
GB_BLOCK_SIZE = FILE_SIZE  
KB_TOTAL_BLOCKS = FILE_SIZE // KB_BLOCK_SIZE
GB_TOTAL_BLOCKS = 1
RANDOM_BLOCK_SIZE = 4096  
RANDOM_TOTAL_BLOCKS = FILE_SIZE // RANDOM_BLOCK_SIZE
RANDOM_ACCESS_COUNT = 10000  

def create_dummy_file(filename, size):
    print(f"Creating dummy file: {filename}")
    with open(filename, 'wb') as f:
        f.seek(size - 1)
        f.write(b'\0')
    print("File creation complete.\n")

def calculate_speed(duration, size):
    return (size / duration) / (1024 * 1024)  

def run_test(filename, block_size, total_blocks, mode, description):
    print(f"Starting {description}...")
    start_time = time.time()
    with open(filename, mode) as f, tqdm(total=total_blocks, desc=description, unit='block') as pbar:
        for _ in range(total_blocks):
            if 'w' in mode:
                f.write(os.urandom(block_size))
            else:
                f.read(block_size)
            pbar.update(1)
    end_time = time.time()
    duration = end_time - start_time
    speed = calculate_speed(duration, block_size * total_blocks)
    print(f"{description} completed. Duration: {duration:.2f} seconds. Speed: {speed:.2f} MB/s\n")
    return duration, speed

def random_access_test(filename, block_size, access_count, mode):
    description = f"Random {mode.capitalize()} Access (4KB blocks)"
    print(f"Starting {description}...")
    start_time = time.time()
    with open(filename, mode + "b") as f, tqdm(total=access_count, desc=description, unit='op') as pbar:
        for _ in range(access_count):
            random_position = random.randint(0, RANDOM_TOTAL_BLOCKS - 1) * block_size
            f.seek(random_position)
            if 'w' in mode:
                f.write(os.urandom(block_size))
            else:
                f.read(block_size)
            pbar.update(1)
    end_time = time.time()
    duration = end_time - start_time
    speed = calculate_speed(duration, block_size * access_count)
    print(f"{description} completed. Duration: {duration:.2f} seconds. Speed: {speed:.2f} MB/s\n")
    return duration, speed

if __name__ == "__main__":
    test_file = "test_file.bin"
    create_dummy_file(test_file, FILE_SIZE)

    run_test(test_file, KB_BLOCK_SIZE, KB_TOTAL_BLOCKS, 'wb', "1kB (Total 1GB) Sequential Write")
    run_test(test_file, KB_BLOCK_SIZE, KB_TOTAL_BLOCKS, 'rb', "1kB (Total 1GB) Sequential Read")
    run_test(test_file, GB_BLOCK_SIZE, GB_TOTAL_BLOCKS, 'wb', "1GB Sequential Write")
    run_test(test_file, GB_BLOCK_SIZE, GB_TOTAL_BLOCKS, 'rb', "1GB Sequential Read")

    random_access_test(test_file, RANDOM_BLOCK_SIZE, RANDOM_ACCESS_COUNT, 'w')
    random_access_test(test_file, RANDOM_BLOCK_SIZE, RANDOM_ACCESS_COUNT, 'r')

    os.remove(test_file)
    print("Cleanup complete. Test file removed.")
