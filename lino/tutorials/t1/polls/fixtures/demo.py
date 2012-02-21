from lino import dd

Poll = dd.resolve_model('polls.Poll')
Choice = dd.resolve_model('polls.Choice')

DATA = """
What is your preferred colour? | Blue | Red | Yellow | other
Do you like Django? | Yes | No | Not yet decided
"""

def objects():
    for ln in DATA.splitlines():
        if ln:
            a = ln.split('|')
            p = Poll(question=a[0].strip())
            yield p
            for choice in a[1:]:
                yield Choice(choice=choice.strip(),poll=p)