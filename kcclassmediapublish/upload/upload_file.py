import os

TMP_UPLOAD_DIR = "/tmp"

def get_file_from_user(filename, input_file):
    """
    Retrieves file form the user.
    """
    # Using the filename like this without cleaning it is very
    # insecure so please keep that in mind when writing your own
    # file handling.
    out_filepath = os.path.join(TMP_UPLOAD_DIR, filename)
    output_file = open(out_filepath, "wb")
    # Finally write the data to the output file
    input_file.seek(0)
    while 1:
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)
    output_file.close()
    return out_filepath