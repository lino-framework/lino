# http://127.0.0.1:8000/media/webdav/davopen_test.html
#~ how to generate a self-signed key:
#~ keytool -genkey
#~ keytool -selfcert
#~ keytool -list


#~ JFLAGS = -d build -sourcepath src
#~ JFLAGS = -classpath s:\classpath\registry-3.1.3\classes
#~ JFLAGS = -target 1.6 -source 1.6 -bootclasspath "C:/Program Files/Java/jre6/lib/rt.jar"
#~ JFLAGS = -Xlint:unchecked
JFLAGS = -classpath ~/Downloads/eid-applet-sdk/eid-applet-service-1.0.1.GA.jar

JC = javac

.SUFFIXES: .java .class

.java.class:
	$(JC) $(JFLAGS) $*.java

DAVLINK_JARFILE = ../lino/media/applets/DavLink.jar
EID_JARFILE = ../lino/media/applets/EIDReader.jar

CLASSES = davlink/DavLink.java lino/eid/EIDReader.java 

default: jars

classes: $(CLASSES:.java=.class)

jars: classes
	jar cvf $(DAVLINK_JARFILE) davlink
	jarsigner -storepass "`cat ~/.keystore_password`" $(DAVLINK_JARFILE) mykey
	jar cvf $(EID_JARFILE) lino/eid
	jarsigner -storepass "`cat ~/.keystore_password`" $(EID_JARFILE) mykey

clean:
	rm davlink/*.class
	rm lino/eid/*.class
	rm $(DAVLINK_JARFILE)
	rm $(EID_JARFILE)
	
	
