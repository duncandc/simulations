""" Module used to create a small collection of merger tree data with the
same file patterns and data stream as the full trees.
Useful for creating a more tractable data stream for exploring different
tree-walking strategies.
"""
import os
from filename_utils import tree_subvol_substring_from_int as fname_from_int


def char_generator(hlist_filename):
    with open(hlist_filename, 'r') as f:
        for i, raw_line in enumerate(f):
            if raw_line[0] == '#':
                yield i


def last_header_index(hlist_filename):
    """ Return the index of the final header line that begins with '#',
    starting from index-0. The subsequent line that has index equal to
    last_header_index + 1 is a special line storing only a single integer,
    num_total_trees. After that special line, the repeating pattern begins.
    """
    with open(hlist_filename, 'r') as f:
        for i, raw_line in enumerate(f):
            if raw_line[0] != '#':
                return i


def read_header(hlist_filename):
    """ Return the header as a list of strings, each beginning with '#'
    """
    with open(hlist_filename, 'r') as f:
        while True:
            header_line = next(f)
            if header_line[0] == '#':
                yield header_line
            else:
                break


def tree_selection_generator(hlist_filename, i, j):
    """ Yield all raw lines of hlist_filename pertaining to [tree_i, tree_j),
    excluding the header, but including the lines such as '#tree 2810141744'.

    For example, tree_sequence_generator(hlist_filename, 2, 5) will yield the
    subset of rows of hlist_filename pertaining to tree 2, tree 3, and tree 4.
    This generator can be used to extract the data rows necessary to create a
    desired slice of a tree file.
    """
    msg1 = "Final tree integer j = {0} must exceed first tree integer i = {1}".format(i, j)
    assert j > 1,  msg1

    with open(hlist_filename, 'r') as f:

        # skip the header
        while True:
            header_line = next(f)
            if header_line[0] == '#':
                pass
            else:
                num_total_trees = int(header_line.strip())
                break

        msg2 = "There are num_total_trees = {0} < j = {1}".format(num_total_trees, j)
        assert num_total_trees > j, msg2

        try:
            tree_counter = -1
            while tree_counter < j:
                raw_line = next(f)
                if raw_line[0] == '#':
                    tree_counter += 1
                if (tree_counter >=i) & (tree_counter < j):
                    yield raw_line

        except StopIteration:
            msg3 = "Unexpectedly reached end of hlist file, which must not be formatted correctly"
            raise IndexError(msg3)


def make_tree_collection(hlist_filename, output_dirname,
        num_divs=5, num_trees_per_output_file=3):
    """ Create a collection of trees from a single subvolume.
    """
    header = list(read_header(hlist_filename))

    num_output_files = num_divs**3

    first_tree = 0
    for i in range(num_output_files):

        # Retrieve the relevant data
        last_tree = first_tree + num_trees_per_output_file
        data = tree_selection_generator(hlist_filename, first_tree, last_tree)

        # Create an output filename
        subvol_str = fname_from_int(i, num_divs)
        output_basename = 'tree_'+subvol_str+'.dat'
        output_fname = os.path.join(output_dirname, output_basename)

        # Write a header, followed by num_trees_per_output_file, followed by the relevant data
        with open(output_fname, 'wb') as f:

            for line in header:
                f.write(line)
            f.write(str(num_trees_per_output_file)+"\n")
            for line in data:
                f.write(line)

        first_tree = last_tree
