CC=/home/spolstra/vertalerbouw/bin/xgcc

%.o: %.s
	$(CC) -c $<

%: %.s
	$(CC) -o $@ $<

all: acron clinpack dhrystone pi slalom whet

clean:
	rm -f acron clinpack dhrystone pi slalom whet
	rm -f *.o
	rm -f *.cycles *.output

