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
            self.pdfFiles.append(os.path.join(self.inputDir,file))
            tableData.append(fileData)
        print("\nThe following PDF files were found in the input directory:\n")
        headers = ["File", "Last Modified", "Size"]
        print(tabulate(tableData, headers=headers, tablefmt="fancy_grid"))
       
    def sort(self):
        while True:
            print("\nIn which order would you like the files to be mergerd? ")
            print("[1] Alphabetically By Filename [A-Z]")
            print("[2] Alphabetically By Filename [Z-A]")
            print("[3] By Date")
            userInput = input("Method: ")
            if userInput == "1":
                self.pdfFiles.sort()
                print("Sorted files alphabetically!\n")
                break
            elif userInput == "2":
                self.pdfFiles.sort(key=lambda x: os.path.getmtime(x))
                self.pdfFiles.reverse()
                print("Sorted files alphabetically!\n")
                break
            elif userInput == "3":
                self.pdfFiles.sort(key=lambda x: os.path.getmtime(x))
                print("Sorted files by date!\n")
                break    

            else:
                print("\n[Error] Invalid Input please choose a correct option. (1 - 3)")

    def buildMergedPdf(self):
        
        while True:
            print("\nAll files in the input directory will be merged into 'Merged.pdf' in the output directory.")
            userInput = input("Would you like to proceed (Y/n)? ")
            if(userInput.upper() == "Y" or userInput.upper() == "YES"):
                print("\nMerging...\n")
                break
            elif(userInput.upper() == "N" or userInput.upper() == "NO"):
                print("\nMerge canceled!\n")
                return
            else:
                print("\n[Error] Invalid Input!\n")
                continue


        masterPDFPages = []
        writer = PyPDF2.PdfWriter()

        for pdf in self.pdfFiles:
            masterPDFPages.append(PyPDF2.PdfReader(pdf))

        for pdf in masterPDFPages:
            for page in range(len(pdf.pages)):
                writer.add_page(pdf.pages[page])
        writer.write(os.path.join(self.outputDir,"Merged.pdf"))


        print("\n[Success] Wrote merged pdf to: " + str(self.outputDir) + "\Merged.pdf")


    #main
    def pdfMerger(self):
        print(f"\nPDF Merger is a simple pdf merging program. pdfs put in the Input Directory ({self.inputDir}) will be merged into one singular PDF file in the output directory({self.outputDir}).\n")
        
        while len(self.dirContentsCheck(self.inputDir)) == 0:
            input("[WARN] The input is directory is empty, please place the pdfs to merge inside and press enter to continue\n")
        
        self.listFiles()
        self.sort()
        self.buildMergedPdf()

merger = main()