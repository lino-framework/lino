from lino.forms import web
from lino.apps.keeper.keeper import Keeper
app=Keeper()
app.quickStartup()
web.run(app)
