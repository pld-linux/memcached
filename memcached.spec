Summary:	A high-performance, distributed memory object caching system
Summary(pl.UTF-8):	Rozproszony, wysokiej wydajności system cache'owania obiektów
Name:		memcached
Version:	1.2.6
Release:	3
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.danga.com/memcached/dist/%{name}-%{version}.tar.gz
# Source0-md5:	200d22f7ac2d114f74a6904552e9eb70
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.danga.com/memcached/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libevent-devel >= 1.1
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.4.1.23
Provides:	group(memcached)
Provides:	user(memcached)
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
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},/var/run/memcached}
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1}

install memcached $RPM_BUILD_ROOT%{_sbindir}
install doc/memcached.1 $RPM_BUILD_ROOT%{_mandir}/man1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%pre
%groupadd -g 209 %{name}
%useradd -u 209 -d /usr/share/empty -g %{name} -c "Memcached User" %{name}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO doc/*.txt
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%{_mandir}/man1/memcached.1*
%dir %attr(770,root,memcached) /var/run/memcached
