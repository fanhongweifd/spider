#!/usr/bin/python
# -*- coding: utf-8 -*-
# 模块名: gooseeker
# 类名: GsExtractor
# Version: 2.1
# 说明: html内容提取器
# 功能: 使用xslt作为模板，快速提取HTML DOM中的内容。
# released by 集搜客(http://www.gooseeker.com) on May 18, 2016
# github: https://github.com/FullerHua/jisou/core/gooseeker.py

from urllib import request
from urllib.parse import quote
from lxml import etree
from xmlUnit import ReadXML
import os


class GsExtractor(object):
    configFileName = os.path.abspath(os.path.dirname(__file__)) + "\\xmlUnit\\config.xml"
    readxml = ReadXML.ReadXml(configFileName)
    APIKey = readxml.get_RootAttribute("appkey")
    def _init_(self):
        self.xslt = ""

    # 从文件读取xslt
    def setXsltFromFile(self, xsltFilePath):
        file = open(xsltFilePath, 'r', encoding='UTF-8')
        try:
            self.xslt = file.read()
        finally:
            file.close()

    # 从字符串获得xslt
    def setXsltFromMem(self, xsltStr):
        self.xslt = xsltStr

    # 通过GooSeeker API接口获得xslt
    def setXsltFromAPI(self, theme, middle=None, bname=None):
        apiurl = "http://www.gooseeker.com/api/getextractor?key=" + GsExtractor.APIKey + "&theme=" + quote(theme)
        if (middle):
            apiurl = apiurl + "&middle=" + quote(middle)
        if (bname):
            apiurl = apiurl + "&bname=" + quote(bname)
        apiconn = request.urlopen(apiurl)
        self.xslt = apiconn.read()

    # 返回当前xslt
    def getXslt(self):
        return self.xslt

    # 提取方法，入参是一个HTML DOM对象，返回是提取结果
    def extract(self, html):
        xslt_root = etree.XML(self.xslt)
        transform = etree.XSLT(xslt_root)
        result_tree = transform(html)
        # return unescape(str(result_tree))  # 直接在方法里面返回的时候，转换特殊字符 比如 &amp;
        return result_tree

    # 提取方法，入参是html源码，返回是提取结果
    def extractHTML(self, html):
        doc = etree.HTML(html)
        return self.extract(doc)
