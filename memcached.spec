#
# TODO: init script (see scripts/),
# but gotta test it first :-)
#
Summary:	A high-performance, distributed memory object caching system
Summary(pl):	Rozproszony system cachowania obiektów o wysokiej wydajno¶ci
Name:		memcached
Version:	1.1.11
Release:	0.1
Epoch:		0
License:	GPL?
Vendor:		Brad Fitzpatrick <brad@danga.com>
Group:		Networking/Daemons
Source0:	http://www.danga.com/memcached/dist/%{name}-%{version}.tar.gz
# Source0-md5:	f42301c02e4223a1f2298dd3d3c30d90
URL:		http://www.danga.com/memcached/
BuildRequires:	libevent-devel
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A high-performance, distributed memory object caching system.

%description -l pl
Rozproszony system cachowania obiektów o wysokiej wydajno¶ci.

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install memcached $RPM_BUILD_ROOT%{_bindir}
install doc/memcached.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO doc/*.txt
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
