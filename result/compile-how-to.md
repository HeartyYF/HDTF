## llhttp

1. (Makefile) add `-fsanitize-coverage=trace-pc-guard` to `CFLAGS`
2. (Makefile, on windows) comment out `$(AR) rcs` part
3. `clang++ -g llhttp-receiver.cpp -c`
4. `clang++ trace-pc-guard-cb.cpp llhttp-receiver.o native/api.o native/http.o c/llhttp.o -fsanitize=address`

## http-parser

1. `clang++ -g -fsanitize-coverage=trace-pc-guard http_parser.c -c`
2. `clang++ -g http-parser-receiver.cpp -c`
3. `clang++ trace-pc-guard-cb.cpp http-parser-receiver.o http_parser.o -fsanitize=address`