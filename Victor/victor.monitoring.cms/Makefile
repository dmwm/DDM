.PHONY: rpm tar rpmbuild

rpmmacros=$(HOME)/.rpmmacros

rpm: $(rpmmacros) tar rpmbuild

tar: $(rpmmacros)
	tar -C .. \
	--wildcards --exclude \*\.svn\* --exclude \*\~ \
	-zcf "`rpm --eval %{_sourcedir}`/victor.monitoring.cms.tar.gz" victor.monitoring.cms
	
rpmbuild: $(rpmmacros)
	rpmbuild -ba victor.monitoring.cms.spec