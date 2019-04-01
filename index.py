def handler(event, context):
	import praw
	from datetime import datetime
	currentTime = datetime.now().strftime("%m-%d-%Y")
	import boto3
	from botocore.exceptions import ClientError
	BODY_HTML = "<html><head></head><body>"
	BODY_TEXT = ""
	reddit = praw.Reddit(client_id='###', client_secret="###",
		user_agent='trendscript')

	print("----PYTHON TRAFFIC----")
	for subreddit in reddit.subreddits.new(limit=1025):
		if subreddit.subscribers > 98:
			BODY_HTML += "\n<b>{}</b> Subscribers: {}\nhttps://www.reddit.com{}\n".format(subreddit.title, subreddit.subscribers, subreddit.url)
			BODY_TEXT += "{} {} \r\nhttps://www.reddit.com{}".format(subreddit.title, subreddit.subscribers, subreddit.url)
	

	"""

                Be mindful I originally set this up as an Amazon Lambda function,
		so you can change a few things to just make it email you direct.
		
		Lambda takes a handler with args, so just remove that top line
		and the function should work through command line.

		Also, you'll need to use your own clid and clisecret.

		Happy hacking!

	"""

	# Replace sender@example.com with your "From" address.
	# This address must be verified with Amazon SES.
	SENDER = "###"

	# Replace recipient@example.com with a "To" address. If your account 
	# is still in the sandbox, this address must be verified.
	RECIPIENT = "###"

	# Specify a configuration set. If you do not want to use a configuration
	# set, comment the following variable, and the 
	# ConfigurationSetName=CONFIGURATION_SET argument below.
	CONFIGURATION_SET = "ConfigSet"

	# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
	AWS_REGION = "us-west-2"

	# The subject line for the email.
	SUBJECT = "Trending Subreddits for {}".format(currentTime)        

	BODY_HTML += "</body></html>"
	# The character encoding for the email.
	CHARSET = "UTF-8"

	# Create a new SES resource and specify a region.
	client = boto3.client('ses',region_name=AWS_REGION)

	# Try to send the email.
	try:
	    #Provide the contents of the email.
	    response = client.send_email(
	        Destination={
	            'ToAddresses': [
	                RECIPIENT,
	            ],
	        },
	        Message={
	            'Body': {
	                'Html': {
	                    'Charset': CHARSET,
	                    'Data': BODY_HTML,
	                },
	                'Text': {
	                    'Charset': CHARSET,
	                    'Data': BODY_TEXT,
	                },
	            },
	            'Subject': {
	                'Charset': CHARSET,
	                'Data': SUBJECT,
	            },
	        },
	        Source=SENDER,
	        # If you are not using a configuration set, comment or delete the
	        # following line
	        ConfigurationSetName=CONFIGURATION_SET,
	    )
	# Display an error if something goes wrong.	
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		print("Email sent! Message ID:"),
		print(response['ResponseMetadata']['RequestId'])
