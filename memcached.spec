# NOTE
# - release notes: https://github.com/memcached/memcached/wiki/ReleaseNotes
# TODO
# - fix x32 build failure:
#crawler.c: In function 'crawler_metadump_eval':
#crawler.c:229:13: warning: format '%ld' expects argument of type 'long int', but argument 5 has type 'time_t {aka long long int}' [-Wformat=]
#             "key=%s exp=%ld la=%llu cas=%llu fetch=%s\n",
#             ^
#crawler.c:229:13: warning: format '%ld' expects argument of type 'long int', but argument 5 has type 'time_t {aka long long int}' [-Wformat=]

Summary:	A high-performance, distributed memory object caching system
Summary(pl.UTF-8):	Rozproszony, wysokiej wydajności system cache'owania obiektów
Name:		memcached
Version:	1.5.12
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.memcached.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	63858fd0a720f870f1e927ac3c6d9b05
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.tmpfiles
URL:		https://memcached.org/about
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libevent-devel >= 1.1
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
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

%define		_bindir	%{_sbindir}

%description
A high-performance, distributed memory object caching system.

%description -l pl.UTF-8
Rozproszony, wysokiej wydajności system cache'owania obiektów.

%package devel
Summary:	Files needed for development using memcached protocol
Group:		Development/Libraries
# does not require base

%description devel
Install memcached-devel if you are developing C/C++ applications that
require access to the memcached binary include files.

%prep
%setup -q

sed -nie '1,/^$/p' ChangeLog

%ifarch x32
%{__sed} -i -e 's/-Werror//' configure.ac
%endif

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_repcached:--enable-replication} \
	--disable-coverage
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},/var/run/memcached} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} install \
	INSTALL="%{__install} -p" \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%pre
%groupadd -g 209 %{name}
%useradd -u 209 -d /usr/share/empty -g %{name} -c "Memcached Daemon" %{name}

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
%doc AUTHORS README.md ChangeLog doc/*.txt
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
%{_mandir}/man1/memcached.1*
%dir %attr(770,root,memcached) /var/run/memcached
%{systemdtmpfilesdir}/%{name}.conf

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
