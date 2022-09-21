from random import choice
from copy import deepcopy
from typing import List, Tuple

from HDTFtypes import Header, HeaderPair
from receiver import Receiver, get_receiver
from mutator import Mutator, get_mutator


def evaluate(receiver: Receiver, header: Header, output: bool = False) -> Tuple[List[HeaderPair], int, bool, str]:
    reslist, coverage, status, reason = receiver.get_parse(header, output)
    if output:
        print('{:<35}'.format(receiver._name) +
              ('parse pass' if status else 'parse fail') + '\n')
        print('{:<35}{}'.format('Coverage', coverage))
        for j in reslist:
            print('{:<35}{}'.format(j.key, j.value))
        print('\n')
    return reslist, coverage, status, reason


def compare_result(all_res: List[Tuple[List[HeaderPair], bool, str]]) -> Tuple[bool, List[Tuple[List[HeaderPair], bool, str]]]:
    if len(all_res) == 0 or len(all_res) == 1:
        return True
    cur_res = all_res[0][0]
    cur_status = all_res[0][1]
    for i in all_res:
        if i[1] != cur_status or i[0] != cur_res:
            return False, all_res
    return True, None


def eval_list(receiver_list: List[Receiver], header: Header, output: bool = False) -> Tuple[bool, List[Tuple[List[HeaderPair], bool, str]]]:
    all_res = []
    header.coverage = 0
    for i in receiver_list:
        reslist, coverage, status, reason = evaluate(i, header, output)
        all_res.append((reslist, status, reason))
        header.coverage += coverage
    return compare_result(all_res)


def timestr() -> str:
    import datetime
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')


def print_inconsistency(header: Header, reslist: List[Tuple[List[HeaderPair], bool, str]]) -> None:
    with open(timestr()+'.txt', 'w') as f:
        f.write(header.readable())
        for i in reslist:
            for j in i[0]:
                f.write(str(j))
            f.write('\n')
            f.write(str(i[1]) + ' ' + str(i[2]))
            f.write('\n\n')


