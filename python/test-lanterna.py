from com.googlecode.lanterna import TerminalFacade
from com.googlecode.lanterna.screen import ScreenWriter, ScreenCharacterStyle
from com.googlecode.lanterna.terminal import Terminal
from java.lang import Thread

screen = TerminalFacade.createScreen()

screen.startScreen()

writer = ScreenWriter(screen)

writer.setForegroundColor(Terminal.Color.BLACK)
writer.setBackgroundColor(Terminal.Color.WHITE)
writer.drawString(5, 3, "Hello Lanterna!", ScreenCharacterStyle.Bold)
writer.setForegroundColor(Terminal.Color.DEFAULT)
writer.setBackgroundColor(Terminal.Color.DEFAULT)
writer.drawString(5, 5, "Hello Lanterna!")
writer.drawString(5, 7, "Hello Lanterna!")
screen.refresh()

Thread.sleep(5000)

screen.clear()
screen.refresh()
Thread.sleep(1000)

screen.stopScreen()
