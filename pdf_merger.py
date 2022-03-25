import os
#you'll probably need to pip or conda install the PyPDF2 package:
from PyPDF2 import PdfFileMerger, PdfFileReader

def merge_pdfs(file_path_str):
    '''
    the file_path_str is either absolute or relative file path as a string to the file where 
    all your pdfs are saved (and where we'll export the merged file to. examples:
    './file_folder_relative_to_where_I_am/'
    or
    '/Users/joesmith/Desktop/pdf_reports/'    
    '''
    #gather list of all the pds in the folder:
    pdf_list = os.listdir(file_path_str)
    #make sure you don't pick up any system files or other non-pdfs:
    pdf_list = [pdf for pdf in pdf_list if '.pdf' in pdf]

    #sort the pdfs by file name:
    pdf_list.sort()
    
    # Call the PdfFileMerger
    mergedObject = PdfFileMerger()
 
    # Loop through all of the single pdfs and append them into one document
    for file in pdf_list:
        fullpath = os.path.join(file_path_str, file)
        mergedObject.append(PdfFileReader(fullpath, 'rb'))

    # Write all the files into a file which is named as shown below
    output = os.path.join(file_path_str, 'merged_pdfs.pdf')
    mergedObject.write(output)

def main():
    print("Hello World!")
    merge_pdfs('/mnt/chromeos/MyFiles/Downloads/pdf')

if __name__ == "__main__":
    main()