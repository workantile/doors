
install:
	install -v doors.py /usr/bin/doorsd
	install -m 644 -D -v doorsrc /etc/doorsrc
	install -m 644 -v doorsd.service /usr/lib/systemd/system/doorsd.service

uninstall:
	rm -v /usr/bin/doorsd /etc/doorsrc
