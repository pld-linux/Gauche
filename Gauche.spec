# $Id: Gauche.spec,v 1.4 2002-12-02 22:08:27 ankry Exp $
Summary:	Scheme script interpreter with multibyte character handling
Summary(pl):	Interpreter Scheme obs³uguj±cy wielobajtowe kodowanie znaków
Name:		Gauche
Version:	0.5.5
Release:	2
License:	BSD
Group:		Development/Languages
Source0:	http://telia.dl.sourceforge.net/sourceforge/gauche/%{name}-%{version}.tgz
Patch0:		%{name}-install.patch
BuildRequires:	gdbm-devel >= 1.8.0
BuildRequires:	slib
Requires:	slib
URL:		http://www.shiro.dreamhost.com/scheme/gauche/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gauche is a Scheme interpreter conforming Revised^5 Report on
Algorithmic Language Scheme. It is designed for rapid development of
daily tools like system management and text processing. It can handle
multibyte character strings natively. This package is compiled with
utf-8 as the native character encoding.

%description -l pl
Gauche jest interpreterem jêzyka Scheme zgodnym z "Revised^5 Report on
Algorithmic Language Scheme". Jest on zaprojektowany do szybkiego
tworzenia codziennych narzêdzi, jak zarz±dzania systemem lub
przetwarzanie tekstu. Potrafi on obs³ugiwaæ natywnie wielobajtowe
kodowanie znaków (jak na przyk³ad unicode). Ten pakiet jest
skompilowany z utf-8 jako natywnym kodowaniem znaków.

%package static
Summary:	Static version of Gauche runtime libary
Summary(pl):	Statyczna wersja biblioteki czasu wykonania Gauche
Group:		Development/Languages
Requires:	%{name} = %{version}

%description static
Static version of Gauche runtime libary.

%description static -l pl
Statyczna wersja biblioteki czasu wykonania Gauche.

%package dbm
Summary:	Gauche bindings for GDBM library
Summary(pl):	Wi±zania do biblioteki GDBM dla Gauche
Group:		Development/Languages
Requires:	%{name} = %{version}

%description dbm
Gauche bindings for GDBM library.

%description dbm -l pl
Wi±zania do biblioteki GDBM dla Gauche.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--enable-multibyte=utf-8 \
	--with-slib=%{_datadir}/guile/slib \
	--with-pthread

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

echo "echo $RPM_BUILD_ROOT\$(sh $(pwd)/src/gauche-config \"\$@\")" >src/gauche-config-install

%{__make} \
	LIB_INSTALL_DIR=$RPM_BUILD_ROOT%{_libdir} \
	BIN_INSTALL_DIR=$RPM_BUILD_ROOT%{_bindir} \
	DATA_INSTALL_DIR=$RPM_BUILD_ROOT%{_datadir} \
	GAUCHE_DATA_DIR=$RPM_BUILD_ROOT%{_datadir}/gauche \
	GAUCHE_ARCH_DIR=$RPM_BUILD_ROOT%{_libdir}/gauche \
	SCM_INSTALL_DIR=$RPM_BUILD_ROOT%{_datadir}/gauche/%{version}/lib \
        GAUCHE_CONFIG="sh $(pwd)/src/gauche-config-install" \
	install-rpm

install -d $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT%{_libdir}/gauche/%{version}/include/* $RPM_BUILD_ROOT%{_includedir}

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -d $RPM_BUILD_ROOT%{_aclocaldir}
install aclocal.m4 $RPM_BUILD_ROOT%{_aclocaldir}/gauche.m4

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
# creates slib catalog, if possible.
/usr/bin/gosh -u slib -e "(require 'logical)" -e "(exit 0)" > /dev/null 2>&1 || :
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog
%attr(755,root,root) %{_bindir}/gosh
%attr(755,root,root) %{_bindir}/gauche-config
%attr(755,root,root) %{_libdir}/libgauche.so
%attr(755,root,root) %{_libdir}/gauche/%{version}/*/*
%exclude %attr(755,root,root) %{_libdir}/gauche/%{version}/*/[nog]dbm.so
%dir %{_libdir}/gauche/site/%{version}/*
%{_datadir}/gauche/%{version}/lib
%exclude %{_datadir}/gauche/%{version}/lib/dbm*
%dir %{_datadir}/gauche/site/lib
%{_includedir}/gauche
%{_includedir}/gauche.h
%{_mandir}/man1/*
%{_aclocaldir}/*.m4

%files static
%defattr(644,root,root,755)
%{_libdir}/libgauche.a

%files dbm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gauche/%{version}/*/[nog]dbm.so
%{_datadir}/gauche/%{version}/lib/dbm
%{_datadir}/gauche/%{version}/lib/dbm.scm
