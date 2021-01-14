# surveyBotAmazonLex
Survey bot created using Amazon Lex, AWS Lambda service, Twilio Messaging service &amp; WhatsApp

## Dependencies
- [AWS RDS - MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html)
- [pymysql](https://pypi.org/project/PyMySQL/)
- [Twilio Programmable Messaging](https://www.twilio.com/docs/api)

***Note: You can use local MySQL server as well - just change the DB endpoint inside answerSurveyFunction

## Deployment Packages
Total of 3 zip files involved:-
- claimQuickBot_3_Bot_LEX_V1.zip (To upload to Amazon Lex)
- triggerSurveyFunction.zip (To upload to AWS Lambda)
- answerSurveyFunction.zip (To upload to AWS Lambda)

## How to upload bot to Amazon Lex
- Go to AWS management console
- Go to Amazon Lex
- In the Bots tab, Actions > Import > Upload file & import

## How to upload functions to AWS Lambda
- Go to AWS management console
- Go to AWS Lambda
- Under Functions tab, Create function > define your function name > select Python 3.7 > Function code > Actions > Upload a .zip file > Upload & save
