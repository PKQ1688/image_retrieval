# -*- coding:utf-8 -*-
# @author :adolf
from googletrans import Translator

translator = Translator(service_urls=['translate.google.cn'])
source = "There are 10 bags with 100 identical coins in each bag. In all bags but one, each coin weighs 10 grams. However, all the coins in the counterfeit bag weigh either 9 or 11 grams. Can you find the counterfeit bag in only one weighing, using a digital scale that tells the exact weight?"
text = translator.translate(source, src='en', dest='zh-cn').text
print(text)
