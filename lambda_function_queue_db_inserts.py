import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
  # Get the ContactId from the event object
  contact_id = event['Details']['ContactData']['ContactId']

  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('CallsInQueueQualicenter')

  # Get current timestamp
  current_time = datetime.now().isoformat()  

  # Check if the contact ID already exists in the DynamoDB table
  response = table.get_item(
      Key={
          'ContactID': contact_id
      }
  )

  if 'Item' in response:
      # Update the item if it exists
      table.update_item(
          Key={
              'ContactID': contact_id
          },
          UpdateExpression='SET InQueue = :val',
          ExpressionAttributeValues={
              ':val': False
          }
      )
  else:
      # Insert a new item if it doesn't exist
      table.put_item(
          Item={
              'ContactID': contact_id,
              'InQueue': True,
              'CurrentTime': current_time  # Add CurrentTime with timestamp
          }
      )

  return {
      'statusCode': 200,
      'body': 'Success'
  }
