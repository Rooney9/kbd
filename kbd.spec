Summary:	Linux console utilities
Summary(ko):	�ܼ��� �����ϴ� ���� (�ۼ���, ���� �͹̳�, �� �ۿ�)
Summary(pl):	Narz�dzia do obs�ugi konsoli
Name:		kbd
Version:	1.09
Release:	1
License:	GPL
Group:		Applications/Console
Source0:	ftp://ftp.win.tue.nl/pub/linux-local/utils/kbd/%{name}-%{version}.tar.gz
# Source0-md5:	493ff483b8b536fef5aa60ad108b647c
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source3-md5:	93c72a27e4fdeba23cb62d62343e9483
Source4:	lat2u-16.psf.gz
# Source4-md5:	dc90a9bcff858175beea32a9b3bebb33
Source5:	lat2u.sfm.gz
# Source5-md5:	8ac4abc169fa1236fc3e64163c043113
Source6:	console.sh
Source7:	console.csh
Source8:	console-man-pages.tar.bz2
# Source8-md5:	3790029011f9f2e299ea4e56df0fa0f9
Source9:	%{name}-pl1.kmap.gz
# Source9-md5:	18d119b54f3fbacbfb561d81ac1a9472
Source10:	%{name}-mac-pl.kmap.gz
# Source10-md5:	47f26751e2d633e0d663e5774d5c1516
# MIME-decoded from po/kbd.sv
Source11:	%{name}-1.06.sv.po
# new
Source12:	%{name}-pl.po
Source13:	pl3.map.gz
Patch0:		%{name}-install.patch
Patch1:		%{name}-sparc.patch
Patch2:		%{name}-compose.patch
Patch3:		%{name}-compat-suffixes.patch
Patch4:		%{name}-unicode_start.patch
Patch5:		%{name}-posixsh.patch
Patch6:		%{name}-DESTDIR.patch
Patch7:		%{name}-missing-nls.patch
Patch8:		%{name}-gcc33.patch
Patch9:		%{name}-po.patch
URL:		http://www.win.tue.nl/~aeb/linux/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	sed
Requires:	open
Requires:	util-linux
Provides:	console-data
Provides:	console-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	util-linux < 2.11
Conflicts:	man-pages < 1.43-5
Obsoletes:	console-data
Obsoletes:	console-tools
Obsoletes:	console-tools-devel
Obsoletes:	console-tools-static

%description
This package contains utilities to load console fonts and keyboard
maps. It also includes a number of different fonts and keyboard maps.

%description -l pl
Pakiet zawiera narz�dzia do �adowania font�w konsolowych oraz map
klawiatury. Dodaktowo do��czono znaczn� liczb� r�nych font�w i map.

%prep
%setup -q
cp -f %{SOURCE11} po/sv.po
cp -f %{SOURCE12} po/pl.po
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

sed -e 's@ ru\.\(po\|gmo\)$@ ru.\1 sv.\1 pl.\1@' po/Makefile > po/Makefile.tmp
mv -f po/Makefile.tmp po/Makefile

%build
./configure \
	--datadir=%{_datadir} \
	--mandir=%{_mandir}
%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{profile.d,rc.d/init.d,sysconfig}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

ln -sf /bin/loadkeys $RPM_BUILD_ROOT%{_bindir}/loadkeys

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/console
%ifarch sparc sparc64
sed 's/KEYTABLE=pl2/KEYTABLE=sunkeymap/' %{SOURCE2} > $RPM_BUILD_ROOT/etc/sysconfig/console
%else
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/console
%endif

install %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/consolefonts/lat2u-16.psfu.gz
gunzip -c %{SOURCE5} >$RPM_BUILD_ROOT%{_datadir}/unimaps/lat2u.uni

install %{SOURCE9} $RPM_BUILD_ROOT%{_datadir}/keymaps/i386/qwerty/pl1.map.gz
install %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/keymaps/mac/all/mac-pl.map.gz
install %{SOURCE13} $RPM_BUILD_ROOT%{_datadir}/keymaps/i386/qwerty/pl3.map.gz

install %{SOURCE6} $RPM_BUILD_ROOT/etc/profile.d
install %{SOURCE7} $RPM_BUILD_ROOT/etc/profile.d

bzip2 -dc %{SOURCE3} | tar xvf - -C $RPM_BUILD_ROOT%{_mandir}
bzip2 -dc %{SOURCE8} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

rm -f doc/{*,*/*}.sgml

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add console

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del console
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGES CREDITS README doc/*.txt
%attr(754,root,root) /etc/rc.d/init.d/console
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/console
%attr(755,root,root) /etc/profile.d/console.*

%attr(755,root,root) /bin/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/console*
%{_datadir}/keymaps
%{_datadir}/unimaps

%{_mandir}/man?/*
%lang(cs) %{_mandir}/cs/man?/*
%lang(de) %{_mandir}/de/man?/*
%lang(es) %{_mandir}/es/man?/*
%lang(fi) %{_mandir}/fi/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(hu) %{_mandir}/hu/man?/*
%lang(it) %{_mandir}/it/man?/*
%lang(ja) %{_mandir}/ja/man?/*
%lang(ko) %{_mandir}/ko/man?/*
%lang(pl) %{_mandir}/pl/man?/*
%lang(pt) %{_mandir}/pt/man?/*
%lang(ru) %{_mandir}/ru/man?/*