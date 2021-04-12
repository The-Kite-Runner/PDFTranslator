from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import time
import os
import pyperclip
import sys


class YoudaoTranslator:

    def __init__(self):
        print("Start to translate by fanyi.youdao.com, be careful DO NOT USE CLIPBOARD before translating finished")
        print("syspath", sys.path[0])
        self.driver_path = sys.path[0].split(
            '/base_library.zip')[0] + "/chromedriver"
        self.driver_path = "./chromedriver"
        self.chrome = webdriver.Chrome(self.driver_path)
        self.chrome.get("http://fanyi.youdao.com/")

    def translate(self, key):
        # self.chrome.refresh()
        try:
            #script = "lans = document.getElementById('languageSelect');lans.childNodes[7].firstElementChild.click()"
            #print("translate from:", key)
            # 这里使用javascript获取翻译语言，注意lans.childNodes[index],index需为奇数，大家在浏览器里运行便可知道原因。
            # chrome.execute_script(script)
            inputOriginal = self.chrome.find_element_by_id('inputOriginal')
            inputOriginal.send_keys(Keys.COMMAND, 'a')
            inputOriginal.send_keys(Keys.BACKSPACE)
            results = self.chrome.find_elements_by_xpath(
                '//div[@id="transTarget"]/p/span')
            while len(results) > 0:
                results = self.chrome.find_elements_by_xpath(
                    '//div[@id="transTarget"]/p/span')

            sendKeyStart = time()
            # inputOriginal.send_keys(key)
            pyperclip.copy(key)
            inputOriginal.send_keys(Keys.COMMAND, 'v')
            sendKeyEnd = time()
            #print("time to send keys:", sendKeyEnd - sendKeyStart, "s")
            # chrome.implicitly_wait(1)
            results = []
            sentencesInParagraph = []
            start = time()
            while len(results) == 0:
                end = time()
                if end - start > 5:
                    return ""
                results = self.chrome.find_elements_by_xpath(
                    '//div[@id="transTarget"]/p/span')
            paragraphs = self.chrome.find_elements_by_xpath(
                '//div[@id="transTarget"]/p')
            for i in range(len(paragraphs)):
                sentences = self.chrome.find_elements_by_xpath(
                    '//div[@id="transTarget"]/p[@data-section="' + str(i) + '"]/span')
                sentencesInParagraph.append(len(sentences))
            #print("sentenceInParagraph: ", sentencesInParagraph)

            trans_str = ""
            sentenceCount = 0
            paraCount = 0
            for result in results:
                # for r in result.text:
                trans_str = trans_str + result.text
                # Add \n when the paragraph finish
                sentenceCount = sentenceCount + 1
                if sentenceCount >= sentencesInParagraph[paraCount]:
                    sentenceCount = 0
                    paraCount = paraCount + 1
                    trans_str = trans_str + '\n'
            return trans_str
        except Exception as e:
            print(e)
