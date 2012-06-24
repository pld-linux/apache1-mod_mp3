%define		arname		mod_mp3
%define		mod_name	mp3
%define 	apxs		/usr/sbin/apxs
Summary:	MP3 Apache module
Summary(pl):	Modu� MP3 do Apache
Name:		apache-mod_mp3
Version:	0.31
Release:	1
License:	distributable
Group:		Networking/Daemons
Group(cs):	S�ov�/D�moni
Group(da):	Netv�rks/D�moner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	R�seau/Serveurs
Group(is):	Net/P�kar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	����/������
Group(sl):	Omre�ni/Stre�niki
Group(sv):	N�tverk/Demoner
Group(uk):	������/������
Source0:	ftp://ftp.tangent.org/pub/apache/%{arname}-%{version}.tar.gz
Source1:	%{arname}.conf
URL:		http://media.tangent.org/
Requires:	apache >= 1.3.12
Prereq:		grep
Prereq:		apache(EAPI) >= 1.3.12
Prereq:		%{_sbindir}/apxs
Provides:	%{arname}
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel >= 1.3.12
BuildRequires:	expat-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _pkglibdir      %(%{apxs} -q LIBEXECDIR)
%define         _sysconfdir     /etc/httpd

%prep
%setup -q -n %{arname}-%{version}

%description
This turns apache into your basic RIAA hating, but every college
student loving mp3 streaming server. It can play from a list of files,
either straight through or randomly. It can also be used to cache
mp3's into memory and have the server operate entirely from memory.
Enjoy, groove, mp3s not included.

%description -l pl
Ten pakiet zamienia Twojego Apache w znienawidzony przez RIAA, ale
uwielbiany przez student�w serwer strumieni MP3. Mo�e odtwarza� list�
plik�w, w kolejno�ci lub losowo. Mo�e by� tak�e u�yty do buforowania
plik�w mp3 w pami�ci, pozwalaj�c serwerowi operowa� wy��cznie na
pami�ci. Baw si� dobrze; pliki mp3 nie s� za��czone.

%build
./configure
%{__make} APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf README ChangeLog LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f %{_sysconfdir}/httpd.conf ] && \
	! grep -q "^Include.*/%{arname}.conf" %{_sysconfdir}/httpd.conf; then
		echo "Include %{_sysconfdir}/%{arname}.conf" >> %{_sysconfdir}/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi
	
%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	grep -E -v "^Include.*%{arname}.conf" %{_sysconfdir}/httpd.conf > \
	%{_sysconfdir}/httpd.conf.tmp
	mv -f %{_sysconfdir}/httpd.conf.tmp %{_sysconfdir}/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.gz faq.html support
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mod_mp3.conf
%attr(755,root,root) %{_pkglibdir}/mod_mp3.so
