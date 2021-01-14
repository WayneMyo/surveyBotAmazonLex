import pymysql #pip install PyMySQL
import sys
import base64
import dateutil.parser
import datetime
import time
import os
import logging

from helper import elicit_intent, elicit_slot, delegate_slot, confirm_intent, close, delegate, build_validation_result, build_response_card, try_ex

# a lambda function perform survey on user as well as to save responses to AWS RDS MySQL

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

now = datetime.datetime.now()
create_time = now.strftime("%Y-%m-%d %H:%M:%S")

REGION = 'ap-southeast-1c'

rds_host  = "dbinstancename.abcdefgh123.region.rds.amazonaws.com" #rds endpoint - can obtain from AWS RDS instance under Connectivity & security tab
name = "username" #rds instance username - can obtain from AWS RDS instance under Configuration tab
password = "###password###" #rds instance password
db_name = "dbname"

# function to save user responses to db
def save_to_db(companyName, businessNature, claimDealFrequency, claimType, userType, claimSystem, claimDuration, claimCount, paymentType, digitalPayment, beneficialScale, preferredInterface, userRequirements, costExpectations):
    """
    This function fetches content from mysql RDS instance
    """
    result = []
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO UserResponse (CompanyName, BusinessNature, ClaimDealFrequency, ClaimTypes, UserType, ClaimSystems, ClaimDuration, ClaimCount, PaymentType, DigitalPayment, BeneficialScale, PreferredInterface, UserRequirements, CostExpectations) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (companyName, businessNature, claimDealFrequency, claimType, userType, claimSystem, claimDuration, claimCount, paymentType, digitalPayment, beneficialScale, preferredInterface, userRequirements, costExpectations))
        cur.execute("""select * from UserResponse""")
        conn.commit()
        cur.close()
        for row in cur:
            result.append(list(row))
        print ("Data from claimQuick Survey RDS...")
        print (result)

# function to perform survey on user        
def start_survey(intent_request, confirmation):
    
    slots = intent_request["currentIntent"]["slots"]
    companyName = slots["company"]
    businessNature = slots["business_nature"]
    claimDealFrequency = slots["deal_with_claim"]
    claimType = slots["claim_types"]
    userType = slots["approver_claimant"]
    claimSystem = slots["claim_systems"]
    claimDuration = slots["claim_duration"]
    claimCount = slots["claim_count"]
    paymentType = slots["payment_type"]
    digitalPayment = slots["digital_payment"]
    beneficialScale = slots["beneficial"]
    preferredInterface = slots["prefered_interface"]
    userRequirements = slots["user_requirements"]
    costExpectations = slots["cost_expectations"]
    
    session_attributes = (
        intent_request["sessionAttributes"]
        if intent_request["sessionAttributes"] is not None
        else {}
    )

    source = intent_request["invocationSource"]

    save_to_db(companyName, businessNature, claimDealFrequency, claimType, userType, claimSystem, claimDuration, claimCount, paymentType, digitalPayment, beneficialScale, preferredInterface, userRequirements, costExpectations)
    
    return close(
        session_attributes,
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": "Thank you very much for participating in the survey. Have a nice day. Goodbye!"
        },
    )

# if answerSurvey intent is triggered, start start_survey function
def dispatch(intent_request, confirmation):

    logger.debug(
        "dispatch userId={}, intentName={}".format(
            intent_request["userId"], intent_request["currentIntent"]["name"]
        )
    )

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to your bot's intent handlers
    if intent_name == "answerSurvey":
        return start_survey(intent_request, confirmation)
    raise Exception("Intent with name " + intent_name + " not supported")


def lambda_handler(event, context):

    # Change time to Singapore Time
    os.environ["TZ"] = "Asia/Singapore"
    time.tzset()
    logger.debug("event.bot.name={}".format(event["bot"]["name"]))
    confirmation = event['currentIntent']["confirmationStatus"]
    
    return dispatch(event, confirmation)