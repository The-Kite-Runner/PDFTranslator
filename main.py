from translateToText import *
from writeWord import *

pdf_file_name = input('Please drug pdf file into terminal, and push ENTER\n')
pdf_file_name = pdf_file_name.replace('\\', '')
pdf_file_name = pdf_file_name.strip()
print(pdf_file_name)

text_file_name = translateToText(pdf_file_name)

writeWord(text_file_name)
