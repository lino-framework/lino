#coding: latin1
#---------------------------------------------------------------------
# $Id: webcal.py,v 1.3 2004/07/31 07:13:46 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

raise "no longer used. replaced by tls package"

from time import localtime, time
from lino.misc.normalDate import ND
from twisted_ui import TwistedRenderer,AdamoResource
from skipper import Skipper
from widgets import Widget



weekdays = ( 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
				 'Saturday', 'Sunday')

months = ( 'January', 'February', 'March', 'April', 'May', 'June',
	'July', 'August', 'September', 'October', 'November', 'December')


class DayWidget(Widget):
	def __init__(self,day):
		self.day = day

	def getLabel(self):
		s = self.day.dayOfWeekName() + ', %d. %s %d' % (
			self.day.day(), self.day.monthName(), self.day.year())
		return s

	def asPreTitle(self,renderer):
		rsc = renderer.resource
		s = months[self.day.month()-1]
		s += " " + str(self.day.year())
		renderer.renderLink(renderer.uriToSelf(self.day.year(),
															self.day.month()), s)
	def asLeftMargin(self,renderer):
		renderer.write('<p>')
		today = ND()
		renderer.renderLink(renderer.uriToSelf(today.year(),
															today.month(),
															today.day()),
								  label='today')
		renderer.write('<p>')
		renderer.resource.db.asLeftMargin(renderer)

		

	def asBody(self,renderer):
		year = self.day.year()
		month = self.day.month()
		day = self.day
		wr = renderer.write
		rsc = renderer.resource
		
		wr('<br>day:')
		d = day - 1
		renderer.renderLink(url=renderer.uriToSelf(d.year(),
															d.month(),
															d.day()),
								  label='<<')
		wr(' ')
		d = day + 1
		renderer.renderLink(url=renderer.uriToSelf(d.year(),
															d.month(),
															d.day()),
								  label='>>')

		
		ds = rsc.db.EVENTS.query(date=day)
		wr('<p>Events: ')
		ds.asParagraph(renderer)
 		#skipper = Skipper(ds,pageLen=10)
		#skipper.asBody(renderer)
		
## 		# skipper.asLabel(renderer)
##  		renderer.renderLink(
##  			url=renderer.uriToSkipper(skipper),
##  			label='(%d events)' % len(ds))
		



class MonthWidget(Widget):
	def __init__(self,year,month):
		self.year = year
		self.month = month
	
	def getLabel(self):
		s = months[self.month-1]
		s += " " + str(self.year)
		return s
	
	def asPreTitle(self,renderer):
		renderer.renderLink(renderer.uriToSelf(self.year),
								  str(self.year))
	def asLeftMargin(self,renderer):
		renderer.write('<p>')
		today = ND()
		renderer.renderLink(renderer.uriToSelf(),
								  label='current month')
		renderer.write('<p>')
		renderer.resource.db.asLeftMargin(renderer)

	def asBody(self,renderer):

		today = ND()
		
		wr = renderer.write
		
		year = self.year
		month = self.month

		wr('<br>year:')
		renderer.renderLink(renderer.uriToSelf(year-1,month),str(year-1))
		wr(' ')
		renderer.renderLink(renderer.uriToSelf(year+1,month),str(year+1))
		wr('<br>month:')
		renderer.renderLink(renderer.uriToSelf(year,month-1),'<<')
		wr(' ')
		renderer.renderLink(renderer.uriToSelf(year,month+1),'>>')
		
		day = ND((year,month,1))
		week = day.weekOfYear()
		
		#(year,week,isoday) = day.iso_week
		#(firstWeekDay,numDays) = calendar.monthrange(year, month)

		#while day.iso_week[1] == week:
		while day.weekOfYear() == week:
			day -= 1
			
		day += 1

		wr(str(day))
		
		wr('<table border=1>')
		wr('<tr>')
		wr('<td>week</td>')
		for wd in weekdays:
			wr('<td>%s</td>' % wd)
		wr('</tr>')
		
		while True:
			wr('<tr>')
			wr('<td>')
			wr(str(week))
			wr('</td>')
			for col in range(7):
				if day == today:
					wr('<td bgcolor="red">')
				elif day.month() == self.month:
					wr('<td bgcolor="white">')
				else:
					wr('<td bgcolor="gold">')
				self.writeDayInMonth(renderer,day)
				day += 1
				wr('</td>')
			wr('</tr>')
			week += 1
			if day.month() > month:
				break
		
		wr('</table>')
		
	def writeDayInMonth(self,renderer,day):
		rsc = renderer.resource
		renderer.write('<p align="center">')
		renderer.renderLink(url=renderer.uriToSelf(day.year(),
																 day.month(),
																 day.day()),
								  label=str(day.day()))
		renderer.write('</p>')
		

		ds = renderer.resource.db.EVENTS.query(date=day)
		renderer.renderLink(
			url=renderer.uriToDatasource(ds),
			label='(%d events)' % len(ds))


		
