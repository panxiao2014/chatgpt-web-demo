import random

RandomRsp = ["Fear is the mind-killer. Fear is the little-death that brings total obliteration. I will face my fear. I will permit it to pass over me and through me. And when it has gone past I will turn the inner eye to see its path. Where the fear has gone there will be nothing. Only I will remain.",
             "是的，可以使用gunicorn的--timeout参数来忽略worker timeout",
             "这段话出自著名科幻小说《沙丘》，作者是萨芬·艾克哈特"
             "熊猫的故乡是中国",
             "Some wikis have an edit button or link directly on the page being viewed if the user has permission to edit the page. This can lead to a text-based editing page where participants can structure and format wiki pages with a simplified markup language, sometimes known as wikitext, wiki markup or wikicode (it can also lead to a WYSIWYG editing page; see the paragraph after the table below). For example, starting lines of text with asterisks could create a bulleted list. The style and syntax of wikitexts can vary greatly among wiki implementations,[example needed] some of which also allow HTML tags"]

class FakeChat:
    def __init__(self):
        return

    def giveAnswer(self):
        return "(Fake) " + random.choice(RandomRsp)
