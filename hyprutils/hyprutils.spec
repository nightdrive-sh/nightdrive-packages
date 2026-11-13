# Shared utility library of the Hyprland stack. Fedora 44 ships 0.7.1; Hyprland 0.57 needs >= 0.14.3.

Name:           hyprutils
Version:        0.14.3
Epoch:          1
Release:        1%{?dist}
Summary:        Hyprland utilities library

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprutils
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(pixman-1)

%description
Small C++ library of utilities used across the Hyprland ecosystem.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

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
%{_libdir}/libhyprutils.so.*

%files devel
%{_includedir}/hyprutils/
%{_libdir}/libhyprutils.so
%{_libdir}/pkgconfig/hyprutils.pc

%changelog
* Fri Nov 13 2026 Jari Lehtinen <jari@feature.fi> - 1:0.14.3-1
- 0.14.3, which Hyprland 0.57 needs (string/UTF8 helpers, LC_MESSAGES in i18n; soname 13 as before)

* Mon Oct 19 2026 Jari Lehtinen <jari@feature.fi> - 1:0.14.2-2
- Epoch 1, as arcaneon/arcos's earlier builds had: an install from them otherwise never takes this package

* Fri Oct 16 2026 Christoph Pracht - 0.14.2-1
- Initial package
