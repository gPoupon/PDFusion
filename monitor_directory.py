import time
import DEFAULT_ENV
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

lastSeenTime = 0
fileDetected = False

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        #print(f"New file created: {event.src_path}")
        fileDetected = True
        lastSeenTime = time.time()

def createIfNotExist(directories):
    for directory in directories:
        if not os.path.isdir(directory):
            try:
                os.mkdir(directory)
            except OSError as error:
                print(error)


def main():
    
    inputPath = os.getenv('SCAN_DIRECTORY', DEFAULT_ENV.INPUT_DIRECTORY)
    processingPath = os.getenv('PROCESSING_DIRECTORY', DEFAULT_ENV.PROCESSING_DIRECTORY)
    outputPath = os.getenv('OUTPUT_DIRECTORY', DEFAULT_ENV.OUTPUT_DIRECTORY)
    maxWaitTime = os.getenv('MAX_WAIT_TIME', DEFAULT_ENV.MAX_WAIT_TIME)
    #Create necesssary folders
    createIfNotExist(inputPath, processingPath, outputPath)

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=inputPath, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
            if fileDetected and (time.time() - lastSeenTime) > maxWaitTime:
                
                fileDetected = False
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
