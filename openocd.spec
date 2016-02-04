Name:       openocd
Version:    0.9.0
Release:    3%{?dist}
Summary:    Debugging, in-system programming and boundary-scan testing for embedded devices

Group:      Development/Tools
License:    GPLv2
URL:        http://sourceforge.net/projects/openocd
Source0:    http://downloads.sourceforge.net/project/openocd/openocd/%{version}/%{name}-%{version}.tar.bz2
# not needed at all, even with jimtcl-0.75 
# Patch0:     openocd-jimtcl0_75.patch
Patch0:     openocd-sdcc.patch
Patch1:     openocd-detect-libftdi.patch

BuildRequires:  chrpath, libftdi-devel, libusbx-devel, jimtcl-devel, hidapi-devel, sdcc, libusb-devel, texinfo
Requires(post): info
Requires(preun):info

%description
The Open On-Chip Debugger (OpenOCD) provides debugging, in-system programming 
and boundary-scan testing for embedded devices. Various different boards, 
targets, and interfaces are supported to ease development time.

Install OpenOCD if you are looking for an open source solution for hardware 
debugging.

%prep
%setup -q
%patch0
%patch1
rm -rf jimtcl
rm -f src/jtag/drivers/OpenULINK/ulink_firmware.hex
cd doc
iconv -f iso8859-1 -t utf-8 openocd.info > openocd.info.conv
mv -f openocd.info.conv openocd.info

%build
pushd src/jtag/drivers/OpenULINK
make hex
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
install -p -m 644 contrib/99-openocd.rules %{buildroot}/%{_prefix}/lib/udev/rules.d/
chrpath --delete %{buildroot}/%{_bindir}/openocd

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files
%doc README COPYING AUTHORS ChangeLog NEWS TODO
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/OpenULINK/ulink_firmware.hex
%{_bindir}/%{name}
%{_prefix}/lib/udev/rules.d/99-openocd.rules
# doc
%{_infodir}/%{name}.info*.gz
%{_mandir}/man1/*

%changelog
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
