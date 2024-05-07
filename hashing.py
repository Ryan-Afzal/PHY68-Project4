## hashing.py - Husam Adam, Ryan Afzal, Labib Afia
## This file is meant to creates and returns a file's hash.

import hashlib

def hash_file(file_path, chunk_size=4096):
    # Initialize the hash object
    hash_obj = hashlib.sha256()

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        while True:
            # Read a chunk of data from the file
            chunk = file.read(chunk_size)
            if not chunk:
                break
            # Update the hash object with the chunk
            hash_obj.update(chunk)

    # Return the hexadecimal representation of the hash
    return hash_obj.hexdigest()