# TODO
#  - with mysql and pgsql?
%define		mod_name	mp3
%define 	apxs		/usr/sbin/apxs1
Summary:	MP3 Apache module
Summary(pl.UTF-8):	Moduł MP3 do Apache
Name:		apache1-mod_%{mod_name}
Version:	0.40
Release:	4
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.tangent.org/download/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	a36b25ee4db268df45a03231993e718d
Source1:	%{name}.conf
URL:		http://media.tangent.org/
BuildRequires:	apache1-apxs
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	libghttp-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	%{apxs}
Requires(triggerpostun):	grep
Requires(triggerpostun):	sed >= 4.0
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_mp3 <= 0.40
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This turns apache into your basic RIAA hating, but every college
student loving MP3 streaming server. It can play from a list of files,
either straight through or randomly. It can also be used to cache
MP3's into memory and have the server operate entirely from memory.
Enjoy, groove, MP3s not included.

%description -l pl.UTF-8
Ten pakiet zamienia Twojego Apache w znienawidzony przez RIAA, ale
uwielbiany przez studentów serwer strumieni MP3. Może odtwarzać listę
plików, w kolejności lub losowo. Może być także użyty do buforowania
plików MP3 w pamięci, pozwalając serwerowi operować wyłącznie na
pamięci. Baw się dobrze; pliki MP3 nie są załączone.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
./configure \
	--with-apxs=%{apxs} \
	%{?debug:--with-debug}

%{__make} \
	APXS=%{apxs} \
	AINCLUDEDIR="-I$(%{apxs} -q INCLUDEDIR) $(%{apxs} -q CFLAGS) %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install src/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- %{name} < 0.40-2.1
if grep -q '^Include conf\.d/\*\.conf' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	sed -i -e '
		/^Include.*mod_%{mod_name}\.conf/d
	' /etc/apache/apache.conf
else
	# they're still using old apache.conf
	sed -i -e '
		s,^Include.*mod_%{mod_name}\.conf,Include %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf,
	' /etc/apache/apache.conf
fi
%service -q apache restart

%files
%defattr(644,root,root,755)
%doc README ChangeLog LICENSE faq.html support CONTRIBUTORS TODO utils/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_mp3.so
