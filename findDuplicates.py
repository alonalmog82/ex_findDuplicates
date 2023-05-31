import os
import sys
import hashlib

# function to get md5 hash from file (thanks chatgpt)
def calculate_file_hash(file_path, algorithm='md5'):
    hash_object = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_object.update(chunk)
    return hash_object.hexdigest()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Check if the path argument was provided
    if len(sys.argv) < 2:
        print("Please provide a path argument.")
        sys.exit(1)

    # Get the path from the command line argument
    path = sys.argv[1]

    # Check if the path exists
    if not os.path.exists(path):
        print("The path provided does not exist.")
        sys.exit(1)

    file_dict = {}

    try:
        # Walk through all files and directories starting from the provided path
        for root, dirs, files in os.walk(path):
            for filename in files:
                # Get the full path of the file
                filepath = os.path.join(root, filename)
                try:
                    md5hash = calculate_file_hash(filepath)
                    if md5hash in file_dict:
                        #dictionary doesn't support an append or extend function. For our purposes, I'm checking if the value is a list
                        if isinstance(file_dict[md5hash], list):
                            file_dict[md5hash].append(filename)
                        else:
                            file_dict[md5hash] = [file_dict[md5hash], filename]
                    else:
                        file_dict[md5hash] = [filename]
                except Exception as e:
                    print(f"An error occurred while hashing files: {str(e)}")
                    sys.exit(1)
    except Exception as e:
        print(f"An error occurred while processing files: {str(e)}")
        sys.exit(1)
    #print only duplicates
    for key, values in file_dict.items():
        if len(values) > 1:
            print("duplicate files: ", end = '')
            print(', '.join(values))