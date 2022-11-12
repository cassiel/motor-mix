"""
Overall display, to curses console and device LCD.
"""

class Display:
    def __init__(self):
        self.labelStore = [["    " for _ in range(8)] for _ in range(8)]

    def setupLabels(self, row, labels):
        """
        >>> d = Display()
        >>> def toScreen(r, c, text): print(f"[toScreen {r} {c} |{text}|]")
        >>> d.toScreen = toScreen

        >>> d.setupLabels(3, ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH"])
        [toScreen 6 0 |AAAA|]
        [toScreen 7 0 |   0|]
        [toScreen 6 1 |BBBB|]
        [toScreen 7 1 |   0|]
        [toScreen 6 2 |CCCC|]
        [toScreen 7 2 |   0|]
        [toScreen 6 3 |DDDD|]
        [toScreen 7 3 |   0|]
        [toScreen 6 4 |EEEE|]
        [toScreen 7 4 |   0|]
        [toScreen 6 5 |FFFF|]
        [toScreen 7 5 |   0|]
        [toScreen 6 6 |GGGG|]
        [toScreen 7 6 |   0|]
        [toScreen 6 7 |HHHH|]
        [toScreen 7 7 |   0|]
        """

        self.labelStore[row] = labels

        for i, x in enumerate(labels):
            self.toScreen(row * 2, i, x)
            self.toScreen(row * 2 + 1, i, f"{0:4}")

    def selectRow(self, row):
        """
        >>> d = Display()
        >>> def toScreen(r, c, text): pass
        >>> d.toScreen = toScreen
        >>> def toLCD(r, c, text): print(f"[toLCD {r} {c} |{text}|]")
        >>> d.toLCD = toLCD

        >>> d.setupLabels(0, ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH"])

        >>> d.selectRow(0)
        [toLCD 0 0 |AAAA|]
        [toLCD 1 0 |   0|]
        [toLCD 0 1 |BBBB|]
        [toLCD 1 1 |   0|]
        [toLCD 0 2 |CCCC|]
        [toLCD 1 2 |   0|]
        [toLCD 0 3 |DDDD|]
        [toLCD 1 3 |   0|]
        [toLCD 0 4 |EEEE|]
        [toLCD 1 4 |   0|]
        [toLCD 0 5 |FFFF|]
        [toLCD 1 5 |   0|]
        [toLCD 0 6 |GGGG|]
        [toLCD 1 6 |   0|]
        [toLCD 0 7 |HHHH|]
        [toLCD 1 7 |   0|]

        >>> d.selectRow(5)
        [toLCD 0 0 |    |]
        [toLCD 1 0 |   0|]
        [toLCD 0 1 |    |]
        [toLCD 1 1 |   0|]
        [toLCD 0 2 |    |]
        [toLCD 1 2 |   0|]
        [toLCD 0 3 |    |]
        [toLCD 1 3 |   0|]
        [toLCD 0 4 |    |]
        [toLCD 1 4 |   0|]
        [toLCD 0 5 |    |]
        [toLCD 1 5 |   0|]
        [toLCD 0 6 |    |]
        [toLCD 1 6 |   0|]
        [toLCD 0 7 |    |]
        [toLCD 1 7 |   0|]
        """
        labels = self.labelStore[row]

        for i, x in enumerate(labels):
            self.toLCD(0, i, x)
            self.toLCD(1, i, f"{0:4}")

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.REPORT_ONLY_FIRST_FAILURE, verbose=False)
