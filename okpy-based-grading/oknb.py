#!/usr/bin/env python3
""" Utility Script to allow autograding of notebooks.
Author: @Sumukh
Date: 01/23/17
"""
import argparse
import json
import os


REQUIRED_PROTOCOLS = ['grading', 'scoring']
DEFUALT_FILTERS = ["ok.auth(", "ok.grade(", "ok.auth(", "ok.submit(", "ok.backup(",
                   "!git ", "!pip "]

def make_grading_cell(score_file):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {
            "collapsed": False
        },
        "outputs": [],
        "source": [
            "# Ok Autograding Start\n",
            "_ = ok.score(score_out='{}')\n".format(score_file),
            "# Ok Autograding Run\n"
        ]
    }

def make_ok_cell(config):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {
            "collapsed": False
        },
        "outputs": [],
        "source": [
            "# Ok config Start\n",
            "from client.api.notebook import Notebook\n",
            "ok = Notebook('{}')\n".format(config),
            "# Ok config End\n"
        ]
    }

def filter(notebook, filter_list, debug=False):
    if filter_list is None:
        filter_list = DEFUALT_FILTERS
    cells = notebook['cells']
    for cell in cells:
        if cell['cell_type'] == "code":
            filtered_lines = []
            for line in cell['source']:
                if any(x in line for x in filter_list):
                    line = "### Commented for autograding ### {}".format(line)
                    if debug:
                        print("Filtered out line with {}".format(line))
                filtered_lines.append(line)
            cell['source'] = filtered_lines
    return notebook

def tweak_ok(config, debug=False):
    """ Tweak the ok config file.
    """
    if not config:
        return

    with open(config, 'r') as f:
        contents = json.load(f)

    if not all(r in contents['protocols'] for r in REQUIRED_PROTOCOLS):
        for req in REQUIRED_PROTOCOLS:
            if req not in contents['protocols']:
                contents['protocols'].append(req)

                if debug:
                    print("Adding the {} protocol".format(req))
        with open(config, 'w') as f:
            contents = json.dump(contents, f, indent=2, sort_keys=True)
        if debug:
            print("Wrote to {}".format(config))

def main():
    parser = argparse.ArgumentParser(
        description=("Prepare a notebook for OK Grading.\n"
                     "Adjust the ok config, filter out lines to avoid running,\n"
                     " and insert the grading cell"))
    parser.add_argument('in_file', help='the notebook to be parsed')
    parser.add_argument('out_file', help='the file to write to')
    parser.add_argument('score_file', help='the file to write to write the score')
    parser.add_argument('--config', help='ok config file to change')
    parser.add_argument('--debug', help='debug prints')
    parser.add_argument('--filter', action="append",
                        help='comment out lines that match the pattern')
    args = parser.parse_args()

    has_all_files = True
    if not os.path.isfile(args.config):
        print("Could not find config ('{}') in directory".format(args.config))
        has_all_files = False
    if not os.path.isfile(args.in_file):
        print("Could not find infine ('{}') in directory".format(args.in_file))
        has_all_files = False

    if not has_all_files:
        curr_dir_files = ','.join(os.listdir())
        print("Current Directory has the following files: {}".format(curr_dir_files))

    tweak_ok(args.config, debug=args.debug)

    contents = None
    try:
        with open(args.in_file, 'r') as f:
            contents = json.load(f)
    except:
        print("Could not load the file: {}".format(contents))

    contents = filter(contents, args.filter, debug=args.debug)
    contents['cells'].append(make_ok_cell(args.config))
    contents['cells'].append(make_grading_cell(args.score_file))
    if args.debug:
        print("Added scoring cell to bottom of notebook")

    with open(args.out_file, 'w') as f:
        json.dump(contents, f, indent=2, sort_keys=True)

if __name__ == "__main__":
    main()
