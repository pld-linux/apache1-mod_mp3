%define		mod_name	mp3
%define 	apxs		/usr/sbin/apxs1
Summary:	MP3 Apache module
Summary(pl):	Modu³ MP3 do Apache
Name:		apache1-mod_%{mod_name}
Version:	0.40
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.tangent.org/download/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	a36b25ee4db268df45a03231993e718d
Source1:	%{name}.conf
URL:		http://media.tangent.org/
BuildRequires:	%{apxs}
BuildRequires:	apache1-devel >= 1.3.12
BuildRequires:	libghttp-devel
PreReq:		apache1 >= 1.3.12
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)

%description
This turns apache into your basic RIAA hating, but every college
student loving mp3 streaming server. It can play from a list of files,
either straight through or randomly. It can also be used to cache
mp3's into memory and have the server operate entirely from memory.
Enjoy, groove, mp3s not included.

%description -l pl
Ten pakiet zamienia Twojego Apache w znienawidzony przez RIAA, ale
uwielbiany przez studentów serwer strumieni MP3. Mo¿e odtwarzaæ listê
plików, w kolejno¶ci lub losowo. Mo¿e byæ tak¿e u¿yty do buforowania
plików mp3 w pamiêci, pozwalaj±c serwerowi operowaæ wy³±cznie na
pamiêci. Baw siê dobrze; pliki mp3 nie s± za³±czone.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
./configure

%{__make} \
	APXS=%{apxs} \
	ACINCLUDEDIR="-I`%{apxs} -q INCLUDEDIR` `%{apxs} -q CFLAGS` %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install src/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f %{_sysconfdir}/apache.conf ] && \
	! grep -q "^Include.*/mod_%{mod_name}.conf" %{_sysconfdir}/apache.conf; then
		echo "Include %{_sysconfdir}/mod_%{mod_name}.conf" >> %{_sysconfdir}/apache.conf
fi
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	umask 027
	grep -E -v "^Include.*mod_%{mod_name}.conf" %{_sysconfdir}/apache.conf > \
		%{_sysconfdir}/apache.conf.tmp
	mv -f %{_sysconfdir}/apache.conf.tmp %{_sysconfdir}/apache.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog LICENSE faq.html support CONTRIBUTORS TODO utils/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%attr(755,root,root) %{_pkglibdir}/mod_mp3.so
