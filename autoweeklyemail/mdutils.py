def hyperlink(text, link=None):
    """
    Create a markdown-formatted hyperlink
    :param text: The text of the link
    :param link: (optional) The link that the text points to, if the text is not the link
    :return: A markdown-formatted hyperlink
    """
    ret = "[" + text + "]"

    if link is None:
        link = text

    ret += "(" + link + ")"
    return ret


def emailLink(address):
    """
    Create a markdown-formatted hyperlink to one's email
    :param address: The email address
    :return: Markdown-formatted hyperlink string
    """
    ret = "[" + address + "]"

    ret += "(mailto:" + address + ")"
    return ret


def b(text):
    return "**" + text + "**"