if __name__ == '__main__':
    req_header_list: List[Header] = []
    # req_header_list.append(Header(r'POST /index.html HTTP/1.1\r\nconnection:close\r\nAccept-Encoding: gzip, deflate, br\r\nHost : www.114514.com\r\n Host: \r\n Host: 1919810\r\ncontent-length: 1\r\n\r\n1\r\n\r\n'))
    # req_header_list.append(Header(r'GET /analytics/track.png?url=https%3A%2F%2Ftechdocs.broadcom.com%2Fus%2Fen%2Fca-enterprise-software%2Flayer7-api-management%2Flive-api-creator%2F5-4%2Finvoking-apis%2Fhttp-headers.html&referrer=https%3A%2F%2Fwww.google.com%2F&e=pageView&t=HTTP%20Headers&uid=e95e476a-e759-11ea-beba-0242ac12000b&r=35807&sid=1661921107287298&taid=1661921107287133&internal=& HTTP/1.1\r\nAccept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-HK;q=0.6,de;q=0.5\r\nCache-Control: no-cache\r\nConnection: keep-alive\r\nCookie: _gid=GA1.2.2026648435.1661921106; _gat_UA-61260089-5=1; _ga=GA1.1.433543581.1661921106; connect.sid=s%3Atu1AsytKmpy06sZ6GqPi34COfRJg5Vnz.OYBbcXClGdyaWsaMraI2c; _ga_5DXTP07SYF=GS1.1.1661921106.1.0.1661921111.0.0.0; OptanonConsent=isIABGlobal=false&datestamp=Wed+Aug+31+2022+12%3A45%3A14+GMT%2B0800+(GMT%2B08%3A00)&version=6.9.0&hosts=&consentId=d7a89c99-4b87-4793-bd6e-507e0695f8fc&interactionCount=1&landingPath=https%3A%2F%2Ftechdocs.broadcom.com%2Fus%2Fen%2Fca-enterprise-software%2Flayer7-api-management%2Flive-api-creator%2F5-4%2Finvoking-apis%2Fhttp-headers.html&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1\r\nHost: searchunify.broadcom.com\r\nPragma: no-cache\r\nReferer: https://techdocs.broadcom.com/\r\nSec-Fetch-Dest: image\r\nSec-Fetch-Mode: no-cors\r\nSec-Fetch-Site: same-site\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36\r\nsec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"'))
    req_header_list.append(Header(
        '''GET /rfc/rfc7231 HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-HK;q=0.6,de;q=0.5
Cache-Control: no-cache
Connection: keep-alive
Host: www.rfc-editor.org
Pragma: no-cache
Referer: https://www.google.com/
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36
sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"''', multiline=True))
    req_header_list.append(Header(
        '''GET / HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-HK;q=0.6,de;q=0.5
Cookie: JSESSIONID=badCeyhYly; serverid=14256
Host: info.tsinghua.edu.cn
Proxy-Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36''', multiline=True))
    req_header_list.append(Header(
        '''GET /analytics/track.png?url=https%3A%2F%2Ftechdocs.broadcom.com%2Fus%2Fen%2Fca-enterprise-software%2Flayer7-api-management%2Flive-api-creator%2F5-4%2Finvoking-apis%2Fhttp-headers.html&referrer=https%3A%2F%2Fwww.google.com%2F&e=pageView&t=HTTP%20Headers&uid=e95e476a-e759-11ea-beba-0242ac12000b&r=35807&sid=1661921107287298&taid=1661921107287133&internal=& HTTP/1.1
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-HK;q=0.6,de;q=0.5
Cache-Control: no-cache
Connection: keep-alive
Cookie: _gid=GA1.2.2026648435.1661921106; _gat_UA-61260089-5=1; _ga=GA1.1.433543581.1661921106; connect.sid=s%3Atu1AsytKmpy06sZ6GqPi34COfRJg5Vnz.OYBbcXClGdyaWsaMraI2c; _ga_5DXTP07SYF=GS1.1.1661921106.1.0.1661921111.0.0.0; OptanonConsent=isIABGlobal=false&datestamp=Wed+Aug+31+2022+12%3A45%3A14+GMT%2B0800+(GMT%2B08%3A00)&version=6.9.0&hosts=&consentId=d7a89c99-4b87-4793-bd6e-507e0695f8fc&interactionCount=1&landingPath=https%3A%2F%2Ftechdocs.broadcom.com%2Fus%2Fen%2Fca-enterprise-software%2Flayer7-api-management%2Flive-api-creator%2F5-4%2Finvoking-apis%2Fhttp-headers.html&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1
Host: searchunify.broadcom.com
Pragma: no-cache
Referer: https://techdocs.broadcom.com/
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36
sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"''', multiline=True))
    req_header_list.append(Header(
        '''GET /videoplayback?expire=1661942918&ei=JegOY5yMI_-z2_gP4-i76Ak&ip=2a0e%3A6901%3A301%3A36%3A5054%3Aff%3Afe95%3A360b&id=o-AEo2ZhMnsKv0VZZ3lAiFQ_szmKjnmns_f39s1zVm87-o&itag=251&source=youtube&requiressl=yes&mh=9y&mm=31%2C26&mn=sn-axq7sn7l%2Csn-5hne6nsz&ms=au%2Conr&mv=u&mvi=16&pl=40&spc=lT-KhmgxszjvW4pXlXMW6cWtSp_PbO8jEPI0cDGOxn26&vprv=1&mime=audio%2Fwebm&ns=YzexES9gwhJ_h5m4I_XukV8H&gir=yes&clen=9534849&dur=599.421&lmt=1652492779352366&mt=1661920226&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=WEB&rbqsm=fr&txp=4532434&n=x4oh9S8fQ4GlSg&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cspc%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgNz7PX8yAHC1wJQhc5nIOR0TkqvT7NX1dIuQ22NVz4nQCIQClf9tSBWvHmwGjPHJQQL1YYHUWDgDNiBGtZjrO0tYbYg%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl&lsig=AG3C_xAwRAIgSuiq407BKCDsDIK3-ZeBAoa_xVl1ewRArqvx7Oh90J4CIA-VzXt-b2sO7LnbXC5Wygv28hkg66wpWmFp_4uLDFPX&alr=yes&cpn=vMa4WfJW8Q0ef1kY&cver=2.20220830.01.00&range=260205-479647&rn=7&rbuf=13124&pot=D9bWk9tpz8Lc1uuSplFfSnh88v97fTucnc1GfKhufxI9gjG9df_cLRlSciI3kFh7SoJXPAEVTaYdbyW12uijo-cNV6niQkP9IGcYe94sBi6Fby2D_AII8cqj-bN0APKr2g== HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-HK;q=0.6,de;q=0.5
Cache-Control: no-cache
Connection: keep-alive
Host: rr16---sn-axq7sn7l.googlevideo.com
Origin: https://www.youtube.com
Pragma: no-cache
Referer: https://www.youtube.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36
X-Client-Data: CJO2yQEIo7bJAQjAEInMnMAQjjy8wBCIbSzAEYranKAQ==
sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"
sec-ch-ua-arch: "x86"
sec-ch-ua-bitness: "64"
sec-ch-ua-full-version: "104.0.5112.102"
sec-ch-ua-full-version-list: "Chromium";v="104.0.5112.102", " Not A;Brand";v="99.0.0.0", "Google Chrome";v="104.0.5112.102"
sec-ch-ua-mobile: ?0
sec-ch-ua-model: 
sec-ch-ua-platform: "Windows"
sec-ch-ua-platform-version: "8.0.0"''', multiline=True))
    req_header_list.append(Header(
        '''GET /login.srf?wa=wsignin1.0&rpsnv=13&ct=1661921385&rver=7.3.6962.0&wp=MBI_SSL&wreply=https:%2F%2Fstorage.live.com%2Fstorageservice%2Fpassport%2Fauth.aspx%3Fsru%3Dhttps:%252f%252fstorage.live.com%252fusers%252f0xfa2b2c40fb8de010%252fmyprofile%252fexpressionprofile%252fprofilephoto:UserTileStatic%252fp&lc=1033&id=63539 HTTP/1.1
Accept: image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
Cookie: MSCC=183.172.120.117-CN
Host: login.live.com
Referer: https://www.bing.com/
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: cross-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70
sec-ch-ua: "Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"''', multiline=True))

    rcvl = get_receiver()
    mttl = get_mutator()
    inconsistency_flag = False
    mtt_round = 0

    for header in req_header_list:
        result, reslist = eval_list(rcvl, header, True)
        if not result:
            print('inconsistency found')
            inconsistency_flag = True
            print_inconsistency(header, reslist)
    if inconsistency_flag:
        print('inconsistency has been written to file')
    input('press any key to start mutating')

    while True:
        inconsistency_flag = False
        new_header_list = []
        for header in req_header_list:
            mtt: Mutator = choice(mttl)
            new_header: Header = deepcopy(header)
            new_header.coverage = 0
            mtt.mutate(new_header)
            result, reslist = eval_list(rcvl, new_header)
            if new_header.coverage > header.coverage or not result:
                new_header_list.append(new_header)
            else:
                new_header_list.append(header)
            if not result:
                print('inconsistency found')
                inconsistency_flag = True
                print_inconsistency(new_header, reslist)
        req_header_list = new_header_list
        mtt_round += 1
        print('mutating round: ', mtt_round)
        if inconsistency_flag:
            print('inconsistency has been written to file')
            input('press any key to continue')

    print(req_header_list[0].readable())
    for i in rcvl:
        reslist, coverage, status = i.get_parse(req_header_list[0])
        print('{:<35}'.format(i._name) +
              ('parse pass' if status else 'parse fail') + '\n')
        print('{:<35}{}'.format('Coverage', coverage))
        for j in reslist:
            print('{:<35}{}'.format(j.key, j.value))
        print('\n')
