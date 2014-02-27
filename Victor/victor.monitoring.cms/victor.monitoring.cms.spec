
%define place /var/www/DjangoProjects/victor

Summary: VICTOR MONITORING FOR CMS
Name: victor.monitoring.cms
Version: 0.5
Release: 0
License: GPL
Group: Application/Monitoring
URL: http://cms-popularity.cern.ch/victor
Source0: victor.monitoring.cms.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: httpd
Requires: Django
Requires: mod_wsgi
Requires: python-memcached

%description
Victor monitoring for CMS experiment  

%prep

%setup -n victor.monitoring.cms

%build

%install
%{__rm} -rf %{buildroot}

mkdir -p %{buildroot}/%{place}/
install lib/*.py %{buildroot}/%{place}/
install config/settings.py %{buildroot}/%{place}/
mkdir -p %{buildroot}/%{place}/templates
install templates/*.html %{buildroot}/%{place}/templates

mkdir -p %{buildroot}/%{place}/media
mkdir -p %{buildroot}/%{place}/media/css
mkdir -p %{buildroot}/%{place}/media/css/datatables
install media/css/datatables/*.css %{buildroot}/%{place}/media/css/datatables
mkdir -p %{buildroot}/%{place}/media/css/SpryMenuBar
install media/css/SpryMenuBar/*.css %{buildroot}/%{place}/media/css/SpryMenuBar
install media/css/SpryMenuBar/*.gif %{buildroot}/%{place}/media/css/SpryMenuBar
mkdir -p %{buildroot}/%{place}/media/css/ui-lightness
install media/css/ui-lightness/*.css %{buildroot}/%{place}/media/css/ui-lightness
mkdir -p %{buildroot}/%{place}/media/css/ui-lightness/images
install media/css/ui-lightness/images/*.png %{buildroot}/%{place}/media/css/ui-lightness/images

mkdir -p %{buildroot}/%{place}/media/images
install media/images/*.png %{buildroot}/%{place}/media/images/
install media/images/*.gif %{buildroot}/%{place}/media/images/

mkdir -p %{buildroot}/var/www/html/
install templates/index.html %{buildroot}/var/www/html/
mkdir -p %{buildroot}/var/www/html/images/
install media/images/*.png %{buildroot}/var/www/html/images/
install media/images/*.gif %{buildroot}/var/www/html/images/

mkdir -p %{buildroot}/%{place}/media/js
install media/js/*.js %{buildroot}/%{place}/media/js/

mkdir -p %{buildroot}/var/www/wsgi-scripts/victor/
install config/victor_wsgi.py %{buildroot}/var/www/wsgi-scripts/victor/

mkdir -p %{buildroot}/etc/httpd/conf.d/
install config/pop_victor.conf %{buildroot}/etc/httpd/conf.d/


%post


%postun

%clean
%{__rm} -rf %{buildroot}

%files

%{place}/*.py*
%{place}/templates/*.html
%{place}/media/css/datatables/*.css
%{place}/media/css/SpryMenuBar/*.css
%{place}/media/css/SpryMenuBar/*.gif
%{place}/media/css/ui-lightness/*.css
%{place}/media/css/ui-lightness/images/*.png
%{place}/media/js/*.js
%{place}/media/images/*.png
%{place}/media/images/*.gif
/var/www/html/index.html
/var/www/html/images/*.png
/var/www/html/images/*.gif
/var/www/wsgi-scripts/victor/victor_wsgi.py*
/etc/httpd/conf.d/pop_victor.conf


%changelog
