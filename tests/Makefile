all: fmasterslave fmasterslave_new cmasterslave cmasterslave_new

fmasterslave: fmasterslave.f
	mpifort -I../include fmasterslave.f -L../src -ltorc -lpthread -lm -o fmasterslave

fmasterslave_new: fmasterslave_new.f
	mpifort -I../include fmasterslave_new.f -L../src -ltorc -lpthread -lm -o fmasterslave_new

cmasterslave_new: cmasterslave_new.c
	mpicc -I../include -std=gnu17 cmasterslave_new.c -L../src -ltorc -lpthread -lm -o cmasterslave_new

cmasterslave: cmasterslave.c
	mpicc -I../include -std=gnu17 cmasterslave.c -L../src -ltorc -lpthread -lm -o cmasterslave


clean:
	rm -f fmasterslave fmasterslave_new cmasterslave cmasterslave_new
	rm -rf *.dSYM
