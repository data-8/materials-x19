"""
Post grades to EdX from a CSV file
"""
import argparse
import csv
import json
import time
import os
from postgrade import post_grade


def read_launch_info(postgres_csv_path):
    launch_info = {}
    with open(postgres_csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            launch_info[row[1]] = json.loads(row[3])

    return launch_info

def post_grades(grades_csv_path, launch_infos, consumer_key, consumer_secret):
    with open(grades_csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            user, score = row
            if user in launch_infos and float(score) != 0.0:
                lti_launch_info = launch_infos[user]
                post_grade(
                    lti_launch_info['lis_result_sourcedid'],
                    lti_launch_info['lis_outcome_service_url'],
                    consumer_key,
                    consumer_secret,
                    score
                )
                print(f'Posted {score} for {user}')
                time.sleep(1)


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('postgres_csv_path')
    argparser.add_argument('grades_csv_path')

    args = argparser.parse_args()

    consumer_key = os.environ['LTI_CONSUMER_KEY']
    consumer_secret = os.environ['LTI_CONSUMER_SECRET']

    launch_infos = read_launch_info(args.postgres_csv_path)

    post_grades(args.grades_csv_path, launch_infos, consumer_key, consumer_secret)

main()
