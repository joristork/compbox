CC=/home/spolstra/vertalerbouw/bin/xgcc

%.s: %.c
	$(CC) -S $<
%.o: %.s
	$(CC) -c $<

%: %.o
	$(CC) $<

all: acron clinpack dhrystone pi slalom whet

asm: acron.s clinpack.s dhrystone.s pi.s slalom.s whet.s

clean:
	rm -f acron clinpack dhrystone pi slalom whet
	rm -f *.o
	rm -f *.s
	rm -f *.cycles *.output