class YearWidget(Widget):

	def __init__(self,year):
		self.year = year

	def getLabel(self):
		return str(self.year)
	
	def asLeftMargin(self,renderer):
		renderer.write('<p>')
		today = ND()
		renderer.renderLink(renderer.uriToSelf(),
								  label='current month')
		renderer.write('<p>')
		renderer.resource.db.asLeftMargin(renderer)

	def asBody(self,renderer):
		year = self.year
		wr = renderer.write
		rsc = renderer.resource
		
		wr('<br>year:')
		renderer.renderLink(url=renderer.uriToSelf(year-1),
								  label='<<')
		wr(' ')
		renderer.renderLink(url=renderer.uriToSelf(year+1),
								  label='>>')

		
		ds = rsc.db.EVENTS.query()
		ds.setFilter("date between %d0101 and %d1231" % (year,year))
		wr('<p>Events: ')
		ds.asParagraph(renderer)

		
## 		skipper = Skipper(ds,None)
## 		# skipper.asLabel(renderer)
## 		renderer.renderLink(
## 			url=renderer.uriToSkipper(skipper),
## 			label='(%d events)' % len(ds))

		
## class CalendarRenderer(Widget,TwistedRenderer):
## 	def __init__(self,rsc,request):
## 		TwistedRenderer. __init__(self,rsc,request)
## 		if len(request.postpath) == 0 :
## 			self.year = localtime(time())[0]
## 		else:
## 			self.year = int(request.postpath[0])
## 		if len(request.postpath) > 1 :
## 			self.month = int(request.postpath[1])
## 		else:
## 			self.month = localtime(time())[1] 
## 		if len(request.postpath) > 2 :
## 			self.day = int(request.postpath[2])
## 			self.day = ND((self.year,self.month,self.day))
## 		else:
## 			self.day = None
					

## 	def getLabel(self):
## 		if self.day is None:
## 			s = months[self.month-1]
## 			s += " " + str(self.year)
## 		else:
## 			day = self.day
## 			s = day.dayOfWeekName() + ', %d. %s %d' % (
## 				day.day(), day.monthName(), day.year())
## 		return s

			
## 	def asBody(self,renderer):
## 		if self.day is None:
## 			self.asMonth(renderer)
## 		else:
## 			self.asDay(renderer)

## 	def asPreTitle(self,renderer):
## 		if self.day is not None:
## 			s = months[self.month-1]
## 			s += " " + str(self.year)
## 			renderer.renderLink(renderer.uriToSelf(self.year,
## 																self.month), s)
		

## 	def asDay(self,renderer):
## 		year = self.year
## 		month = self.month
## 		day = self.day
## 		wr = renderer.write
		
## 		wr('<br>day:')
## 		d = day - 1
## 		renderer.renderLink(url=self.uriToSelf(d.year(),
## 															d.month(),
## 															d.day()),
## 								  label='<<')
## 		wr(' ')
## 		d = day + 1
## 		renderer.renderLink(url=self.uriToSelf(d.year(),
## 															d.month(),
## 															d.day()),
## 								  label='>>')
		
