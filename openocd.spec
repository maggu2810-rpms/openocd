Name:       openocd
Version:    0.5.0
Release:    1%{?dist}
Summary:    Debugging, in-system programming and boundary-scan testing for embedded devices

Group:      Development/Tools
License:    GPLv2
URL:        http://sourceforge.net/projects/openocd
Source0:    http://downloads.sourceforge.net/project/openocd/openocd/%{version}/%{name}-%{version}.tar.bz2

# Patch has been applied: http://openocd.zylin.com/#change,274
Patch0:     openocd.COPYING.patch
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  chrpath, libftdi-devel
Requires(post): info
Requires(preun):info

%description
The Open On-Chip Debugger (OpenOCD) provides debugging, in-system programming 
and boundary-scan testing for embedded devices.  Various different boards, 
targets, and interfaces are supported to ease development time.

Install OpenOCD if you are looking for an open source solution for hardware 
debugging.

%prep
%setup -q
%patch0
cd doc
iconv -f iso8859-1 -t utf-8 openocd.info > openocd.info.conv
mv -f openocd.info.conv openocd.info

%build
%configure \
  --disable-werror \
  --enable-static \
  --disable-shared \
  --enable-dummy \
  --enable-ft2232_libftdi \
  --enable-gw16012 \
  --enable-parport \
  --enable-parport_ppdev \
  --enable-presto_libftdi \
  --enable-amtjtagaccel \
  --enable-arm-jtag-ew \
  --enable-jlink \
  --enable-rlink \
  --enable-ulink \
  --enable-usbprog \
  --enable-vsllink \
  --enable-oocd_trace \
  --enable-ep39xx \
  --enable-at91rm9200 \
  --disable-doxygen-html \
  CROSS=
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -f %{buildroot}/%{_infodir}/dir
rm -f %{buildroot}/%{_libdir}/libopenocd.*
chrpath --delete %{buildroot}/%{_bindir}/openocd

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS ChangeLog NEWS TODO
%doc %{_datadir}/%{name}/contrib/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/scripts
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_infodir}/%{name}.info*.gz
%{_mandir}/man1/*

%changelog
* Wed Dec 14 2011 Dean Glazeski <dnglaze at gmail.com> - 0.5.0-1
- RPM build for new release.

* Sat Feb 13 2010 Dean Glazeski <dnglaze at gmail.com> - 0.4.0-1
- RPM build for new release.

* Fri Nov 13 2009 Dean Glazeski <dnglaze at gmail.com> - 0.3.1-1
- RPM build for bug fix for new release.

* Fri Oct 30 2009 Dean Glazeski <dnglaze at gmail.com> - 0.3.0-1
- RPM build for new release.

* Sat Aug 22 2009 Dean Glazeski <dnglaze at gmail.com> - 0.2.0-4
- Fixed duplicate file warnings for RPM build

* Fri Aug 21 2009 Dean Glazeski <dnglaze at gmail.com> - 0.2.0-3
- Updated spec file to match with suggestions from the review request
  (Bug 502130)
- Changed back to static library but removed the library from the distribution

* Fri Aug 14 2009 Dean Glazeski <dnglaze at gmail.com> - 0.2.0-2
- Switched to a shared object instead of a static library for the installation
  and added ldconfig commands
- Added some interfaces that were added to OpenOCD since 0.1.0

* Sat Aug 08 2009 Dean Glazeski <dnglaze at gmail.com> - 0.2.0-1
- Updated for new OpenOCD release

* Sat Jul 18 2009 Dean Glazeski <dnglaze at gmail.com> - 0.1.0-3
- Fixed the website URL and source0 URL

* Wed Jul 01 2009 Dean Glazeski <dnglaze at gmail.com> - 0.1.0-2
- Added some suggestions from package review (Bug 502130)
- Errors produced by RPM lint can be ignored (Bug 502112)

* Tue Mar 17 2009 Dean Glazeski <dnglaze at gmail.com> - 0.1.0-1
- Created initial package for Fedora
