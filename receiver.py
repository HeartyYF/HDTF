import os
import io
from typing import List, Tuple

from HDTFtypes import Header, HeaderPair

rcvl = []


class Receiver:
    _name = 'receiverBaseClass'

    @classmethod
    def get_parse(cls, header: Header, output: bool = False) -> Tuple[List[HeaderPair], int, bool]:
        pass


def syscall_header(name: str, header: Header) -> List[str]:
    return io.TextIOWrapper(os.popen(name + ' "' + str(header) + '"').detach(), encoding='utf-8').readlines()


class llhttpReceiver(Receiver):
    _name = 'llhttp'

    @classmethod
    def get_parse(cls, header: Header, output: bool = False) -> Tuple[List[HeaderPair], int, bool, str]:
        data = syscall_header(cls._name + '.exe', header)
        coverage = 0
        result = []
        status = True
        cur_res = HeaderPair()
        cur_res_inuse = False
        reason = ''
        for i in data:
            if i.startswith('guard'):
                coverage += 1
            else:
                if output:
                    print('{:<35}'.format(cls._name) + i, end='')
                if i.startswith('head field: '):
                    if cur_res_inuse:
                        result.append(cur_res)
                        cur_res = HeaderPair()
                    cur_res.key = i[12:len(i)-1]
                elif i.startswith('head value: '):
                    cur_res.value = i[12:len(i)-1]
                    result.append(cur_res)
                    cur_res = HeaderPair()
                    cur_res_inuse = False
                elif i.startswith('Parse error: '):
                    status = False
                    reason = i[13:len(i)-1]
        if cur_res_inuse:
            result.append(cur_res)
        return result, coverage, status, reason


class httpParserReceiver(Receiver):
    _name = 'http_parser'

    @classmethod
    def get_parse(cls, header: Header, output: bool = False) -> Tuple[List[HeaderPair], int, bool]:
        data = syscall_header(cls._name + '.exe', header)
        coverage = 0
        result = []
        status = True
        cur_res = HeaderPair()
        cur_res_inuse = False
        reason = ''
        for i in data:
            if i.startswith('guard'):
                coverage += 1
            else:
                if output:
                    print('{:<35}'.format(cls._name) + i, end='')
                if i.startswith('head field: '):
                    if cur_res_inuse:
                        result.append(cur_res)
                        cur_res = HeaderPair()
                    cur_res.key = i[12:len(i)-1]
                elif i.startswith('head value: '):
                    cur_res.value = i[12:len(i)-1]
                    result.append(cur_res)
                    cur_res = HeaderPair()
                    cur_res_inuse = False
                elif i.startswith('Parse error: '):
                    status = False
                    reason = i[13:len(i)-1]
        if cur_res_inuse:
            result.append(cur_res)
        return result, coverage, status, reason


rcvl.append(llhttpReceiver)
rcvl.append(httpParserReceiver)


def get_receiver() -> List[Receiver]:
    return rcvl.copy()
