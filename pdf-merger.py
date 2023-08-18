import PyPDF2, os

INPUT_DIR = "input"
OUTPUT_DIR = "output"

class main:
    def __init__(self):
        self.cwd = os.getcwd()
        self.inputDirAddress = os.path.join(self.cwd,INPUT_DIR)
        self.outputDirAddress = os.path.join(self.cwd,OUTPUT_DIR)
        self.dirExistsCheck()
        print(f"\nPDF Merger is a simple pdf merging program. pdfs put in the Input Directory ({self.inputDirAddress}) will be merged into one singular PDF file in the output directory({self.outputDirAddress}).")
      
    #check if input and output dirs exist
    def dirExistsCheck(self):
        if os.path.exists(self.inputDirAddress) == False:
            os.mkdir(self.inputDirAddress)
            print(f"Created input directory: {self.inputDirAddress}")
        if os.path.exists(self.outputDirAddress) == False:
            os.mkdir(self.outputDirAddress)
            print(f"Created output directory: {self.outputDirAddress}")    
            



merger = main()