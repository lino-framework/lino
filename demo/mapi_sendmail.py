from forum import simplemapi

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
