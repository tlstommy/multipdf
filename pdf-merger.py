import PyPDF2, os

INPUT_DIR = "input"
OUTPUT_DIR = "output"

class main:
    def __init__(self):
        self.cwd = os.getcwd()
        self.inputDir = os.path.join(self.cwd,INPUT_DIR)
        self.outputDir = os.path.join(self.cwd,OUTPUT_DIR)
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
        

    #main
    def pdfMerger(self):
        print(f"\nPDF Merger is a simple pdf merging program. pdfs put in the Input Directory ({self.inputDir}) will be merged into one singular PDF file in the output directory({self.outputDir}).\n")
        
        while len(self.dirContentsCheck(self.inputDir)) == 0:
            input("[WARN] The input is directory is empty, please place the pdfs to merge inside and press enter to continue\n")
        
        self.listFiles()

merger = main()