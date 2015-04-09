
install:
	install -v doors.py /usr/bin/doorsd
	install -D -v doorrc /etc/doorrc

uninstall:
	rm -v /usr/bin/doorsd /etc/doorrc
