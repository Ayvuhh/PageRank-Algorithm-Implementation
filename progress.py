"""A progress bar for the command line"""
import sys
import time


class Progress:
    """Progress bar object for the comand line

    This class allows to conveniently add progress bars to long running
    calculations. It writes textual and graphical information about
    the progress of a text to sys.stderr. To be used in the following
    way:

    >>> prog = Progress(100, "Performing some long running task")
    >>> for step in some_long_calculation():
    >>>     prog += 1
    >>>     prog.show()
    >>> prog.finish()

    The progress bar displays the percentage of completion
    (counter/total) and the real time taken by the calculation so far.

    It is allowed to manually alter prog.counter and prog.total during
    use.
    """
    def __init__(self, total, title="Progress", width=80):
        """Initialize Progress bar

        Parameters:
        total (number) -- maximum value of counter
        title (str) -- information to be displayed
        width (int) -- width of the display progress bar
        """
        self.counter = 0
        self.total = total
        self.title = title
        self.width = width
        self.start_time = time.time()

    def __iadd__(self, value):
        """Increase current counter by value"""
        self.counter += value
        return self

    def show(self):
        """Display progress bar in its current state"""
        sec = time.time()-self.start_time
        # eta = self.total/self.counter*sec-sec if self.counter else 0
        percent = 100*self.counter/self.total
        title = f'{self.title} ({percent:.0f}% {sec//60:02.0f}:{sec%60:02.0f}) '
        if len(title) >= self.width:
            raise ValueError("Progress bar does not fit width. Shorten title of increase width.")
        bar_width = self.width - (len(title)) - 3
        full_width = int(bar_width*self.counter/self.total)
        empty_width = bar_width - full_width
        sys.stdout.write('\r'+title+'['+full_width*'#'+empty_width*'.'+']')
        sys.stdout.flush()

    def finish(self):
        """Hide progress bar"""
        sys.stdout.write('\r'+self.width*' '+'\r')
        sys.stdout.flush()
