Name:       openocd
Version:    0.10.0
Release:    12%{?dist}
Summary:    Debugging, in-system programming and boundary-scan testing for embedded devices

License:    GPLv2
URL:        http://sourceforge.net/projects/openocd
Source0:    http://downloads.sourceforge.net/project/openocd/openocd/%{version}/%{name}-%{version}.tar.bz2
Patch0:     CVE-2018-5704-Prevent-some-forms-of-Cross-Protocol-Scripting.patch

BuildRequires:  gcc
BuildRequires:  chrpath, libftdi-devel, libusbx-devel, jimtcl-devel, hidapi-devel, sdcc, libusb-devel, texinfo, libjaylink-devel

%description
The Open On-Chip Debugger (OpenOCD) provides debugging, in-system programming 
and boundary-scan testing for embedded devices. Various different boards, 
targets, and interfaces are supported to ease development time.

Install OpenOCD if you are looking for an open source solution for hardware 
debugging.

%prep
%setup -q
%patch0 -p1 -b .cve
rm -rf jimtcl
rm -f src/jtag/drivers/OpenULINK/ulink_firmware.hex
pushd doc
iconv -f iso8859-1 -t utf-8 openocd.info > openocd.info.conv
mv -f openocd.info.conv openocd.info
popd
sed -i 's/MODE=.*/TAG+="uaccess"/' contrib/60-openocd.rules

%build
pushd src/jtag/drivers/OpenULINK
make PREFIX=sdcc hex
popd

%configure \
  --disable-werror \
  --enable-static \
  --disable-shared \
  --enable-dummy \
  --enable-ftdi \
  --enable-stlink \
  --enable-ti-icdi \
  --enable-ulink \
  --enable-usb-blaster-2 \
  --enable-jlink \
  --enable-osbdm \
  --enable-opendous \
  --enable-aice \
  --enable-vsllink \
  --enable-usbprog \
  --enable-rlink \
  --enable-armjtagew \
  --enable-cmsis-dap \
  --enable-parport \
  --enable-parport_ppdev \
  --enable-jtag_vpi \
  --enable-usb_blaster_libftdi \
  --enable-amtjtagaccel \
  --enable-ioutil \
  --enable-ep39xx \
  --enable-at91rm9200 \
  --enable-gw16012 \
  --enable-presto_libftdi \
  --enable-openjtag_ftdi \
  --enable-oocd_trace \
  --enable-buspirate \
  --enable-sysfsgpio \
  --enable-remote-bitbang \
  --disable-internal-jimtcl \
  --disable-doxygen-html \
  CROSS=
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -f %{buildroot}/%{_infodir}/dir
rm -f %{buildroot}/%{_libdir}/libopenocd.*
rm -rf %{buildroot}/%{_datadir}/%{name}/contrib
mkdir -p %{buildroot}/%{_prefix}/lib/udev/rules.d/
install -p -m 644 contrib/60-openocd.rules %{buildroot}/%{_prefix}/lib/udev/rules.d/60-openocd.rules
chrpath --delete %{buildroot}/%{_bindir}/openocd

%files
%doc README COPYING AUTHORS ChangeLog NEWS TODO
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/OpenULINK/ulink_firmware.hex
%{_bindir}/%{name}
%{_prefix}/lib/udev/rules.d/60-openocd.rules
# doc
%{_infodir}/%{name}.info*.gz
%{_mandir}/man1/*

%changelog
* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 0.10.0-12
- Remove obsolete requirements for %%post/%%preun scriptlets

* Thu Feb 21 2019 Jiri Kastner <jkastner@redhat.com> - 0.10.0-11
- fix for CVE-2018-5704 (RHBZ 1534844)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 22 2018 Jiri Kastner <jkastner@redhat.com> - 0.10.0-9
- fix openocd rules (RHBZ 1571599)

* Sat Sep 22 2018 Lubomir Rintel <lkundrak@v3.sk> - 0.10.0-8
- rebuild for jimtcl soname bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 24 2017 Jon Disnard <parasense@fedoraproject.org> - 0.10.0-3
- Update to use recent libjim.so bump

* Mon Mar 13 2017 Jiri Kastner <jkastner@redhat.com> - 0.10.0-2
- removed line with commented macro

* Wed Mar  8 2017 Jiri Kastner <jkastner@redhat.com> - 0.10.0-1
- update to 0.10.0 (RHBZ 1415527)
- added new dependency for libjaylink
- removed patches (RHBZ 1427016)

* Tue Mar  7 2017 Jiri Kastner <jkastner@redhat.com> - 0.9.0-6
- rebuild for jimtcl soname bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May 13 2016 Markus Mayer <lotharlutz@gmx.de> - 0.9.0-4
- Fix wrong udev rules bz#1177996

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Jiri Kastner <jkastner@redhat.com> - 0.9.0-1
- update to 0.9.0
- added texinfo dependency

* Mon Feb 02 2015 Markus Mayer <lotharlutz@gmx.de> - 0.8.0-6
- rebuild for jimtcl soname bump

* Mon Feb 02 2015 Markus Mayer <lotharlutz@gmx.de> - 0.8.0-5
- rebuild for jimtcl soname bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Markus Mayer <lotharlutz@gmx.de> - 0.8.0-2
- fix build issue with libftdi-1.1

* Tue Apr 29 2014 Markus Mayer <lotharlutz@gmx.de> - 0.8.0-1
- update to 0.8.0
- build ulink_firmware.hex during build
- enable new targets
- add udev rule

* Mon Mar 03 2014 Markus Mayer <lotharlutz@gmx.de> - 0.7.0-5
- rebuild for jimtcl soname bump
- add patch to adapt to new jimtcl API

* Sun Mar 02 2014 Markus Mayer <lotharlutz@gmx.de> - 0.7.0-4
- rebuild for jimtcl soname bump

* Sat Sep 07 2013 Markus Mayer <lotharlutz@gmx.de> - 0.7.0-3
- rebuild for jimtcl soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 22 2013 Markus Mayer <lotharlutz@gmx.de> - 0.7.0-1
- update to upstream release 0.7.0

* Thu May 02 2013 Markus Mayer <lotharlutz@gmx.de> - 0.6.1-1
- update to upstream release 0.6.1
- don't bundle jimtcl
- enable additional targets

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Dean Glazeski <dnglaze at gmail.com> - 0.6.0-2
- Enabling the stlink option

* Tue Sep 11 2012 Dean Glazeski <dnglaze at gmail.com> - 0.6.0-1
- RPM build for new release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 31 2012 Dennis Gilmore <dennis@ausil.us> - 0.5.0-3
- patch in flyswatter2 support

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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
