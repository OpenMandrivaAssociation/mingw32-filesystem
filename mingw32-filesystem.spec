%define debug_package %{nil}

Name:           mingw32-filesystem
Version:        46
Release:        %mkrel 1
Summary:        MinGW base filesystem and environment

Group:          Development/Other
License:        GPLv2+
URL:            http://hg.et.redhat.com/misc/fedora-mingw--devel/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch

Source0:        mingw32-COPYING
Source1:        mingw32-macros.mingw32
Source2:        mingw32.sh
#Source3:        mingw32.csh
Source4:        mingw32-find-requires.sh
Source5:        mingw32-find-provides.sh
Source6:        mingw32-scripts.sh
Source7:        mingw32-rpmlint.config

Requires:       setup
Requires:       rpm
Requires:       rpmlint >= 0.84

BuildRequires:  rpmlint >= 0.84

# Note about 'Provides: mingw32(foo.dll)'
# ------------------------------------------------------------
#
# We want to be able to build & install mingw32 libraries without
# necessarily needing to install wine.  (And certainly not needing to
# install Windows!)  There is no requirement to have wine installed in
# order to use the mingw toolchain to develop software (ie. to
# compile more stuff on top of it), so why require that?
#
# So for expediency, this base package provides the "missing" DLLs
# from Windows.  Another way to do it would be to exclude these
# proprietary DLLs in our find-requires checking script - essentially
# it comes out the same either way.
#
Provides:       mingw32(gdi32.dll)
Provides:       mingw32(kernel32.dll)
Provides:       mingw32(ole32.dll)
Provides:       mingw32(mscoree.dll)
Provides:       mingw32(msvcrt.dll)
Provides:       mingw32(user32.dll)
Provides:       mingw32(wldap32.dll)
Provides:       mingw32(glut32.dll)
Provides:       mingw32(secur32.dll)


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%prep
%setup -q -c -T
cp %{SOURCE0} COPYING
sed 's/@VERSION@/%{version}/' < %{SOURCE4} > mingw32-find-requires.sh


%build
# nothing


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_libexecdir}/mingw32-scripts

mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_bindir}
for i in mingw32-configure mingw32-make; do
  ln -s %{_libexecdir}/mingw32-scripts $i
done
popd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
#install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.d/mingw32.macros

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint/

mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32

# GCC requires these directories, even though they contain links
# to binaries which are also installed in /usr/bin etc.  These
# contain Fedora native binaries.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/lib

# The MinGW system root which will contain Windows native binaries
# and Windows-specific header files, pkgconfig, etc.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/include/sys
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/lib/pkgconfig

mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/share/aclocal

# We don't normally package manual pages and info files, except
# where those are not supplied by a Fedora native package.  So we
# need to create the directories.
#
# Note that some packages try to install stuff in
#   /usr/i586-pc-mingw32/sys-root/mingw/man and
#   /usr/i586-pc-mingw32/sys-root/mingw/doc
# but those are both packaging bugs.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/share/info
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i586-pc-mingw32/sys-root/mingw/share/man/man{1,2,3,4,5,6,7,8,l,n}

# NB. NOT _libdir
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 mingw32-find-requires.sh $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/usr/lib/rpm


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING
%config(noreplace) %{_sysconfdir}/rpm/macros.d/mingw32.macros
%config(noreplace) %{_sysconfdir}/profile.d/mingw32.sh
#%config(noreplace) %{_sysconfdir}/profile.d/mingw32.csh
%config(noreplace) %{_sysconfdir}/rpmlint/mingw32-rpmlint.config
%{_bindir}/mingw32-configure
%{_bindir}/mingw32-make
%{_libexecdir}/mingw32-scripts
%{_prefix}/i586-pc-mingw32/
/usr/lib/rpm/mingw32-*
