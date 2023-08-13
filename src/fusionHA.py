import time
import DEFAULT_ENV
import os
import shutil
import subprocess
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
        print('Detected new file: ' + event.src_path + ' at:' + lastSeenTime)

def createIfNotExist(directories):
    for directory in directories:
        print('Checking for existence of: ' + directory)
        if not os.path.isdir(directory):
            try:
                print (directory + ' not found; trying to create...')
                os.mkdir(directory)
                print (directory + ' created!')
            except OSError as error:
                print(error)
        else:
            print('Directory found!')

def processFiles(processingPath, outputPath):
    fileNames = os.listdir(processingPath)
    if not len(fileNames) == 0:
        print("Combining: " + fileNames)
        subprocess.run(['pdfunite','*.pdf', 'output'+time.time()+'.pdf'])

def moveFiles(inputPath, processingPath):
    fileNames = os.listdir(inputPath)
    for file in fileNames:
        shutil.move(os.path.join(inputPath, file), processingPath)
        print('Moved file: ' + file)

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
                moveFiles(inputPath, processingPath)
                fileDetected = False
                processFiles(processingPath, outputPath)
                # Checking for race-condition
                if not fileDetected and len(os.listdir(inputPath)) != 0:
                    fileDetected = True
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
