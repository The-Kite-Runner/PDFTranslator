# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
from YoudaoTranslator import *
import pyperclip


def get_number_count(s):
    numList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    count = 0
    for i in s:
        if i in numList:
            count += 1
    return count


def translateToText(file_path):
    MIN_BUFFER_SIZE = 3000
    MAX_HEADER_FOOT_LENGTH = 100
    MIN_HEADER_FOOT_NUMBER_COUNT = 5

    Path = open(file_path, 'rb')
    Save_name = file_path.split('.pdf')[0] + '.txt'
    # 来创建一个pdf文档分析器
    parser = PDFParser(Path)
    # 创建一个PDF文档对象存储文档结构
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建一个PDF资源管理器对象来存储共赏资源
        rsrcmgr = PDFResourceManager()
        # 设定参数进行分析
        laparams = LAParams()
        # 创建一个PDF设备对象
        # device=PDFDevice(rsrcmgr)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        translator = YoudaoTranslator()
        buffer = ""

        # 处理每一页
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                if(isinstance(x, LTTextBoxHorizontal)):
                    content = str(x.get_text())
                    content = content.replace('-\n', '').replace('-\r', '')
                    content = content.replace('\n', ' ').replace('-r', ' ')
                    content = content + "\n"
                    # Check whether the content is valid
                    if content.isspace():
                        continue
                    if len(content) <= MAX_HEADER_FOOT_LENGTH:
                        numberCount = get_number_count(content)
                        if numberCount > MIN_HEADER_FOOT_NUMBER_COUNT or numberCount >= len(content) / 2:
                            continue

                    # Add content to buffer
                    buffer = buffer + content

                    # When length is over MIN_BUFFER_SIZE, start to translate
                    if len(buffer) > MIN_BUFFER_SIZE:
                        #trans_content = youdao_translate(content)
                        trans_content = translator.translate(buffer)
                        with open(Save_name, 'a', encoding='utf-8') as f:
                            #print("write:" + buffer)
                            #print("trans:" + trans_content)
                            # f.write(buffer)
                            f.write(trans_content)
                            f.write('\n')
                        buffer = ""
        trans_content = translator.translate(buffer)
        with open(Save_name, 'a', encoding='utf-8') as f:
            #print("write:" + buffer)
            #print("trans:" + trans_content)
            # f.write(buffer)
            f.write(trans_content)
            f.write('\n')
        print("Finish translate, store to ", Save_name)
    return Save_name
