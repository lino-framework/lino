# http://127.0.0.1:8000/media/webdav/davopen_test.html
#~ how to generate a self-signed key:
#~ keytool -genkey
#~ keytool -selfcert
#~ keytool -list


#~ JFLAGS = -d build -sourcepath src
#~ JFLAGS = -classpath s:\classpath\registry-3.1.3\classes
#~ JFLAGS = -target 1.6 -source 1.6 -bootclasspath "C:/Program Files/Java/jre6/lib/rt.jar"
#~ JFLAGS = -Xlint:unchecked
JFLAGS = 
JC = javac

.SUFFIXES: .java .class

.java.class:
	$(JC) $(JFLAGS) $*.java

JARFILE = ../media/applets/DavLink.jar
CLASSES = davlink/DavLink.java

default: jar

classes: $(CLASSES:.java=.class)

jar: classes
	jar cvf $(JARFILE) davlink
	jarsigner $(JARFILE) mykey

clean:
	rm davlink/*.class
	rm $(JARFILE)
	
	