import PyPDF2, os, stat, datetime
from tabulate import tabulate

INPUT_DIR = "input"
OUTPUT_DIR = "output"

class main:
    def __init__(self):
        self.cwd = os.getcwd()
        self.inputDir = os.path.join(self.cwd,INPUT_DIR)
        self.outputDir = os.path.join(self.cwd,OUTPUT_DIR)
        self.pdfFiles = []

        self.dirExistsCheck()
        self.pdfMerger()
        
      
    #check if input and output dirs exist
    def dirExistsCheck(self):
        if os.path.exists(self.inputDir) == False:
            os.mkdir(self.inputDir)
            print(f"Created input directory: {self.inputDir}")
        if os.path.exists(self.outputDir) == False:
            os.mkdir(self.outputDir)
            print(f"Created output directory: {self.outputDir}")    
            
    def dirContentsCheck(self,dir):
        dir = os.listdir(dir)
        return dir

    #list all the input files and their info
    def listFiles(self):

        tableData = []
        for file in os.listdir(self.inputDir):
            fileStats = os.stat(os.path.join(self.inputDir, file))
            fileData = [file, str(datetime.datetime.utcfromtimestamp(fileStats.st_mtime)), str(f"{fileStats.st_size/(1<<10):,.0f} KB")]
            self.pdfFiles.append(file)
            tableData.append(fileData)
        print("\nThe following PDF files were found in the input directory:\n")
        headers = ["File", "Last Modified", "Size"]
        print(tabulate(tableData, headers=headers, tablefmt="fancy_grid"))
    
    def sort(self,method):
        while True:
            print("In which order would you like the files to be mergerd? ")
            print("[1] Alphabetically By Filename")
            print("[2] By Date")
            userInput = input("Method: ")
            if userInput




    #main
    def pdfMerger(self):
        print(f"\nPDF Merger is a simple pdf merging program. pdfs put in the Input Directory ({self.inputDir}) will be merged into one singular PDF file in the output directory({self.outputDir}).\n")
        
        while len(self.dirContentsCheck(self.inputDir)) == 0:
            input("[WARN] The input is directory is empty, please place the pdfs to merge inside and press enter to continue\n")
        
        self.listFiles()
        self.sort()

merger = main()