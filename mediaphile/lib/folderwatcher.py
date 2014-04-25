import pyinotify

# The watch manager stores the watches and provides operations on watches
wm = pyinotify.WatchManager()

mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events


class EventHandler(pyinotify.ProcessEvent):
    """
    Eventhandler for inotify.
    """
    def process_IN_CREATE(self, event):
        """
        Handles creation of files.
        """
        print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        """
        Handles deletion of files.
        """
        print "Removing:", event.pathname


def run():
    """

    """
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch('/tmp', mask, rec=True)
    notifier.loop()