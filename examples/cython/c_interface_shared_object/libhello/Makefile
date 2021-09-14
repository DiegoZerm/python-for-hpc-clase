all: libhello.so

libhello.so: c_hello.c
	gcc -Wall -fPIC -c c_hello.c
	gcc -shared -o $@ c_hello.o

.PHONY: clean
clean:
	rm -f *.o *.so
