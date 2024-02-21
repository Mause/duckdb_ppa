all:
	@echo No.

bump:
	git add -p
	dch --distribution jammy --upstream
	git add debian/changelog
	debcommit

deb:
	dpkg-buildpackage -us -uc -b
	# debuild -S -sa

