class ChatUtil:
    def __init__(self):
        return
    
    def processText(self, chatText):
        textLines = chatText.split('\n')
        htmlText = '<br>'.join(textLines)

        return htmlText