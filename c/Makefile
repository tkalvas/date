all:	date_test date_profile

%.o : %.c
	gcc -o $@ -c $< -Wall -Wno-sometimes-uninitialized -std=c99 -O3

date_test: date_test.o date.o
	gcc -o date_test $^

date_profile:	date_profile.o date.o
	gcc -o date_profile $^
