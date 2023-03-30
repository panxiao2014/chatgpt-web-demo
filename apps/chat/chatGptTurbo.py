import openai
from flask import current_app as app
from apps.chat.fakeChat import FakeChat
from apps.chat.chatUtil import ChatUtil

f = open('apps/chat/openai_api_key.txt', 'r')
openai.api_key = f.read()

#use for debugging, so no api credit is spent
FAKE_CHAT = False
fakeChat = FakeChat()

#use model gpt-3.5-turbo:
MaxToken = 4096

chatUtil = ChatUtil()


def parseFinishReason(userConversations, currentUser, finishReason):
    if(finishReason == "stop"):
        return
    
    #conversation has exceeded maximum token allowed, need to re-init:
    if(finishReason == "length"):
        userConversations[currentUser] = [{"role": "system", "content": "You are a helpful assistant."}]
    
    app.logger.warning("%s's chat return with reason: %s" % (currentUser, finishReason))
    return


def parseTotalToken(userConversations, currentUser, totalToken):
    if(totalToken > (MaxToken - 40)):
        app.logger.warning("%s's total token reached %d, reset conversation" % (currentUser, totalToken))
        userConversations[currentUser] = [{"role": "system", "content": "You are a helpful assistant."}]

    return


userConversations = {}
def chatWithTurbo3(currentUser, chatConversation):
    global userConversations
    
    try:
        response  = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chatConversation,
            temperature=0.1,
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
        userConversations[currentUser] = []
        return ("我出错了，请你再试试"), 0, "response_error"
    
    try:
        totalToken = response['usage']['total_tokens']
        finishReason = response['choices'][0]['finish_reason']
    except Exception as e:
        app.logger.warning(e)
        return ("我出错了，请你再试试"), 0, "parse_result_error"

    return message, totalToken, finishReason


def chatResponseFromTurbo(currentUser, prompt):
    global userConversations

    if currentUser not in userConversations:
        userConversations[currentUser] = [{"role": "system", "content": "You are a helpful assistant."}]

    userConversations[currentUser].append({"role": "user", "content": prompt})

    if(FAKE_CHAT == False):
        botAnswer, totalToken, finishReason= chatWithTurbo3(currentUser,  userConversations[currentUser])
    else:
        botAnswer = fakeChat.giveAnswer()
    
    app.logger.info("Response to %s with total token %d: %s" % (currentUser, totalToken, botAnswer))

    userConversations[currentUser].append({"role": "assistant", "content": botAnswer})

    parseFinishReason(userConversations, currentUser, finishReason)
    parseTotalToken(userConversations, currentUser, totalToken)

    return botAnswer