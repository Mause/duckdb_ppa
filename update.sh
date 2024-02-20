#!/bin/sh -e
# called with '--upstream-version' <version> <file>
uupdate "$@"
package=`dpkg-parsechangelog | sed -n 's/^Source: //p'`
cd ../$package-$2
debuild
