# Hyprland's rendering backend library (DRM/KMS, libinput, Wayland nested).

Name:           aquamarine
Version:        0.16.0
Release:        1%{?dist}
Summary:        Very light Linux rendering backend library

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/aquamarine
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hwdata-devel
BuildRequires:  hyprwayland-scanner-devel >= 0.4.0
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprutils) >= 0.8.0
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput) >= 1.26.0
BuildRequires:  pkgconfig(libseat) >= 0.8.0
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
Aquamarine is a very light Linux rendering backend library used by Hyprland. It provides
DRM/KMS, libinput and nested Wayland backends.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

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
%{_libdir}/libaquamarine.so.*

%files devel
%{_includedir}/aquamarine/
%{_libdir}/libaquamarine.so
%{_libdir}/pkgconfig/aquamarine.pc

%changelog
* Fri Nov 13 2026 Jari Lehtinen <jari@feature.fi> - 0.16.0-1
- 0.16.0, which Hyprland 0.57.1 and later need (setMaxBpc); soname 14 -> 15, so hyprland
  and hyprtoolkit are rebuilt against it

* Fri Oct 16 2026 Christoph Pracht - 0.15.1-1
- Initial package
