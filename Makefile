
install:
	install -v doors.py /usr/bin/doorsd
	install -D -v doorsrc /etc/doorsrc
	install -v doorsd.service /usr/lib/systemd/system/doorsd.service

uninstall:
	rm -v /usr/bin/doorsd /etc/doorsrc
