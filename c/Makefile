all:	date_test date_profile

%.o : %.c
	gcc -o $@ -c $< -Wall -Wno-sometimes-uninitialized -std=c99 -O3

cheat.h:
	curl https://raw.githubusercontent.com/Tuplanolla/cheat/master/cheat.h -o cheat.h

cheats.h:
	curl https://raw.githubusercontent.com/Tuplanolla/cheat/master/cheats.h -o cheats.h

date_test: date_test.o date.o
	gcc -o date_test $^

date_profile:	date_profile.o date.o
	gcc -o date_profile $^

date_test.o: cheat.h cheats.h date.h
date_profile.o: date.h
date.o: date.h

