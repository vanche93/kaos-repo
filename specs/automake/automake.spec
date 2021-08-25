################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

%global _configure_gnuconfig_hack 0

%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Automake::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Automake::

################################################################################

Summary:          A GNU tool for automatically creating Makefiles
Name:             automake
Version:          1.16.2
Release:          0%{?dist}
License:          GPLv2+ and GFDL and Public Domain and MIT
Group:            Development/Tools
URL:              https://www.gnu.org/software/automake/

Source0:          https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source2:          https://git.savannah.gnu.org/cgit/config.git/plain/config.sub
Source3:          https://git.savannah.gnu.org/cgit/config.git/plain/config.guess

Source100:        checksum.sha512

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:         perl(Thread::Queue)
Requires:         perl(threads)

BuildRequires:    autoconf >= 2.65 make coreutils findutils help2man
BuildRequires:    perl-generators perl-interpreter perl(Thread::Queue)
BuildRequires:    perl(threads)

BuildArch:        noarch

Provides:         %{name} = %{version}-%{release}

################################################################################

%description
Automake is a tool for automatically generating Makefile.in files compliant with
the GNU Coding Standards.

You should install Automake if you are developing software and would like to use
its ability to automatically generate GNU standard Makefiles.

################################################################################

%prep
%{crc_check}

%setup -q

for file in %{SOURCE2} %{SOURCE3} ; do
  for dest in $(find -name "$(basename "$file")"); do
    cp "$file" "$dest"
  done
done

%build
%configure
%{__make} %{?_smp_mflags}

cp m4/acdir/README README.aclocal
cp contrib/multilib/README README.multilib

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc COPYING*
%doc AUTHORS README THANKS NEWS README.aclocal README.multilib
%doc %{_defaultdocdir}/%{name}/amhello-1.0.tar.gz
%exclude %{_datadir}/aclocal
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/automake-*
%{_datadir}/aclocal-*
%{_mandir}/man1/*

################################################################################

%changelog
* Sat May 23 2020 Anton Novojilov <andy@essentialkaos.com> - 1.16.2-0
- Initial build for kaos repository
