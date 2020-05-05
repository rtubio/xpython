import argparse, os


def is_valid_file(parser, arg):
    """
    This function simply checks whether the file exists or not. In case it does
    not exists, it raises an exception.
    """
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def is_valid_dir(parser, arg):
    """
    This function simply checks whether the dir exists or not. In case it does
    not exists, it raises an exception.
    """
    if not os.path.isdir(arg):
        parser.error("The directory %s does not exist!" % arg)

    if not os.access(arg, os.W_OK):
        parser.error("The directory %s is not writable!" % arg)

    return arg


def is_writable_file(arg):

    if not os.path.exists(arg):
        raise argparse.ArgumentTypeError(f"Path \"{arg}\" does not exist")
    if not os.path.isfile(arg):
        raise argparse.ArgumentTypeError(f"Path \"{arg}\" is not a file")
    if not os.access(arg, os.W_OK):
        raise argparse.ArgumentTypeError(f"Path \"{arg}\" is not writable")

    return arg
