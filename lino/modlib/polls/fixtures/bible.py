# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.conf import settings
from lino.api import rt
from lino.utils import Cycler


def objects():

    polls = rt.modules.polls

    one = polls.ChoiceSet.objects.get(name="-1..+1")

    USERS = Cycler(settings.SITE.user_model.objects.all())

    def poll(choiceset, title, details, questions):
        return polls.Poll(
            user=USERS.pop(),
            title=title.strip(),
            details=details.strip(),
            state=polls.PollStates.published,
            questions_to_add=questions,
            default_choiceset=choiceset)

    yield poll(one, "Matthew 1:1-17", """
Please give your vote and optional remark for each verse.
""", """
The Good News According to Matthew

The Birth, Parentage and Infancy

[1:1] A genealogy of Jesus Christ, a descendant of David and Abraham. 
[1:2] Abraham was the father of Isaac, Isaac of Jacob, Jacob of Judah and his brothers, 
[1:3] Judah of Perez and Zerah, whose mother was Tamar, Perez of Hezron, Hezron of Ram, 
[1:4] Ram of Amminadab, Amminadab of Nashon, Nashon of Salmon, 
[1:5] Salmon of Boaz, whose mother was Rahab, Boaz of Obed, whose mother was Ruth, Obed of Jesse, 
[1:6] Jesse of David the King. David was the father of Solomon, whose mother was Uriah’s widow, 
[1:7] Solomon of Rehoboam, Rehoboam of Abijah, Abijah of Asa, 
[1:8] Asa of Jehoshaphat, Jehoshaphat of Jehoram, Jehoram of Uzziah, 
[1:9] Uzziah of Jotham, Jotham of Ahaz, Ahaz of Hezekiah, 
[1:10] Hezekiah of Manasseh, Manasseh of Ammon, Ammon of Josiah, 
[1:11] Josiah of Jeconiah and his brothers, at the time of the Exile to Babylon. 
[1:12] After the Exile to Babylon — Jeconiah was the father of Shealtiel, Shealtiel of Zerubbabel, 
[1:13] Zerubbabel of Abiud, Abiud of Eliakim, Eliakim of Azor, 
[1:14] Azor of Zadok, Zadok of Achim, Achim of Eliud, 
[1:15] Eliud of Eleazar, Eleazar of Matthan, Matthan of Jacob, 
[1:16] Jacob of Joseph, the husband of Mary, who was the mother of Jesus, who is called ‘Christ’. 
[1:17] So the whole number of generations from Abraham to David is fourteen; from David to the Exile to Babylon fourteen; and from the Exile to Babylon to the Christ fourteen.
    
""")

    yield poll(one, "Matthew 1:17-25", """
Please give your vote and optional remark for each verse.
""", """
[1:18] This is how Jesus Christ was born: 
His mother Mary was engaged to Joseph, but, before the marriage took place, she found herself to be pregnant by the power of the Holy Spirit. 
[1:19] Her husband, Joseph, was a religious man and, since he did not want to disgrace her publicly, he resolved to put an end to their engagement privately. 
[1:20] He had been thinking this over, when an angel of the Lord appeared to him in a dream.
“Joseph, son of David,” the angel said, “do not be afraid to take Mary for your wife, for her child has been conceived by the power of the Holy Spirit. 
[1:21] She will give birth to a son; name him Jesus, for he will save his people from their sins.”

[1:22] All this happened in fulfillment of these words of the Lord in the prophet, where he says —

[1:23] ‘The virgin will conceive and will give birth to a son, and they will give him the name Immanuel’
— a word which means ‘God is with us.’ 
[1:24] When Joseph woke up, he did as the angel of the Lord had directed him. 
[1:25] He made Mary his wife, but they did not sleep together before the birth of her son; and to this son he gave the name Jesus.
""")

    for p in polls.Poll.objects.exclude(questions_to_add=''):
        p.after_ui_save(None, None)
        #~ p.save()

    yield polls.Response(poll=p, user=USERS.pop())
