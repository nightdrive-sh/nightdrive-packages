# Quickshell, the toolkit Nightdrive's top bar, menus, launcher and apps are written in. Fedora 44 has 0.2.1^git20260209,
# whose Hyprland module crashes on Hyprland 0.57 (special workspaces have an address there, not an id: two of them with
# windows and HyprlandWorkspace::insertToplevel gets a null pointer). 0.3.2 reads the new format (upstream fae96f1).
# Based on Fedora's spec (src.fedoraproject.org/rpms/quickshell, by Neal Gompa); leaves the COPR once Fedora has 0.3.2.

# No crash handler: it needs cpptrace, which Fedora doesn't have and COPR's builds can't fetch (no network).
# Fedora's 0.2.1 had none either (breakpad off).
%bcond crash_handler 0
# Not available in RHEL
%bcond x11 %[%{undefined rhel}]

# The tag's commit, for `qs --version` (the archive has no .git to read it from)
%global commit 4f508be500dea6e5732cc3d50382a0048b17e7b1

Name:               quickshell
Version:            0.3.2
Release:            1%{?dist}
Summary:            Flexible QtQuick based desktop shell toolkit
# Code is LGPL, Hyprland protocols are BSD-3-Clause, wlr protocols are HPND-sell-variant
License:            LGPL-3.0-or-later and BSD-3-Clause and HPND-sell-variant
URL:                https://quickshell.org/
Source:             https://git.outfoxxed.me/%{name}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Upstream 4befab5, after 0.3.2: a Hyprland workspace that changes its id keeps it in Quickshell (the same
# workspace-address work as fae96f1). Drop with the next release.
Patch:              quickshell-follow-workspace-id-changes.patch

BuildRequires:      cmake
BuildRequires:      cmake(Qt6Core)
BuildRequires:      cmake(Qt6Qml)
BuildRequires:      cmake(Qt6CorePrivate)
BuildRequires:      cmake(Qt6QuickPrivate)
BuildRequires:      cmake(Qt6ShaderTools)
BuildRequires:      cmake(Qt6WaylandClient)
BuildRequires:      desktop-file-utils
BuildRequires:      gcc-c++
BuildRequires:      ninja-build
BuildRequires:      pkgconfig(CLI11)
BuildRequires:      pkgconfig(glib-2.0)
BuildRequires:      pkgconfig(gbm)
BuildRequires:      pkgconfig(jemalloc)
BuildRequires:      pkgconfig(libdrm)
BuildRequires:      pkgconfig(libpipewire-0.3)
BuildRequires:      pkgconfig(pam)
BuildRequires:      pkgconfig(polkit-agent-1)
BuildRequires:      pkgconfig(wayland-client)
BuildRequires:      pkgconfig(wayland-protocols)
BuildRequires:      spirv-tools
# New in 0.3: screencopy's Vulkan backend
BuildRequires:      vulkan-headers
%if %{with x11}
BuildRequires:      pkgconfig(xcb)
%endif
%if %{with crash_handler}
BuildRequires:      cpptrace-devel
%endif

# Quickshell uses Qt's private API, which may change in any Qt release: it runs only with the Qt it was built against.
# Fedora rebuilds its own with every Qt update; this one holds a Qt update back until the COPR rebuilds it, rather
# than crash the desktop after one (Fedora's packaging guidelines for private Qt API).
%{?_qt6:Requires:   %{_qt6}%{?_isa} = %{_qt6_version}}
# Add undetectable runtime dependencies
Requires:           qt6-qtsvg%{?_isa}

Provides:           desktop-notification-daemon = %{version}-%{release}
Provides:           PolicyKit-authentication-agent = %{version}-%{release}

%description
Quickshell is a toolkit for building status bars, widgets,
lockscreens, and other desktop components using QtQuick.

It can be used alongside a Wayland compositor to build
a complete desktop environment.

%prep
%autosetup -p1 -n %{name}

%conf
%cmake  -GNinja \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_SKIP_INSTALL_RPATH=ON \
        -DDISTRIBUTOR="Nightdrive COPR" \
        -DINSTALL_QML_PREFIX=%{_lib}/qt6/qml \
        -DCRASH_HANDLER=%{?with_crash_handler:ON}%{!?with_crash_handler:OFF} \
        -DX11=%{?with_x11:ON}%{!?with_x11:OFF} \
        -DGIT_REVISION=%{commit} \
        %{nil}

%build
%cmake_build

%install
%cmake_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%license LICENSE*
%doc BUILD.md CONTRIBUTING.md README.md changelog/
%{_bindir}/qs
%{_bindir}/quickshell
%{_datadir}/applications/org.quickshell.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.quickshell.svg
%{_qt6_qmldir}/Quickshell/

%changelog
* Sat Nov 14 2026 Jari Lehtinen <jari@feature.fi> - 0.3.2-1
- 0.3.2 for Hyprland 0.57's workspace addresses, with upstream 4befab5
- No crash handler (cpptrace isn't in Fedora); vulkan-headers for screencopy
- Requires the Qt it was built against

* Mon Aug 31 2026 Jan Grulich <jgrulich@redhat.com> - 0.2.1^git20260209.dacfa9d-5
- Rebuild (qt6)

* Mon Feb 16 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.2.1^git20260209.dacfa9d-1
- Bump to git snapshot

* Sun Jan 04 2026 Neal Gompa <ngompa@fedoraproject.org> - 0.2.1-7
- Initial package based on ErrorNoInternet/quickshell COPR version
