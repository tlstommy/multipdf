import PyPDF2, os, stat, datetime
from tabulate import tabulate

INPUT_DIR = "input"
OUTPUT_DIR = "output"

class main:
    def __init__(self):
        self.cwd = os.getcwd()
        self.inputDir = os.path.join(self.cwd, INPUT_DIR)
        self.outputDir = os.path.join(self.cwd, OUTPUT_DIR)
        self.pdfFiles = []
        self.insertPdf = None
        self.targetPdfPath = None
        self.insertPage = None
        self.insertMode = False

        self.dirExistsCheck()
        self.pdfMerger()

    def dirExistsCheck(self):
        if not os.path.exists(self.inputDir):
            os.mkdir(self.inputDir)
            print(f"Created input directory: {self.inputDir}")
        if not os.path.exists(self.outputDir):
            os.mkdir(self.outputDir)
            print(f"Created output directory: {self.outputDir}")

    def dirContentsCheck(self, dir):
        return os.listdir(dir)

    def listFiles(self):
        tableData = []
        for file in os.listdir(self.inputDir):
            fileStats = os.stat(os.path.join(self.inputDir, file))
            fileData = [file, str(datetime.datetime.utcfromtimestamp(fileStats.st_mtime)), f"{fileStats.st_size/(1<<10):,.0f} KB"]
            self.pdfFiles.append(os.path.join(self.inputDir, file))
            tableData.append(fileData)
        print("\nThe following PDF files were found in the input directory:\n")
        headers = ["File", "Last Modified", "Size"]
        print(tabulate(tableData, headers=headers, tablefmt="fancy_grid"))

    def sort(self):
        while True:
            print("\nIn which order would you like the files to be merged? ")
            print("[1] Alphabetically By Filename [A-Z]")
            print("[2] Alphabetically By Filename [Z-A]")
            print("[3] By Date")
            print("[4] Insert a PDF into a specific position")
            userInput = input("Method: ")
            if userInput == "1":
                self.pdfFiles.sort()
                print("Sorted files alphabetically!\n")
                break
            elif userInput == "2":
                self.pdfFiles.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                print("Sorted files alphabetically!\n")
                break
            elif userInput == "3":
                self.pdfFiles.sort(key=lambda x: os.path.getmtime(x))
                print("Sorted files by date!\n")
                break
            elif userInput == "4":
                self.insertMode = True
                if self.askForInsertPdf():
                    break
            else:
                print("\n[Error] Invalid Input, please choose a correct option. (1 - 4)")

    def askForInsertPdf(self):
        print("\nSpecify the PDF where you want to insert another PDF.")
        targetFile = input("Enter the target PDF filename: ").strip()
        self.targetPdfPath = os.path.join(self.inputDir, targetFile)
        
        if not os.path.exists(self.targetPdfPath):
            print("[Error] The specified target PDF does not exist in the input directory.")
            return False

        print("\nSpecify the PDF to be inserted.")
        insertFile = input("Enter the PDF filename to insert: ").strip()
        insertPdfPath = os.path.join(self.inputDir, insertFile)
        
        if not os.path.exists(insertPdfPath):
            print("[Error] The specified insert PDF does not exist in the input directory.")
            return False
        
        try:
            target_reader = PyPDF2.PdfReader(self.targetPdfPath)
            total_pages = len(target_reader.pages)
            print(f"\nTarget PDF has {total_pages} pages.")
            self.insertPage = int(input(f"Enter the page number after which to insert the PDF (1-{total_pages}): "))
            self.insertPage = self.insertPage - 1
            if self.insertPage <= 0 or self.insertPage > total_pages:
                print(f"[Error] Page number must be between 1 and {total_pages}")
                return False
        except ValueError:
            print("[Error] Please enter a valid page number.")
            return False

        try:
            self.insertPdf = PyPDF2.PdfReader(insertPdfPath)
            return True
        except Exception as e:
            print(f"[Error] Failed to read PDF: {str(e)}")
            return False

    def buildMergedPdf(self):
        while True:
            print("\nAll files in the input directory will be merged into 'Merged.pdf' in the output directory.")
            userInput = input("Would you like to proceed (Y/n)? ")
            if userInput.upper() in ["Y", "YES", ""]:
                print("\nMerging...")
                break
            elif userInput.upper() in ["N", "NO"]:
                print("\nMerge canceled!")
                return
            else:
                print("\n[Error] Invalid Input!")

        try:
            writer = PyPDF2.PdfWriter()
            
            if self.insertMode:
                # Handle PDF insertion mode
                target_reader = PyPDF2.PdfReader(self.targetPdfPath)
                
                # Add pages from target PDF up to insert point
                for i in range(self.insertPage + 1):
                    writer.add_page(target_reader.pages[i])
                
                # Insert the new PDF
                for page in self.insertPdf.pages:
                    writer.add_page(page)
                
                # Add remaining pages from target PDF
                for i in range(self.insertPage + 1, len(target_reader.pages)):
                    writer.add_page(target_reader.pages[i])
            else:
                # Handle normal merge mode
                for pdf_file in self.pdfFiles:
                    reader = PyPDF2.PdfReader(pdf_file)
                    for page in reader.pages:
                        writer.add_page(page)

            with open(os.path.join(self.outputDir, "Merged.pdf"), "wb") as output_file:
                writer.write(output_file)

            print("\n[Success] Wrote merged pdf to: " + os.path.join(self.outputDir, "Merged.pdf"))
            
        except Exception as e:
            print(f"\n[Error] Failed to merge PDFs: {str(e)}")

    def pdfMerger(self):
        print(f"\nPDF Merger is a simple PDF merging program. PDFs put in the Input Directory ({self.inputDir}) will be merged into one singular PDF file in the Output Directory ({self.outputDir}).\n")
        
        while len(self.dirContentsCheck(self.inputDir)) == 0:
            input("[WARN] The input directory is empty. Please place the PDFs to merge inside and press enter to continue\n")
        
        self.listFiles()
        self.sort()
        self.buildMergedPdf()

if __name__ == "__main__":
    merger = main()