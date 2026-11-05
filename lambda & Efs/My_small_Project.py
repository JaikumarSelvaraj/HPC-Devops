		AWS Lambda

Serverless

Example -> Zomato -> 

Programming model
 Handler
 Context
 Event
 Logging
 Exception


Using ChatGpt Do Small Project
---------------------------------------------------------------------------------------------------------------------
1)AWS Lambda how to create schedule based event give small project in onepage

Create Lambda Function
- AWS Console → Lambda → Create function.
- Function name: Scheduled-Lambda
- Runtime: Python 3.x
- Create a new execution role with basic Lambda permissions.

Code
import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info("Scheduled Lambda Started")

    current_time = datetime.now(timezone.utc)

    print("Hello! Lambda executed automatically")
    print("Execution Time:", current_time)

    return {
        "status": "Success",
        "message": "Scheduled task completed"
    }

Create Schedule using EventBridge
- AWS Console → Lambda -> Scheduler
- Select Scheduler → Create schedule.
- Schedule name: Every-5-Minutes
- Schedule pattern: Recurring schedule.
- Schedule type: Rate-based.
- Rate expression: rate(5 minutes).
- Target: AWS Lambda Invoke.
- Select function: Scheduled-Lambda.
- Configure execution role permissions to invoke Lambda.
- Create schedule.


Verify Execution
- Wait for the next scheduled execution.
- Go to Lambda → Monitor → View CloudWatch Logs.
- Check the execution messages.

Note: I am unable to see log on the Lambda -> Monitoring page, However we can see this details in 

Cloudwatch -> Logmanagement -> Lambdafuntion name
---------------------------------------------------------------------------------------------------------------------
Chatgpt : Lamda Auto Trigger feautres create small project

Create S3 Bucket
1. Open AWS S3.
2. Create bucket: my-lambda-trigger-demo.
3. Keep default settings.
4. Create bucket.


Create Lambda Function
1. Open AWS Lambda → Create function.
2. Function name: S3-Auto-Trigger.
3. Runtime: Python 3.x.
4. Create function.

Code 

def lambda_handler(event, context):

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        filename = record['s3']['object']['key']

        print("Bucket:", bucket)
        print("Uploaded File:", filename)

    return "File processed successfully"

Configure Automatic Trigger
1. Open your Lambda function.
2. Select Add trigger.
3. Select source: S3.
4. Select bucket: my-lambda-trigger-demo.
5. Event type: All object create events.
6. Acknowledge recursive invocation warning if displayed.
7. Click Add.

Test the Project
Upload a file named test.txt into your S3 bucket.

Expected CloudWatch output:
Bucket: my-lambda-trigger-demo

Uploaded File: test.txt

Verify Execution
Cloudwatch -> Logmanagement -> Lambdafuntion name


role
---------------------------------------------------------------------------------------------------------------------
