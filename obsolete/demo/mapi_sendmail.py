from forum import simplemapi

"""
Another application is attempting to send mail using your user profile. Are you sure you wxant to send mail?

Warn me whenever other applications try to send mail from me.

"""

simplemapi.SendMail(
    "Luc Saffre <luc.saffre@gmx.net>",
    "My Subject",
    """
My message body

blabla.
blablabla.
blabla.
blablabla.
blabla.
blablabla.
""","")
