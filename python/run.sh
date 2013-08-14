REPO=$HOME/.m2/repository
RWMIDI=$REPO/com/ruinwesen/com-ruinwesen-rwmidi/0.1c/com-ruinwesen-rwmidi-0.1c.jar
MIDIWRAPPER=$REPO/net/loadbang/net.loadbang.midiwrapper/0.0.1-SNAPSHOT/net.loadbang.midiwrapper-0.0.1-SNAPSHOT.jar
JYTHON=/Media/MaxJARs/support/jython2.7b1/jython.jar

java -cp $RWMIDI:$MIDIWRAPPER:$JYTHON org.python.util.jython