## 		ds = self.resource.db.EVENTS.query(date=day)
##  		skipper = Skipper(ds,pageLen=10)
## 		skipper.asBody(renderer)
		
## ## 		# skipper.asLabel(renderer)
## ##  		renderer.renderLink(
## ##  			url=renderer.uriToSkipper(skipper),
## ##  			label='(%d events)' % len(ds))
		
## 	def asMonth(self,renderer):

## 		today = ND()
		
## 		wr = renderer.write
		
## 		year = self.year
## 		month = self.month

## 		wr('<br>year:')
## 		renderer.renderLink(self.uriToSelf(year-1,month),str(year-1))
## 		wr(' ')
## 		renderer.renderLink(self.uriToSelf(year+1,month),str(year+1))
## 		wr('<br>month:')
## 		renderer.renderLink(self.uriToSelf(year,month-1),'<<')
## 		wr(' ')
## 		renderer.renderLink(self.uriToSelf(year,month+1),'>>')
		
## 		day = ND((year,month,1))
## 		week = day.weekOfYear()
		
## 		#(year,week,isoday) = day.iso_week
## 		#(firstWeekDay,numDays) = calendar.monthrange(year, month)

## 		#while day.iso_week[1] == week:
## 		while day.weekOfYear() == week:
## 			day -= 1
			
## 		day += 1

## 		wr(str(day))
		
## 		wr('<table border=1>')
## 		wr('<tr>')
## 		wr('<td>week</td>')
## 		for wd in weekdays:
## 			wr('<td>%s</td>' % wd)
## 		wr('</tr>')
		
## 		while True:
## 			wr('<tr>')
## 			wr('<td>')
## 			wr(str(week))
## 			wr('</td>')
## 			for col in range(7):
## 				if day == today:
## 					wr('<td bgcolor="red">')
## 				elif day.month() == self.month:
## 					wr('<td bgcolor="white">')
## 				else:
## 					wr('<td bgcolor="gold">')
## 				self.writeDayInMonth(renderer,day)
## 				day += 1
## 				wr('</td>')
## 			wr('</tr>')
## 			week += 1
## 			if day.month() > month:
## 				break
		
## 		wr('</table>')
		
## 	def writeDayInMonth(self,renderer,day):
## 		renderer.write('<p align="center">')
## 		renderer.renderLink(url=self.uriToSelf(year=day.year(),
## 															month=day.month(),
## 															day=day.day()),
## 								  label=str(day.day()))
## 		renderer.write('</p>')
		

## 		ds = self.resource.db.EVENTS.query(date=day)
## 		renderer.renderLink(
## 			url=renderer.uriToDatasource(ds),
## 			label='(%d events)' % len(ds))
		
## ## 		skipper = Skipper(ds,None)
## ## 		# skipper.asLabel(renderer)
## ## 		renderer.renderLink(
## ## 			url=renderer.uriToSkipper(skipper),
## ## 			label='(%d events)' % len(ds))

## 	def show(self):
## 		self.writeWidget(self)
## 		return self._body

		
		
class WebCalendar(AdamoResource):
	isLeaf = True

	def getChild(self, name, request):
		raise "should never be called"

	def renderYear(self):
		pass
		
	def render_GET(self, request):
		renderer = TwistedRenderer(self,request)
 		if len(request.postpath) == 0 :
			year,month = localtime(time())[0:2]
 			#month = localtime(time())[1] 
			return renderer.show(MonthWidget(year,month))
 		year = int(request.postpath[0])
		if len(request.postpath) == 1 :
			return renderer.show(YearWidget(year))
		month = int(request.postpath[1])
		if len(request.postpath) == 2 :
			return renderer.show(MonthWidget(year,month))
		day = int(request.postpath[2])
		widget = DayWidget(ND((year,month,day)))
		return renderer.show(widget)
			
## 	def uriToSelf(self,year=None,month=None,day=None,**options):
## 		uri = self.baseuri + 'calendar'
## 		if year is not None:
## 			uri += '/%d' % year
## 		if month is not None:
## 			uri += '/%d' % month
## 		if day is not None:
## 			uri += '/%d' % day
## 		return uri
		
