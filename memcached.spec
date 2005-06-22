# TODO
# - init script (see scripts/), but gotta test it first :-)
#
Summary:	A high-performance, distributed memory object caching system
Summary(pl):	Rozproszony system cache'owania obiektów o wysokiej wydajno¶ci
Name:		memcached
Version:	1.1.12
Release:	0.2
Epoch:		0
License:	GPL?
Vendor:		Brad Fitzpatrick <brad@danga.com>
Group:		Networking/Daemons
Source0:	http://www.danga.com/memcached/dist/%{name}-%{version}.tar.gz
# Source0-md5:	a1236dad33e9ac6c36d53faa8da61780
URL:		http://www.danga.com/memcached/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libevent-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A high-performance, distributed memory object caching system.

%description -l pl
Rozproszony system cache'owania obiektów o wysokiej wydajno¶ci.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1}
install memcached $RPM_BUILD_ROOT%{_sbindir}
install doc/memcached.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO doc/*.txt
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
