#!/usr/bin/env python

import os
import sys
import time
import boto3

sqs = boto3.resource('sqs')

channel = os.environ['IRC_CHANNEL']
if channel[0] != '#':
    channel = '#' + channel

queue = sqs.get_queue_by_name(QueueName=os.environ.get('QUEUE_NAME', 'errbot-facultybot.fifo'))


def send_message(message):

    if os.environ.get('CODEBUILD_BUILD_ID'):
        build_name, build_id = os.environ.get('CODEBUILD_BUILD_ID').split(':', 1)
        short_build_id = "{}:{}".format(build_name, build_id.split('-', 1)[0])
        message = "build({}) ".format(short_build_id) + message

    queue.send_message(
        MessageAttributes={
            'channel': {
                'StringValue': channel,
                'DataType': 'String'
            }
        },
        MessageBody=message,
        MessageGroupId=str(time.time())
    )

if __name__ == '__main__':
    # called from command line
    message = " ".join(sys.argv[1:])
    send_message(message)
