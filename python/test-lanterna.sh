REPO=$HOME/.m2/repository
RWMIDI=$REPO/com/ruinwesen/com-ruinwesen-rwmidi/0.1c/com-ruinwesen-rwmidi-0.1c.jar
MIDIWRAPPER=$REPO/net/loadbang/net.loadbang.midiwrapper/0.0.1-SNAPSHOT/net.loadbang.midiwrapper-0.0.1-SNAPSHOT.jar
LANTERNA=$REPO/com/googlecode/lanterna/lanterna/2.1.8/lanterna-2.1.8.jar
JYTHON=$REPO/org/python/jython/2.7-b1/jython-2.7-b1.jar

# Run in Swing (HEADLESS=false) for debugging; turn HEADLESS=true to run neatly
# in a terminal.

HEADLESS=true

java -cp $RWMIDI:$MIDIWRAPPER:$LANTERNA:$JYTHON \
    -Djava.awt.headless=$HEADLESS \
    org.python.util.jython \
    test-lanterna.py
