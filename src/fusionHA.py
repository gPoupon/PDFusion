import time
import DEFAULT_ENV
import os
import shutil
import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

lastSeenTime = 0
fileDetected = False

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        global lastSeenTime, fileDetected
        if event.is_directory:
            return
        #print(f"New file created: {event.src_path}")
        fileDetected = True
        lastSeenTime = time.time()
        print('Detected new file: ' + event.src_path + ' at: ' + time.ctime())

def createIfNotExist(directories):
    for directory in directories:
        print('Checking for existence of: ' + str(directory))
        if not Path.exists(directory):
            if Path.is_file(directory):
                raise Exception("Supplied directory is actually an existing file: " + str(directory))
            try:
                print (str(directory) + ' not found; trying to create...')
                Path.mkdir(directory)
                print (str(directory) + ' created!')
            except OSError as error:
                print(error)
        else:
            print('Directory found!')

def cleanup(directory):
    if Path.exists(directory) and len(list(Path.iterdir(directory))) > 0:
        for file in Path.iterdir(directory):
            try:
                #subprocess.run(['rm','-r', str(directory)+'/','*'])
                Path.unlink(file)
            except OSError as error:
                print(error)


def processFiles(processingPath, outputPath):
    
    if len(list(Path.iterdir(processingPath))) >0:
        command=['gs', '-o', str(Path.joinpath(outputPath,'output_'+str(time.time_ns())+'.pdf')),'-sDEVICE=pdfwrite', '-dPDFSETTINGS=/prepress']
        fileNames = list(map(str, processingPath.glob('*.pdf')))
        command+=fileNames
        print("Combining: " + str(fileNames))
        print(str(command))
        subprocess.run(command)
        cleanup(processingPath)

def moveFiles(sourceDirectory, outputDirectory):
    for file in Path.iterdir(sourceDirectory):
        shutil.move(Path.joinpath(sourceDirectory, file), outputDirectory)
        print('Moved file: ' + str(file))

def main():
    global lastSeenTime
    global fileDetected

    inputPath = Path(os.getenv('SCAN_DIRECTORY', DEFAULT_ENV.INPUT_DIRECTORY))
    processingPath = Path(os.getenv('PROCESSING_DIRECTORY', DEFAULT_ENV.PROCESSING_DIRECTORY))
    outputPath = Path(os.getenv('OUTPUT_DIRECTORY', DEFAULT_ENV.OUTPUT_DIRECTORY))
    maxWaitTime = os.getenv('MAX_WAIT_TIME', DEFAULT_ENV.MAX_WAIT_TIME)
    if not isinstance(maxWaitTime, int) or maxWaitTime > 3600:
        maxWaitTime = 3600
    
    #Create necesssary folders
    createIfNotExist([inputPath, processingPath, outputPath])
    cleanup(inputPath)
    cleanup(processingPath)

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=inputPath, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
            print('max wait time: ' + str(maxWaitTime))
            print('filedetected: ' + str(fileDetected))
            print(time.time() - lastSeenTime)
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
