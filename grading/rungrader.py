#!/usr/bin/env python3

import psycopg2
import psycopg2.extras
import subprocess
import argparse
import os
import json
import asyncio
import async_timeout
from postgrade import post_grade
from itertools import islice

argparser = argparse.ArgumentParser()
argparser.add_argument(
    '--image',
    default='yuvipanda/materials-x18',
    help='Image to use for grading'
)
argparser.add_argument(
    'lab_src_path_template',
    default='/mnt/prod-fileserver-01/{user_id}/materials-x18/materials/x18/lab/3/{lab}/{lab}.ipynb',
    help='template used to find a user\'s notebook'
)
argparser.add_argument(
    'lab_container_path_template',
    default='/srv/repo/materials/x18/lab/3/{lab}/{lab}.ipynb',
    help='Template to find original notebook inside container'
)
argparser.add_argument(
    'lab',
    help='Lab to grade'
)
argparser.add_argument(
    'resource_link_id',
    help='Resource Link ID for this lab'
)
argparser.add_argument(
    '--postgres-host',
    default='/run/csql/data8x-scratch:us-central1:prod-hubshard-db-instance',
    help='Hostname to use to connect to postgresql db'
)
argparser.add_argument(
    '--postgres-username',
    default='prod-db-proxyuser',
    help='Username for connecting to postgresql db'
)
argparser.add_argument(
    '--postgres-dbname',
    default='prod-hubshard-sharder-db',
    help='Database to connect to on postgres host'
)
argparser.add_argument(
    '--homedir-base',
    default='/export/pool0/homes',
    help='Base path where all user homedirs are'
)
argparser.add_argument(
    '--parallelism',
    default=64,
    type=int,
    help='Number of concurrent gradings to happen now'
)

args = argparser.parse_args()

LTI_CONSUMER_KEY = os.environ['LTI_CONSUMER_KEY']
LTI_CONSUMER_SECRET = os.environ['LTI_CONSUMER_SECRET']

async def main():
    conn = psycopg2.connect(
        host=os.path.abspath(args.postgres_host),
        user=args.postgres_username,
        dbname=args.postgres_dbname,
        password=os.environ['POSTGRES_PASSWORD'],
        cursor_factory=psycopg2.extras.DictCursor
    )

    posted_counts = 0
    total_counts = 0
    with conn.cursor() as cur:
        cur.execute(
            "select * from lti_launch_info_v1 where resource_link_id=%s",
            (args.resource_link_id, )
        )
        grade_coros = (
            grade_lab(args.lab_src_path_template, args.lab_container_path_template, row['user_id'], row['launch_info'], args.lab, args.image)
            for row in cur
        )

        for res in limited_as_completed(grade_coros, args.parallelism):
            posted = await res
            if posted:
                posted_counts += 1
            total_counts += 1
            if total_counts % 500 == 0:
                print(f'Posted {posted_counts} scores after checking {total_counts} assignments')

        print(f'Posted {posted_counts} scores after checking {total_counts} assignments')

def limited_as_completed(coros, limit):
    futures = [
        asyncio.ensure_future(c)
        for c in islice(coros, 0, limit)
    ]
    async def first_to_finish():
        while True:
            await asyncio.sleep(0)
            for f in futures:
                if f.done():
                    futures.remove(f)
                    try:
                        newf = next(coros)
                        futures.append(
                            asyncio.ensure_future(newf))
                    except StopIteration as e:
                        pass
                    return f.result()
    while len(futures) > 0:
        yield first_to_finish()

async def grade_lab(lab_src_path_template, lab_container_path_template, user_id, launch_info, lab, grader_image):
    src_path = lab_src_path_template.format(
        user_id=user_id,
        lab=lab
    )
    if not os.path.exists(src_path):
        # The princess is in another file server, mario
        return False

    command = [
        'docker', 'run',
        '--rm',
        '-m', '2G',
        '-i',
        '--net=none',
        grader_image,
        "/srv/repo/grading/containergrade.bash",
        lab_container_path_template.format(lab=lab)
    ]
    process = await asyncio.create_subprocess_exec(
        *command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    with open(src_path) as f:
        content = f.read().encode('utf-8')
        try:
            async with async_timeout.timeout(300):
                stdout, stderr = await process.communicate(content)
        except asyncio.TimeoutError:
            print(f'Grading timed out for {src_path}')
            return False
        for line in stderr.decode('utf-8').split('\n'):
            if line.strip() == '':
                # Ignore empty lines
                continue
            if 'Killed' in line:
                # Our container was killed, so let's just skip this one
                return False
            if not line.startswith('WARNING:'):
                print(line)
                raise Exception("Found unrecognized output in stderr from {}, halting".format(' '.join(command)))
    grade = float(stdout.decode("utf-8").strip().split("\n")[-1])
    if lab == 'lab02' and grade > 0.9:
        # HACK
        grade = 1
        print('rounding up lab02')
    if grade != 0.0:
        if 'lis_outcome_service_url' not in launch_info:
            print(f'Missing list_outcome_service_url in {src_path}')
            return False
        await post_grade(
            launch_info['lis_result_sourcedid'],
            launch_info['lis_outcome_service_url'],
            LTI_CONSUMER_KEY,
            LTI_CONSUMER_SECRET,
            grade
        )
        return True
    return False

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the commands
    loop.run_until_complete(main())
    loop.close()
