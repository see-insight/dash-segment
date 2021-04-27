# Monitoring files for changes
# pip install watchdog

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
	def on_modified(self, event):
		print("{event.src_path} has been modified")

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path = '.', recursive=False)
observer.start()

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	observer.stop()
observer.join()

# watchdog in javascript?

# When you run this program and make any changes to any file in current directory,
# the on_modified function from MyHandler class gets called with the event.
# In the MyHandler class you can define your own functions to handle the events. 
# In the path, you can specify the files/directories you want to monitor. 
# To stop this program, use Ctrl + C

# Monitor a filesystem and react when a change occurs, so that I can check for the segmentation mask in the directory