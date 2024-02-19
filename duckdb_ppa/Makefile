all:
	@echo No.

bump:
	git add -p
	dch -D jammy
	git add -p
	debcommit

deb:
	dpkg-buildpackage -us -uc -b
	# debuild -S -sa

