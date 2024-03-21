# Version: 2024.02.28
"""
**********************************************************************************************************************
 *  Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved                                            *
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
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'DEBUG')))

def lambda_handler(event, context):
    logger.debug(": %s",event)

    # Grab incoming data elements from the S3 event
    try:
        recording_key = event['detail']['object']['key']
        logger.debug('Record Result: Recording Key: %s', recording_key)
        recording_name = recording_key.replace('voicemail_recordings/','')
        logger.debug('Record Result: Recording Name: %s', recording_name)
        contact_id = recording_name.replace('.wav','')
        logger.debug('Record Result: Contact ID: %s', contact_id)
        recording_bucket = event['detail']['bucket']['name']
        logger.debug('Record Result: Recording Bucket: %s', recording_bucket)
        recording_region = event['region']
        logger.debug('Record Result: Recording Region: %s', recording_region)
    except Exception as e:
        logger.error(e)
        logger.debug('Record Result: Failed to extract data from event')
        return {'result':'Failed to extract data from event'}

    # Establish the S3 client and get the object tags
    try:
        s3_client = boto3.client('s3')
        object_data = s3_client.get_object_tagging(
            Bucket=recording_bucket,
            Key=recording_key
        )
        logger.debug('Record Result: Object Data: %s', object_data)

        object_tags = object_data['TagSet']
        logger.debug('Record Result: Object Tags: %s', object_tags)
        loaded_tags = {}

        for i in object_tags:
            loaded_tags.update({i['Key']:i['Value']})
            logger.debug('Record Result: Loaded tags: %s', loaded_tags)

    except Exception as e:
        logger.error(e)
        logger.debug('Record Result: Failed to extract tags from object')
        return {'result':'Failed to extract tags from object'}

    # Build the Recording URL
    try:
        recording_url = 'https://{0}.s3-{1}.amazonaws.com/{2}'.format(recording_bucket, recording_region, recording_key)
        logger.debug('Record Result: Recording URL: %s', recording_url)

    except Exception as e:
        logger.error(e)
        logger.debug('Record Result: Failed to generate recording URL')
        return {'result':'Failed to generate recording URL'}

    # Do the transcription
    try:
        # Esteablish the client
        transcribe_client = boto3.client('transcribe')
        logger.debug('Record Result: LanguageCode: %s', loaded_tags['vmx_lang'])
        # Submit the transcription job
        transcribe_response = transcribe_client.start_transcription_job(
            TranscriptionJobName=contact_id,
            LanguageCode=loaded_tags['vmx_lang'],
            MediaFormat='wav',
            Media={
                'MediaFileUri': recording_url
            },
            OutputBucketName=os.environ['s3_transcripts_bucket']
        )
        logger.debug('Record Result: Transcription Response: %s', transcribe_response)

    except Exception as e:
        logger.error(e)
        logger.debug('Record Result: Transcription job failed')
        return {'result':'Transcription job failed'}

    logger.debug('Record Result: Success!')

    return {
        'status': 'complete',
        'result': 'record processed'
    }
