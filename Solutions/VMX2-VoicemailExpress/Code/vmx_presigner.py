# Version: 2024.02.28
"""
**********************************************************************************************************************
 *  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved                                            *
 *                                                                                                                    *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated      *
 *  documentation files (the "Software"), to deal in the Software without restriction, including without limitation   *
 *  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and  *
 *  to permit persons to whom the Software is furnished to do so.                                                     *
 *                                                                                                                    *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO  *
 *  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    *
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF         *
 *  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS *
 *  IN THE SOFTWARE.                                                                                                  *
 **********************************************************************************************************************
"""
import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    logger.debug(event)

    # Establish an empty response
    response = {}
    # Set the default result to success
    response.update({'result': 'success'})

    # Generate the presigned URL and return
    try:
        s3_client = boto3.client('s3')

        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': event['recording_bucket'],
                'Key': event['recording_key']
            },
            ExpiresIn=int(os.environ['s3_obj_lifecycle']) * 86400
        )
        response.update({'presigned_url': presigned_url})

        return response

    except Exception as e:
        logger.error(e)
        response.update({'result': 'fail'})
        response.update({'detail': 'presigned URL generation failed'})
        logger.debug(response)
        return response