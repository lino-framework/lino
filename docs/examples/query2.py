# list of Belgian cities and number of inhabitants
from lino.schemas.sprl import demo, Cities, Nations

sess=demo.startup()
be=sess.query(Nations).peek("be")
qry=be.cities.query("name inhabitants", orderBy="inhabitants")

sess.showQuery(qry,width=50)
