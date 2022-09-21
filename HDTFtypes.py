class HeaderPair:
    key = ''
    value = ''
    has_colon = True

    def __init__(self, key: str = '', value: str = '', has_colon: bool = True):
        self.key = key
        self.value = value
        self.has_colon = has_colon

    def __str__(self):
        return self.key + (':' if self.has_colon else '') + self.value

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, HeaderPair):
            return False
        return self.key == __o.key and self.value == __o.value and self.has_colon == __o.has_colon


class Header:
    method = ''
    url = ''
    version = ''
    header_list = []

    '''
    def __init__(self, method: str, url: str, version: str):
        self.method = method
        self.url = url
        self.version = version
        self.header_list = []
        self.coverage = 0
    '''

    def __init__(self, header: str, multiline: bool = False):
        self.header_list = []
        self.coverage = 0
        '''
        if multiline:
            if '\r' in header:
                header.replace('\r', '\\r')
                header.replace('\n', '\\n')
            else:
                header.replace('\n', '\\r\\n')
        header = header.split('\\r\\n')
        '''
        if multiline:
            if '\r' in header:
                header = header.split('\r\n')
            else:
                header = header.split('\n')
        else:
            header = header.split('\\r\\n')
        self.method, self.url, self.version = header[0].split(' ')
        for i in header[1:]:
            if ':' in i:
                key, value = i.split(':', 1)
                self.add_header(key, value)
            else:
                self.add_header(i, '', False)
        '''
        http2_scheme = False
        colon_pos = 0
        for i in header[1:]:
            if ':' in i:
                for v in range(len(i)):
                    if i[v] == ' ':
                        continue
                    elif i[v] == ':':
                        http2_scheme = True
                        colon_pos = v
                        break
                    else:
                        http2_scheme = False
                        break
                if ':' in i[colon_pos+1:]:
                    pass
                else:
                    self.add_header(i, '', False)

            self.add_header(*i.split(':'))
        '''

    def add_header(self, key: str = '', value: str = '', has_colon: bool = True):
        self.header_list.append(HeaderPair(key, value, has_colon))

    def __str__(self) -> str:
        return self.method + ' ' + self.url + ' ' + self.version + '\\r\\n' + '\\r\\n'.join([str(i) for i in self.header_list])

    def readable(self) -> str:
        return self.method + ' ' + self.url + ' ' + self.version + '\r\n' + '\r\n'.join([str(i) for i in self.header_list])

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Header):
            return False
        return self.method == __o.method and self.url == __o.url and self.version == __o.version and self.header_list == __o.header_list
