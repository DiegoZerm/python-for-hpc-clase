all: libhello.so

libhello.so: c_hello.c
	$(CC) -Wall -fPIC -c c_hello.c
	$(CC) -shared -o $@ c_hello.o

.PHONY: clean
clean:
	rm -f *.o *.so
