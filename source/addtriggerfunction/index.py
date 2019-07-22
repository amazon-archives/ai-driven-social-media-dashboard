from __future__ import print_function
import json
import boto3
import time
import os
from botocore.vendored import requests

def sendResponseCfn(event, context, responseStatus):
    response_body = {'Status': responseStatus,
                     'Reason': 'Log stream name: ' + context.log_stream_name,
                     'PhysicalResourceId': context.log_stream_name,
                     'StackId': event['StackId'],
                     'RequestId': event['RequestId'],
                     'LogicalResourceId': event['LogicalResourceId'],
                     'Data': json.loads("{}")}

    requests.put(event['ResponseURL'], data=json.dumps(response_body))

def lambda_handler(event, context):
  print(json.dumps(event))
  if event["RequestType"] == "Create":
      print("RequestType %s, nothing to do" % event["RequestType"])
      
      function_name = os.environ['lambda_arn']
      s3_bucket = os.environ['s3_bucket']
      
      response = boto3.client('lambda').add_permission(
          FunctionName=function_name,
          StatementId='S3callingLambdaForSocialMedia',
          Action='lambda:InvokeFunction',
          Principal='s3.amazonaws.com',
          SourceArn='arn:aws:s3:::' + s3_bucket,
          SourceAccount=os.environ['account_number']
      )


      response = boto3.client('s3').put_bucket_notification_configuration(
                          Bucket=s3_bucket,
                          NotificationConfiguration={
                                      'LambdaFunctionConfigurations': [
                                          {
                                              'Id': 'TriggerRawProcessing',
                                              'LambdaFunctionArn': function_name,
                                              'Events': [
                                                  's3:ObjectCreated:*'
                                              ],
                                              'Filter': {
                                                  'Key': {
                                                      'FilterRules': [
                                                          {
                                                              'Name': 'prefix',
                                                              'Value': 'raw/'
                                                          },
                                                      ]
                                                  }
                                              }
                                          },
                                      ]
                                  }
                              )
  else:
      print("RequestType %s, nothing to do" % event["RequestType"])

  sendResponseCfn(event, context, "SUCCESS")
