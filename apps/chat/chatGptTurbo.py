import openai
from flask import current_app as app
from apps.chat.fakeChat import FakeChat
from apps.chat.chatUtil import ChatUtil

f = open('apps/configs/openai_api_key.txt', 'r')
openai.api_key = f.read()

#use for debugging, so no api credit is spent
FAKE_CHAT = False
fakeChat = FakeChat()

#error message to fonrt user when something gose wrong:
ErrMsg = "我出错了，您再重新试试？"

#use model gpt-3.5-turbo:
MaxToken = 4096
TokenMargin = 100

chatUtil = ChatUtil()

#reset user's conversation:
def resetConversation(userConversations, currentUser):
    userConversations[currentUser] = [{"role": "system", "content": "You are a helpful assistant."}]
    return


def parseFinishReason(userConversations, currentUser, finishReason):
    if(finishReason == "stop"):
        return
    
    #conversation has exceeded maximum token allowed, need to re-init:
    if(finishReason == "length"):
        #restConversation(userConversations, currentUser)
        pass
    
    app.logger.warning("%s's chat return with reason: %s" % (currentUser, finishReason))
    return


def parseTotalToken(userConversations, currentUser, totalToken):
    if(totalToken > (MaxToken - TokenMargin)):
        app.logger.warning("%s's total token reached %d, reset conversation" % (currentUser, totalToken))
        resetConversation(userConversations, currentUser)

    return


userConversations = {}
def chatWithTurbo3(currentUser, chatConversation):
    global userConversations
    
    try:
        response  = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chatConversation,
            temperature=0.2,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=None
        )

        message = response['choices'][0]['message']['content']
        message = message.strip()
        message = chatUtil.processText(message)
    except Exception as e:
        app.logger.warning(e)
        resetConversation(userConversations, currentUser)
        return ErrMsg, 0, "response_error"
    
    try:
        totalToken = response['usage']['total_tokens']
        finishReason = response['choices'][0]['finish_reason']
    except Exception as e:
        app.logger.warning(e)
        resetConversation(userConversations, currentUser)
        return ErrMsg, 0, "parse_result_error"

    return message, totalToken, finishReason


def chatResponseFromTurbo(currentUser, prompt):
    global userConversations

    #app.logger.info("User %s Encrypted prompt %s" % (currentUser, prompt))

    if currentUser not in userConversations:
        resetConversation(userConversations, currentUser)

    userConversations[currentUser].append({"role": "user", "content": prompt})

    if(FAKE_CHAT == False):
        botAnswer, totalToken, finishReason= chatWithTurbo3(currentUser,  userConversations[currentUser])
    else:
        botAnswer = fakeChat.giveAnswer()
        totalToken = 0
        finishReason = "stop"
    
    app.logger.info("Response to %s with total token %d" % (currentUser, totalToken))

    #we got a good response:
    if(finishReason == "stop"):
        userConversations[currentUser].append({"role": "assistant", "content": botAnswer})

    parseFinishReason(userConversations, currentUser, finishReason)
    parseTotalToken(userConversations, currentUser, totalToken)

    return botAnswer