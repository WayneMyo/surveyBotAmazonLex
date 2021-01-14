""" --- Helper Functions (Elicit intent, elicit slot etc.) --- """

def elicit_intent(session_attributes, message):
    return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": "PlainText",
                    "content": message
                }
            },
        }

def elicit_slot(
    session_attributes, intent_name, slots, slot_to_elicit, message, response_card=None
):
    if response_card:
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ElicitSlot",
                "intentName": intent_name,
                "slots": slots,
                "slotToElicit": slot_to_elicit,
                "message": message,
                "responseCard": response_card,
            },
        }
    else:
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ElicitSlot",
                "intentName": intent_name,
                "slots": slots,
                "slotToElicit": slot_to_elicit,
                "message": message,
            },
        }
        

def delegate_slot(slots, sessionAttributes, completed):
    output_session_attributes = sessionAttributes
    output_session_attributes["Completed"] = completed
    
    response = {
        "sessionAttributes": output_session_attributes,
        "dialogAction": {
            "type": "Delegate",
            "slots": slots
        }
    }
    return response


def confirm_intent(session_attributes, intent_name, slots, message, confirmation):
    if(confirmation == "None"):
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "ConfirmIntent",
                "intentName": intent_name,
                "slots": slots,
                "message": message
            }
            
        }
        
    elif((confirmation == "Denied")):
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "PlainText",
                    "content": "Okay, your request will not proceed."
                }
            }
            
        }
        
    else:
        return delegate_slot(slots, session_attributes, "confirmed")
    
    
def close(session_attributes, fulfillment_state, message, response_card=None):
    if response_card:
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": fulfillment_state,
                "message": message,
                "responseCard": response_card,
            },
        }
    else:
        return {
            "sessionAttributes": session_attributes,
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": fulfillment_state,
                "message": message,
            },
        }


def delegate(session_attributes, slots):
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }

def build_validation_result(is_valid, outputDialogMode, violated_slot, message_content):
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}
        
    else:
        if outputDialogMode=="VOICE":
            return {
                "isValid": is_valid,
                "violatedSlot": violated_slot,
                "message": {"contentType": "SSML", "content": message_content},
            }
        else:
            return {
                "isValid": is_valid,
                "violatedSlot": violated_slot,
                "message": {"contentType": "PlainText", "content": message_content},
            }

def build_response_card(title, subtitle, options):
    buttons = None

    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        "contentType": "application/vnd.amazonaws.card.generic",
        "version": 1,
        "genericAttachments": [
            {"title": title, "subTitle": subtitle, "buttons": buttons}
        ],
    }
    

def try_ex(func):
    try:
        return func()
    except KeyError:
        return None
