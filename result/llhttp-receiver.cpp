#include <iostream>
#include <string>
#include "llhttp.h"
using namespace std;

#define MAX_LEN 2048

int on_message_begin(llhttp_t* parser)
{
    printf("parse start\n");
    return 0;
}

int on_url(llhttp_t* parser, const char* at, size_t length)
{
    char url[MAX_LEN];
    strncpy(url, at, length);
    url[length] = '\0';
    printf("on_url: %s\n", url);
    return 0;
}

int on_header_field(llhttp_t* parser, const char* at, size_t length)
{
    char header_field[MAX_LEN];
    strncpy(header_field, at, length);
    header_field[length] = '\0';
    printf("head field: %s\n", header_field);
    return 0;
}

int on_header_value(llhttp_t* parser, const char* at, size_t length)
{
    char header_value[MAX_LEN];
    strncpy(header_value, at, length);
    header_value[length] = '\0';
    printf("head value: %s\n", header_value);
    return 0;
}

int on_headers_complete(llhttp_t* parser)
{
    printf("on_headers_complete, major: %d, major: %d, keep-alive: %d, upgrade: %d\n", parser->http_major, parser->http_minor, llhttp_should_keep_alive(parser), parser->upgrade);
    return 0;
}

int on_body(llhttp_t* parser, const char* at, size_t length)
{
    char body[MAX_LEN];
    strncpy(body, at, length);
    body[length] = '\0';
    printf("on_body: %s\n", body);
    return 0;
}

int on_message_complete(llhttp_t* parser)
{
    printf("on_message_complete\n");
    return 0;
}

int main(int argc, char** argv)
{
    llhttp_t parser;
    llhttp_settings_t settings;
    llhttp_settings_init(&settings);
    llhttp_init(&parser, HTTP_REQUEST, &settings);

    settings.on_message_begin = on_message_begin;
    settings.on_url = on_url;
    settings.on_header_field = on_header_field;
    settings.on_header_value = on_header_value;
    settings.on_headers_complete = on_headers_complete;
    settings.on_body = on_body;
    settings.on_message_complete = on_message_complete;

    string req;
    if (argc == 1)
    {
        req = "POST /index.html HTTP/1.1\r\nconnection:close\r\nAccept-Encoding: gzip, deflate, br\r\nHost:www.114514.com\r\nHost: 1919810\r\ncontent-length: 1\r\n\r\n1\r\n\r\n";
    }
    else
    {
        bool flag = false;
        for (int i = 1; i < argc; i++)
        {
            for (int j = 0; argv[i][j] != '\0'; j++)
            {
                if (argv[i][j] == '\\')
                {
                    flag = true;
                    continue;
                }
                else if (flag)
                {
                    if (argv[i][j] == 'r')
                    {
                        req += '\r';
                    }
                    else if (argv[i][j] == 'n')
                    {
                        req += '\n';
                    }
                    else
                    {
                        req += '\\';
                        req += argv[i][j];
                    }
                    flag = false;
                }
                else
                {
                    req += argv[i][j];
                }
            }
            if (i != argc - 1)
            {
                req += ' ';
            }
        }
    }

    // string req = "POST /index.html HTTP/1.1\r\nconnection:close\r\nAccept-Encoding: gzip, deflate, br\r\nHost:www.114514.com\r\nHost: 1919810\r\ncontent-length: 1\r\n\r\n1\r\n\r\n";
    // cout<<req<<endl;
    // cout<<argc<<endl;
    int request_len = req.length();

    enum llhttp_errno err = llhttp_execute(&parser, req.data(), request_len);
    if (err != HPE_OK) {
       printf("Parse error: %s %s\n", llhttp_errno_name(err), parser.reason);
    }

    return 0;
}