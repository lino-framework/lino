# list of all cities and number of inhabitants
from lino.schemas.sprl import demo, Cities
sess=demo.startup()
qry=sess.query(Cities,"nation name inhabitants", orderBy="inhabitants")
sess.showQuery(qry,width=50)
