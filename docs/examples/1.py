# list of all cities and number of inhabitants
from lino.schemas.sprl import demo, Cities
sess=demo.startup()

q1=sess.query(Cities,"nation name inhabitants",
              orderBy="inhabitants")
q1.report(width=50)
