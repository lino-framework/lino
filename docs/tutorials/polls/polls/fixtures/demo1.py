from polls.models import Poll, Choice


def objects():
    p = Poll(question="What is your preferred colour?")
    yield p
    yield Choice(choice="Blue", poll=p)
    yield Choice(choice="Red", poll=p)
    yield Choice(choice="Yellow", poll=p)
    yield Choice(choice="other", poll=p)

    p = Poll(question="Do you like Django?")
    yield p
    yield Choice(choice="Yes", poll=p)
    yield Choice(choice="No", poll=p)
    yield Choice(choice="Not yet decided", poll=p)
