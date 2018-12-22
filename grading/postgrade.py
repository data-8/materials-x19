"""
Script to post grades back to EdX.

How to run standalone:

1. Find out the lti_launch_info for the user / lab combo.

   1. Open up a postgresql shell with:

      bash grading/psql

   2. Find the lti_launch_info for the user / lab with:

      SELECT * FROM user_id='user_id' AND resource_link_id='resource_link_id';

      user_id is the EdX user id that is specific for the course. It
      is the same as the hub user id. You can easily find this from
      https://edx.readthedocs.io/projects/open-edx-building-and-running-a-course/en/named-release-birch/running_course/course_student.html#access-anonymized

   3. Copy the third row (launch_info)

2. Run this script.

   1. Make sure you are in the venv:

      source bin/activate

   2. Run this!

      python grading/postgrade.py '<json copied from step 1>' <grade>

      The single quotes are important
"""
import json
import os
import time
from oauthlib.oauth1.rfc5849 import signature, parameters
from lxml import etree
from hashlib import sha1
import argparse
import base64
import aiohttp
import asyncio
import async_timeout


class GradePostException(Exception):
    def __init__(self, response=None):
        self.response = response

async def post_grade(sourcedid, outcomes_url, consumer_key, consumer_secret, grade):
    # Who is treating XML as Text? I am!
    # WHY WOULD YOU MIX MULTIPART, XML (NOT EVEN JUST XML, BUT WSDL GENERATED POX WTF), AND PARTS OF OAUTH1 SIGNING
    # IN THE SAME STANDARD AAAA!
    # TODO: extract this into a real library with real XML parsing
    # WARNING: You can use this only with data you trust! Beware, etc.
    post_xml = r"""
    <?xml version = "1.0" encoding = "UTF-8"?>
    <imsx_POXEnvelopeRequest xmlns = "http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">
      <imsx_POXHeader>
        <imsx_POXRequestHeaderInfo>
          <imsx_version>V1.0</imsx_version>
          <imsx_messageIdentifier>999999123</imsx_messageIdentifier>
        </imsx_POXRequestHeaderInfo>
      </imsx_POXHeader>
      <imsx_POXBody>
        <replaceResultRequest>
          <resultRecord>
            <sourcedGUID>
              <sourcedId>{sourcedid}</sourcedId>
            </sourcedGUID>
            <result>
              <resultScore>
                <language>en</language>
                <textString>{grade}</textString>
              </resultScore>
            </result>
          </resultRecord>
        </replaceResultRequest>
      </imsx_POXBody>
    </imsx_POXEnvelopeRequest>
    """
    post_data = post_xml.format(grade=float(grade), sourcedid=sourcedid)

    # Yes, we do have to use sha1 :(
    body_hash_sha = sha1()
    body_hash_sha.update(post_data.encode('utf-8'))
    body_hash = base64.b64encode(body_hash_sha.digest()).decode('utf-8')
    args = {
        'oauth_body_hash': body_hash,
        'oauth_consumer_key': consumer_key,
        'oauth_timestamp': str(time.time()),
        'oauth_nonce': str(time.time())
    }

    base_string = signature.construct_base_string(
        'POST',
        signature.normalize_base_string_uri(outcomes_url),
        signature.normalize_parameters(
            signature.collect_parameters(body=args, headers={})
        )
    )

    oauth_signature = signature.sign_hmac_sha1(base_string, consumer_secret, None)
    args['oauth_signature'] = oauth_signature

    headers = parameters.prepare_headers(args, headers={
        'Content-Type': 'application/xml'
    })


    async with async_timeout.timeout(10):
        async with aiohttp.ClientSession() as session:
            async with session.post(outcomes_url, data=post_data, headers=headers) as response:
                resp_text = await response.text()

                if response.status != 200:
                    raise GradePostException(response)

    response_tree = etree.fromstring(resp_text.encode('utf-8'))

    # XML and its namespaces. UBOOF!
    status_tree = response_tree.find('.//{http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0}imsx_statusInfo')
    code_major = status_tree.find('{http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0}imsx_codeMajor').text

    if code_major != 'success':
        raise GradePostException(response)


async def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'lti_launch_info',
        help="Full LTI Launch info, in JSON format"
    )
    argparser.add_argument(
        'grade',
        help='Grade to post',
        type=float
    )

    args = argparser.parse_args()

    lti_launch_info = json.loads(args.lti_launch_info)
    consumer_key = os.environ['LTI_CONSUMER_KEY']
    consumer_secret = os.environ['LTI_CONSUMER_SECRET']

    await post_grade(
        lti_launch_info['lis_result_sourcedid'],
        lti_launch_info['lis_outcome_service_url'],
        consumer_key,
        consumer_secret,
        args.grade
    )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the commands
    loop.run_until_complete(main())
    loop.close()