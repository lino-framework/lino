from lino.schemas.sprl import demo, Currencies

sess=demo.startup(langs="en de fr")

q1=sess.query(Currencies)
q1.report()

sess.setBabelLang("de")
q1.report()

sess.setBabelLang("fr")
q1.report()

sess.setBabelLang("en fr de")
q1.report()

