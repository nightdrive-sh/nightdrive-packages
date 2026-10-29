# wayvnc, a VNC server for Hyprland and other wlroots-like compositors: Nightdrive's VNC Display (plugins/vnc-display)
# runs it. Fedora 44 has 0.9.1, which exits when a cursor capture fails (Hyprland fails one whenever the cursor grows)
# and which macOS's Screen Sharing can't log in to; 0.10 fixes both. Fedora's 0.10.2 is only in rawhide.
# wayvnc 0.10 needs neatvnc 1.0 and aml 1.0, whose sonames changed (.so.1), and Fedora 44's weston-libs-backend-vnc
# needs neatvnc's .so.0. So they aren't packaged here: both are built into wayvnc as static meson subprojects
# (Source1/2 in subprojects/), and Fedora's neatvnc and aml stay as they are.
# Goes from the COPR once Fedora's own wayvnc is 0.10 or later. The spec is rawhide's (src.fedoraproject.org/rpms/wayvnc)
# with the subprojects added; their BuildRequires are those of rawhide's neatvnc, without its examples' libpng and libsixel.

%global aml_version 1.0.0
%global nvnc_version 1.0.3

Name:           wayvnc
Version:        0.10.2
Release:        2%{?dist}
Summary:        A VNC server for wlroots based Wayland compositors

# wayvnc and aml are ISC; neatvnc is ISC, with a few BSD-2-Clause and BSD-3-Clause files
License:        ISC AND BSD-2-Clause AND BSD-3-Clause
URL:            https://github.com/any1/wayvnc
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/any1/aml/archive/v%{aml_version}/aml-%{aml_version}.tar.gz
Source2:        https://github.com/any1/neatvnc/archive/v%{nvnc_version}/neatvnc-%{nvnc_version}.tar.gz
# Hyprland 0.56 sends an opaque black cursor while the pointer is off the output: clients drew a black square (#1818)
Patch0:         wayvnc-uniform-cursor.patch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pam-devel
BuildRequires:  scdoc
BuildRequires:  turbojpeg-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(gmp)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(jansson)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(nettle)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xkbcommon) >= 1.0.0
BuildRequires:  pkgconfig(zlib)

Requires:       (sway >= 1.6 if sway)
Provides:       bundled(aml) = %{aml_version}
Provides:       bundled(neatvnc) = %{nvnc_version}

%description
This is a VNC server for wlroots based Wayland compositors. It
attaches to a running Wayland session, creates virtual input devices
and exposes a single display via the RFB protocol. The Wayland session
may be a headless one, so it is also possible to run wayvnc without a
physical display attached.

This build has neatvnc %{nvnc_version} and aml %{aml_version} built in.

%prep
%autosetup -p1
# wayvnc's meson.build takes subprojects/aml and subprojects/neatvnc over the system's when they are there (neatvnc
# finds the same aml); the top folder only, as meson flattens nested subprojects
mkdir -p subprojects/aml subprojects/neatvnc
tar -xzf %{SOURCE1} -C subprojects/aml --strip-components=1
tar -xzf %{SOURCE2} -C subprojects/neatvnc --strip-components=1
cp -p subprojects/aml/COPYING COPYING.aml
cp -p subprojects/neatvnc/COPYING COPYING.neatvnc

%build
# Static: aml then installs nothing, and neatvnc's library and header are left out of the install (--skip-subprojects)
%meson \
    -Daml:default_library=static \
    -Dneatvnc:default_library=static
%meson_build

%install
%meson_install --skip-subprojects

%check
%meson_test

%files
%license COPYING COPYING.aml COPYING.neatvnc
%doc README.md FAQ.md
%{_bindir}/%{name}
%{_bindir}/%{name}ctl
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/%{name}ctl.1.*

%changelog
* Thu Oct 29 2026 Jari Lehtinen <jari@feature.fi> - 0.10.2-2
- A cursor of a single colour is sent as transparent: Hyprland's opaque black one, sent while the pointer is off
  the output, showed on clients as a black square

* Thu Oct 29 2026 Jari Lehtinen <jari@feature.fi> - 0.10.2-1
- For Nightdrive's VNC Display on Fedora 44: neatvnc 1.0.3 and aml 1.0.0 built in (static), as their new sonames
  would replace the ones Fedora's weston-libs-backend-vnc needs
