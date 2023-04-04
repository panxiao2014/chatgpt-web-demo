import openai
from flask import current_app as app
from apps.chat.fakeChat import FakeChat

f = open('apps/chat/openai_api_key.txt', 'r')
openai.api_key = f.read()

#use for debugging, so no api credit is spent
FAKE_CHAT = False
fakeChat = FakeChat()

#use model text-davinci-003:
MaxToken = 4096
userConversations = {}
def chatWithDavinci3(currentUser, prompt):
    global userConversations
    
    try:
        completions = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=None
        )
    except Exception as e:
        app.logger.warning(e)
        userConversations[currentUser] = ""
        return ("我出错了，请你再试试")
    
    message = completions.choices[0].text
    message = message.strip()
    return message


def chatResponseFromDavinci(currentUser, prompt):
    global userConversations

    if currentUser not in userConversations:
        userConversations[currentUser] = ""

    if(len(userConversations[currentUser]) >= MaxToken):
        userConversations[currentUser] = ""

    userConversations[currentUser] = userConversations[currentUser] + "User: " + prompt

    if(FAKE_CHAT == False):
        botAnswer = chatWithDavinci3(currentUser,  userConversations[currentUser])
    else:
        botAnswer = fakeChat.giveAnswer()
    
    app.logger.info("Response to %s" % (currentUser))

    userConversations[currentUser] += botAnswer
    return botAnswer