# -*- coding: gbk -*- 
'''
Created on 2016��4��19��
@author: shenyf
'''
import urllib2
import re
import string

class AchieveSSEStockInfo_Deprecated:
    '''����Ϻ�֤��������Ʊ��Ϣ.'''
    
    # Ĭ�ϵĻ�ȡָ��ֵ�ı��ʽ
    __patternStr = "<td.+>(.+)</td>"
    # ����ҳ��ɹ�
    __urlAccessSuccess = False
    
    # ָ��ķ�����˳���Ѿ��źã��벻Ҫ�Ҷ�
    __public__ = ['getCompanyCode', 'getCompanyShortName', 'getCompanyName', 'getCompanyEnlishName', 'getIpoAddress', 'getASharesCode',
                  'getASharesShortName', 'getASharesIPODate', 'getASharesTotalCapital', 'getASharesOutstandingCaptial', 'getBSharesCode',
                  'getBSharesShortName', 'getBSharesIPODate', 'getBSharesTotalCapital', 'getBSharesOutstandingCaptial', 'getArea',
                  'getProvince', 'getCity', 'getTrade', 'getWebsite']
    '''
    all indexs as follow:
        companyCode     ��˾����
        companyShortName     ��˾���
        companyName      ��˾ȫ��
        companyEnlishName      Ӣ������
        ipoAddress      ע���ַ
        aSharesCode      A�ɴ���
        aSharesShortName      A�ɼ��
        aSharesIPODate      A����������
        aSharesTotalCapital      A���ܹɱ�
        aSharesOutstandingCaptial      A����ͨ�ɱ�
        bSharesCode      B�ɴ���
        bSharesShortName      B�ɼ��
        bSharesIPODate      B���������� 
        bSharesTotalCapital       B���ܹɱ�  
        bSharesOutstandingCaptial      B����ͨ�ɱ�
        area      ���� 
        province      ʡ��
        city      ����
        trade      ������ҵ
        website      ��˾��ַ
        
        status A��״̬/B��״̬
    '''
    
    def getCompanyCode(self):
        return self.__getBasicValue(u'��˾����')
    
    def getStatus(self):
        v = self.__getBasicValue(u'A��״̬/B��״̬', pattern='<td>(.+)</td>')
