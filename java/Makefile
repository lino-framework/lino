# http://127.0.0.1:8000/media/webdav/davopen_test.html

#~ JFLAGS = -d build -sourcepath src
JFLAGS = -classpath s:\classpath\registry-3.1.3\classes
JC = javac

.SUFFIXES: .java .class

.java.class:
	$(JC) $(JFLAGS) $*.java

JARFILE = ../media/applets/Applets.jar
CLASSES = davopen/DavOpen.java

default: jar

classes: $(CLASSES:.java=.class)

jar: classes
	jar cvf $(JARFILE) davopen
	jarsigner $(JARFILE) mykey

clean:
	rm davopen/*.class
	rm $(JARFILE)
	
	