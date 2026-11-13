# Hyprland's GUI toolkit; hyprland-guiutils (and later hyprpolkitagent) are built on it.

Name:           hyprtoolkit
Version:        0.6.0
Release:        3%{?dist}
Summary:        Modern C++ Wayland-native GUI toolkit

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprtoolkit
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hyprwayland-scanner-devel >= 0.4.0
BuildRequires:  pkgconfig(absl_flat_hash_map)
BuildRequires:  pkgconfig(aquamarine) >= 0.10.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.3.0
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprutils) >= 0.14.2
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

%description
A small, Wayland-native C++ GUI toolkit used by Hyprland's utilities.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig(aquamarine)
Requires:       pkgconfig(hyprgraphics)
Requires:       pkgconfig(hyprutils)

%description devel
Headers and pkg-config file for %{name}.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_libdir}/libhyprtoolkit.so.*

%files devel
%{_includedir}/hyprtoolkit/
%{_libdir}/libhyprtoolkit.so
%{_libdir}/pkgconfig/hyprtoolkit.pc

%changelog
* Fri Nov 13 2026 Jari Lehtinen <jari@feature.fi> - 0.6.0-3
- Rebuild against aquamarine 0.16.0 (soname 15)

* Sun Oct 18 2026 Christoph Pracht - 0.6.0-2
- Rebuild against aquamarine 0.15.1 (the -1 build linked an older libaquamarine)

* Fri Oct 16 2026 Christoph Pracht - 0.6.0-1
- Initial package
