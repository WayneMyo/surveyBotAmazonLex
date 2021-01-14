import base64
import dateutil.parser
import datetime
import time
import os
import logging

from helper import elicit_intent, elicit_slot, delegate_slot, confirm_intent, close, delegate, build_validation_result, build_response_card, try_ex

# main lambda function that will introduce the user on the survey upon user saying hi/hello etc. to the bot fulfilling surveyIntro intent from claimQuick bot

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

now = datetime.datetime.now()
create_time = now.strftime("%Y-%m-%d %H:%M:%S")

# after user confirmed that he/she wants to take part in a survey, start answerSurvey intent and ask the company user is from
def ask_company(intent_request, confirmation):
    
    slots = intent_request["currentIntent"]["slots"]
    
    session_attributes = (
        intent_request["sessionAttributes"]
        if intent_request["sessionAttributes"] is not None
        else {}
    )

    source = intent_request["invocationSource"]
    
    return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ElicitSlot",
                "intentName": "answerSurvey", #calling answerSurvey intent
                "slots": slots,
                "slotToElicit": "company", #start 1st slot of answerSurvey intent
                "message": {
                    "contentType": "PlainText",
                    "content": "Would you please indicate the name of your company? (Please add the city your company HQ is residing as a surfix to the answer i.e. ABC Singapore)"
                }
            },
        }

# if user utterance triggers surveyIntro intent, start ask_company function
def dispatch(intent_request, confirmation):

    logger.debug(
        "dispatch userId={}, intentName={}".format(
            intent_request["userId"], intent_request["currentIntent"]["name"]
        )
    )

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to your bot's intent handlers
    if intent_name == "surveyIntro":
        return ask_company(intent_request, confirmation)
    raise Exception("Intent with name " + intent_name + " not supported")


def lambda_handler(event, context):

    # Change time to Singapore Time
    os.environ["TZ"] = "Asia/Singapore"
    time.tzset()
    logger.debug("event.bot.name={}".format(event["bot"]["name"]))
    confirmation = event['currentIntent']["confirmationStatus"]
    
    return dispatch(event, confirmation)