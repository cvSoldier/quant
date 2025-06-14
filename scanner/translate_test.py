from googletrans import Translator

def ggtran(text,dest,src):
    """
    googletrans api 翻译调用
    :param text: 要翻译的原文
    :param dest: 翻译后输出的语言种类
    :param src: 原文的语言种类（auto为默认识别）
    :return: 翻译后的内容
    """
    translater = Translator()
    result = translater.translate(text, dest, src)
    print(result)
    print(result.text)
    return result.text

import requests

if __name__=="__main__":
    from translate import Translator

    translator = Translator(to_lang="zh")
    translation = translator.translate("Houston American Energy Corp. Provides Response to Unusual Market Action")
    # translation = translator.translate("Helius Medical Technologies, Inc. Announces Authorized Claim for Payment by Major Healthcare Payer for its Portable Neuromodulation Stimulator (PoNS®) Device")
    print(translation)  # 输出: "你好，世界！"