"""
Grade a given ipynb file with okpy tests
"""
import argparse
import os
from glob import glob
from okgrade.notebook import grade_notebook

def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        'ipynb_path',
        help='Path to python file to grade'
    )

    args = argparser.parse_args()
    ipynb_path = os.path.abspath(args.ipynb_path)
    os.chdir(os.path.dirname(ipynb_path))

    base_path = os.path.dirname(ipynb_path)
    test_files = glob(os.path.join(base_path, 'tests/q*.py'))

    result = grade_notebook(ipynb_path, test_files)

    print(result.grade)

main()