#         print v
        if v == 0 or u'ժ��' in v:
            return False
        else:
            return True
    
    def getCompanyShortName(self):
        return self.__getBasicValue(u'��˾���')
    
    def getCompanyName(self):
        return self.__getBasicValue(u'��˾ȫ��').split('/')[0]
    
    def getCompanyEnlishName(self):
        return self.__getBasicValue(u'��˾ȫ��').split('/')[1]
    
    def getIpoAddress(self):
        return self.__getBasicValue(u'ע���ַ')
    
    def getASharesCode(self):
        return self.__getBasicValue(u'��Ʊ����(A��/B��)').split('/')[0]
    
    def getASharesShortName(self):
        return self.__getBasicValue(u'��˾���')
    
    def getASharesIPODate(self):
        return self.__getBasicValue(u'������(A��/B��)', '.*<a.+>(\d{4}-\d{2}-\d{2})</a>')

    def getASharesTotalCapital(self):      
        return self.__getCapitalValue(u'�ɷ�����')
    
    def getASharesOutstandingCaptial(self):
        return self.__getCapitalValue(u'����ͨ�ɷݺϼ�')
    
    def getBSharesCode(self):
        return self.__getBasicValue(u'��Ʊ����(A��/B��)').split('/')[1]
    
    def getBSharesShortName(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.getASharesShortName()
    
    def getBSharesIPODate(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.__getBasicValue(u'������(A��/B��)', '.*<a.+>/(.+)</a>.*')
    
    def getBSharesTotalCapital(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.getASharesTotalCapital()  
    
    def getBSharesOutstandingCaptial(self):
        if self.getBSharesCode().find('-') != -1:
            return ''
        else:
            return self.getASharesOutstandingCaptial()
    
    def getArea(self):
        return self.__getBasicValue(u'����ʡ/ֱϽ��')
    
    def getProvince(self):
        return self.__getBasicValue(u'����ʡ/ֱϽ��') 
    
    def getCity(self):
        return self.__getBasicValue(u'����ʡ/ֱϽ��') 
    
    def getTrade(self):
        return self.__getBasicValue(u'CSRC��ҵ')
    
    def getWebsite(self):
        return self.__getBasicValue(u'��ַ', '.+>(.+)</a></td>')
        
    def __getPage(self, url):
        '''��ȡָ����ַ��html���� .'''
        
        request = urllib2.Request(url)
        # ���в���ʵ���Ͽ��Բ�����
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Encoding', 'gzip, deflate, sdch')
        request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        request.add_header('Cache-Control', 'max-age=0')
        request.add_header('Connection', 'keep-alive')
        request.add_header('Host', 'biz.sse.com.cn')
        request.add_header('Upgrade-Insecure-Requests', '1')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36')
        
        # ����5�Σ����ÿ�ζ���timeout����ӡ��ʾ��Ϣ������none 
        Max_Num = 5
        for i in range(Max_Num):
            try:    
                response = urllib2.urlopen(url=request, timeout=15)
                self.__urlAccessSuccess = True
                break
            except:
                pass
            
            if i < Max_Num - 1:
                continue
            else:
                print 'URLError: <urlopen error timed out> All times is failed '
                return None
        
        # gbk����gb2312
        response.encoding = 'gbk'
        result = response.read()
        # �����н�βΪbr�����,�õ���ҳ������\r\n����
        result = result.replace("<br>\r\n", '/').replace('<BR>\r\n', '/')
#         print result
        return  unicode(result, "gbk")
    
    def __locateIndex(self, resultList, key):
        """���ָ��ָ����������."""
        
        # ���ָ��������
        for i in range(0, resultList.__len__()):
    #         print 'list' + resultList[i]
            if key in resultList[i]:
                    return  i
        # ���û�в鵽ָ�꣬����-1
        return -1    
    
    def __getValue(self, key, resultList, pattern):
        '''���ָ���ֵ '''
        
        lineStartAndEnd = '^<td.+</td>'
        sourceStr = ''
        
        lineNumber = self.__locateIndex(resultList, key)
        
        # ���û��ָ��������Ϊ-1��ֱֵ�ӷ���0
        if lineNumber == -1:
            return 0
            
        for i in range(lineNumber, resultList.__len__()):
            sourceStr = sourceStr + resultList[i + 1].replace('\r\n', '')
        #       print sourceStr
            # ���������<td>*</td>��ʽ,����ƴ��Ϊһ��
            m = re.match(lineStartAndEnd, sourceStr)
            if m:
                m = re.match(pattern, sourceStr)
                if m:
#                     print key + " " + m.group(1)
                    return m.group(1)
                else:
                    break
            else:
                i = i + 1
        return 0
    
    def __getBasicValue(self, key, pattern=__patternStr):
        '''������й�˾������Ϣ��ֵ.'''
        
        # �״�ʹ�ø÷�������Ҫ����url����ȡ��ҳ����
        if self.basicResultList == None:
            result = self.__getPage(self.url)
            if self.__urlAccessSuccess:
                self.basicResultList = result.split('\r\n')
        
        # �����һ��getPage ����ʧ�ܣ��ù����ָ��ֱ�ӷ���None�����ټ������Է���ҳ��
        if not self.__urlAccessSuccess:
            return None
        
        return self.__getValue(key, self.basicResultList, pattern)

    def __getCapitalValue(self, key, pattern=__patternStr):
        '''������й�˾�ɱ���Ϣ��ֵ.'''
        
        # �״�ʹ�ø÷�������Ҫ����url����ȡ��ҳ����
        if self.capitalResultList == None:
            result = string.lower(self.__getPage(self.capitalUrl))
            if self.__urlAccessSuccess:
                self.capitalResultList = result.split('\r\n')
                
        # �����һ��getPage ����ʧ�ܣ��ù����ָ��ֱ�ӷ���None�����ټ������Է���ҳ��
        if not self.__urlAccessSuccess:
                return None
        
        return self.__getValue(key, self.capitalResultList, pattern)
    
    def __init__(self, stockCode):
        self.url = r'http://biz.sse.com.cn/sseportal/webapp/datapresent/SSEQueryListCmpAct?reportName=QueryListCmpRpt&COMPANY_CODE=' + str(stockCode) + '&REPORTTYPE=GSZC&PRODUCTID=' + str(stockCode)
        self.capitalUrl = r'http://biz.sse.com.cn/sseportal/webapp/datapresent/SSEQueryStckStructAct?PRODUCT=' + str(stockCode) + '&COMPANYCODE=' + str(stockCode)
        self.basicResultList = None
        self.capitalResultList = None
        pass 
    
        
if __name__ == '__main__':
    a = AchieveSSEStockInfo(600292)
    for c in a.__public__:
        f = getattr(a, c)
        print c 
        print f()
    
    print a.getStatus()
