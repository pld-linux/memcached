# TODO
# - memcached has -P option for pid, but root privs are dropped before
#   pid is written, so either run memcached as new uid or hack code to
#   write pidfile before changing uid, as rc-script removes pid on
#   shutdown anyway.
Summary:	A high-performance, distributed memory object caching system
Summary(pl.UTF-8):	Rozproszony, wysokiej wydajności system cache'owania obiektów
Name:		memcached
Version:	1.2.5
Release:	2
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.danga.com/memcached/dist/%{name}-%{version}.tar.gz
# Source0-md5:	8ac0d1749ded88044f0f850fad979e4d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.danga.com/memcached/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libevent-devel >= 1.1
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A high-performance, distributed memory object caching system.

%description -l pl.UTF-8
Rozproszony, wysokiej wydajności system cache'owania obiektów.

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
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1}

install memcached $RPM_BUILD_ROOT%{_sbindir}
install doc/memcached.1 $RPM_BUILD_ROOT%{_mandir}/man1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO doc/*.txt
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
