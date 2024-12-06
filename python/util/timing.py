from datetime import datetime


class Timer:
    """ Utility class for measuring elapsed time """

    def __init__(self):
        self.start = datetime.now()

    def reset(self):
        """ Reset the timer back to 0.0 elapsed """
        self.start = datetime.now()

    def elapsed(self):
        """
        Elapsed time since object construction or last reset call
        :return: A timedelta object repesenting the elapsed time
        """
        return datetime.now() - self.start

    def elapsed_secs(self):
        """
        Return how many seconds have elapsed
        :return: A float of elapsed seconds
        """
        return (datetime.now() - self.start).total_seconds()


class RateLogger:
    """
    Helper class for printing status when processing lots of records. You can use this class to keep track of
    how many records you have processed and print every N records so you can get a rough feel of how far the process
    is and how fast it is going.
    """
    def __init__(self, log_every_n=1000, log_fn=None):
        self.total = 0
        self.diff = 0
        self.log_every_n = log_every_n
        self.timer = Timer()

        self.log_fn = log_fn
        if not self.log_fn:
            self.log_fn = lambda r: "Processing {} records took {}s.  Total={}".format(r.log_every_n,
                                                                                       r.timer.elapsed_secs(),
                                                                                       r.total)

    def inc(self, n=1):
        self.diff += n

        # start total used to store the original total so we can have it at the correct values both at the end of this
        # fn and in the loop.
        start_total = self.total
        self.total = int(self.total / self.log_every_n) * self.log_every_n

        while self.diff >= self.log_every_n:
            self.diff -= self.log_every_n

            # Incrementing total here so available for log with correct value. Needs to be done here in case
            # n is greater than the log_every_n size.
            self.total += self.log_every_n
            print(self.log_fn(self))

            # Reset the timer for the next block
            self.timer.reset()

        # Set total to the correct final total which may not line up with the block size
        self.total = start_total + n

    def total_time(self):
        return self.timer.elapsed()
