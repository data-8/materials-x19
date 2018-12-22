#!/usr/bin/env python3
import sys
import argparse
from datetime import datetime, timedelta


def adjust_score(score, category, submitted_at, deadline, full_cutoff=None,
                 partial_cutoff=None, max_score=None):
    """Adjusts the score depending on checkpoints met, as well as the
    assignment category. Outputs the adjusted score, along with the reason
    behind the applied adjustment.
    """

    return score, reason


def valid_date(s):
    """Checks if a date is in the valid format %m/%d/%Y. Offsets it by a
    constant amount to fix it at a minute before midnight.
    """
    try:
        offset = timedelta(hours=23, minutes=59, seconds=59)
        return datetime.strptime(s, "%m/%d/%Y") + offset
    except ValueError:
        msg = "Not a valid date: '{}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def parse_ok_output(output):
    point_breakdown = []
    reversed_list = output.splitlines()[::-1]
    score_lines = output.splitlines()
    for ind, line in enumerate(reversed_list):
        if line.lstrip().startswith('Score:'):
            point_breakdown = reversed_list[ind+1:][::-1]
            score_lines = reversed_list[:ind+1][::-1]
            break
    for line in score_lines:
        line = line.lstrip()
        if line.startswith('Total:'):
            _, score = line.rsplit(maxsplit=1)
    try:
        lines, score_f = '\n'.join(point_breakdown), float(score)
    except UnboundLocalError as e:
        print("No lines found with Score Tag?", e)
        print()
        raise e

    return lines, score_f

def main():
    parser = argparse.ArgumentParser(description='Grade an assignment')
    parser.add_argument('infile', help='the ok dump to be parsed')
    parser.add_argument('--max-score', type=float,
                        help='score received when getting full credit')

    args = parser.parse_args()

    try:
        from info import info
        submitted_at = datetime.strptime(info['timestamp'],
                                         '%Y-%m-%d %H:%M:%S.%f')
    except ImportError:
        info = None
        submitted_at = datetime.now()

    with open(args.infile) as infile:
        output = infile.read()

    point_breakdown, score = parse_ok_output(output)
    print(point_breakdown, end='', file=sys.stderr)

    print('Score:', file=sys.stderr)
    print('    Total:', score, file=sys.stderr)
    print('    ', score / args.max_score,'out of 1.0', file=sys.stderr)
    print(score / args.max_score)

if __name__ == "__main__":
    main()
