#import traceback

from lino.sdoc import commands as pds

import sys
from StringIO import StringIO

# CodeExampleStyle = styles.Code.child(leftIndent=0)

def showAndExec(txt,expectedOutput=None):
	pds.setFeeder('plain')
	pds.pre(txt)
	pds.setFeeder('xml')

##		for l in traceback.extract_stack():
##			(filename, line_number, function_name, text) = l
##			print filename
	
	sys.stdout = StringIO()
	# sys.stderr = StringIO()
	exec txt in pds.__dict__, pds.__dict__
	out = sys.stdout.getvalue()
	#err = sys.stderr.getvalue()
	sys.stdout = sys.__stdout__
	#sys.stderr = sys.__stderr__

	if expectedOutput is not None:
		if expectedOutput.split() == out.split():
			if len(expectedOutput):
				pds.p("Output:")
				pds.pre(expectedOutput)
		else:
			sys.stderr.write("expectedOutput")
			pds.p("(Test failure: actual output was:")
			pds.pre(out)

def codeExample(txt):
	beginTable("ll",width=getTextWidth()*0.9,
				  model=stylesheet.DefaultTable)
	setFeeder('plain')
	pre(txt,CodeExampleStyle)
	endCell()
	setFeeder('xml')
	exec txt in globals()
	endTable()


def testingExample(visibleCode,expectedOutput=None):
	beginTable("ll",width=getTextWidth()*0.95,
				  model=stylesheet.DefaultTable)
	setFeeder('plain')
	pre(visibleCode,CodeExampleStyle)
	endCell()
	setFeeder('plain')
	
	sys.stdout = StringIO()
	# sys.stderr = StringIO()
	exec txt in globals()
	out = sys.stdout.getvalue()
	#err = sys.stderr.getvalue()
	sys.stdout = sys.__stdout__
	#sys.stderr = sys.__stderr__

	if expectedOutput is not None:
		if expectedOutput != out:
			sys.stderr.write("expectedOutput")

	if len(out):
		pre(out)
	#if len(err):
	#	 pre(err)
		
	endTable()

def tableFromCursor(csr):
	tm = pds.stylesheet.DefaultTable.child()
	for (name, type_code, display_size, internal_size, \
		  precision, scale, null_ok) in csr.description:
		tm.addColumn(label=name)
	if pds.beginTable(model=tm):
		pds.setFeeder('plain')
		for raw in csr.fetchall():
			pds.tr(*raw)
		pds.endTable()

def tableFromQuery(q):
	tm = pds.stylesheet.DefaultTable.child()
	for col in q.getVisibleColumns():
		tm.addColumn(label=col.name)
	if pds.beginTable(model=tm):
		pds.setFeeder('plain')
		for row in q:
			if True: #pds.beginRow():
				for cell in row:
					if True: # pds.beginCell():
						#value = col.atoms2value(atomicRow)
						# print col.name + " = " + str(value)
						#pds.p(str(value))
						pds.p(cell.format())
						pds.endCell()
				pds.endRow()
		pds.endTable()
