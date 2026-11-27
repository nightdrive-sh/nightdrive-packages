# Hyprland compositor, ArcOS's desktop. Not packaged in Fedora 44.

# Commit of the v%%{version} tag; Hyprland embeds it in `hyprctl version`.
%global commit 11cbc6c577b84ffb1edf4df3fc5b6128c3ae6947
# Hyprland pins glaze 7.x and would download it at configure time; we ship that exact
# version as a second source so the build works offline (COPR builders have no network).
%global glaze_version 7.2.0

Name:           hyprland
Version:        0.57.2
Release:        4%{?dist}
Summary:        Dynamic tiling Wayland compositor

# Hyprland: BSD-3-Clause; bundled glaze (header-only, used by hyprpm/start-hyprland): MIT
License:        BSD-3-Clause AND MIT
URL:            https://github.com/hyprwm/Hyprland
Source0:        %{url}/archive/v%{version}/Hyprland-%{version}.tar.gz
Source1:        https://github.com/stephenberry/glaze/archive/v%{glaze_version}/glaze-%{glaze_version}.tar.gz
# Upstream 79d3046f (after 0.57.2): input capture sent a wheel tick as a continuous delta and as a value120 of that
# same delta (15 instead of 120), so Lan Mouse's Mac scrolled the wrong way (Nightdrive #3594). Drop it at 0.58.
Patch0:         hyprland-input-capture-wheel-value120.patch
# Upstream 1aa477bed3 (after 0.57.2): a monitor that gets no working mode stays enabled at 0x0, and the next blur
# refresh allocated its framebuffer anyway and aborted, so a USB-C display the DCP rejected crashed Hyprland in a
# loop, safe mode too (Nightdrive #3710). Drop it at 0.58.
Patch1:         hyprland-propRefresher-modeless-monitor.patch

BuildRequires:  cmake >= 3.30
BuildRequires:  gcc-c++
BuildRequires:  glslang-devel
BuildRequires:  hyprwayland-scanner-devel >= 0.3.10
BuildRequires:  hyprwire-devel
BuildRequires:  lua5.5-devel
BuildRequires:  udis86-devel >= 1.7.2
# 0.57.1's max_bpc backport uses aquamarine 0.16's API, though CMakeLists.txt still asks for 0.15.0
BuildRequires:  pkgconfig(aquamarine) >= 0.16.0
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprcursor) >= 0.1.7
BuildRequires:  pkgconfig(hyprgraphics) >= 0.5.1
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.8.0
BuildRequires:  pkgconfig(hyprlang) >= 0.6.7
BuildRequires:  pkgconfig(hyprutils) >= 0.14.3
BuildRequires:  pkgconfig(lcms2)
# Event sounds (new in 0.57)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(libinput) >= 1.29
BuildRequires:  pkgconfig(muparser)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.49
BuildRequires:  pkgconfig(wayland-server) >= 1.22.91
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon) >= 1.11.0

Requires:       xorg-x11-server-Xwayland
# hyprland-uwsm.desktop starts the session through uwsm.
Recommends:     uwsm
Provides:       bundled(glaze) = %{glaze_version}
# hyprland-uwsm.desktop was a subpackage of its own up to 0.56.2-1 (arcos): this package has it now
Provides:       hyprland-uwsm = %{version}-%{release}
Obsoletes:      hyprland-uwsm < %{version}-%{release}
# Quickshell before 0.3.2 (Fedora 44's 0.2.1 snapshot) crashes on 0.57's special workspaces, which have an address and no
# id there: Nightdrive's bar and lock run on it. Nightdrive's stable setup takes only the Hyprland stack from this COPR,
# not its quickshell, so dnf keeps such a machine on 0.56.2 instead of breaking its desktop.
Conflicts:      quickshell < 0.3.2

%description
Hyprland is a dynamic tiling Wayland compositor with animations, configured in Lua.

%package devel
Summary:        Headers for building Hyprland plugins
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig(aquamarine)
Requires:       pkgconfig(hyprcursor)
Requires:       pkgconfig(hyprgraphics)
Requires:       pkgconfig(hyprlang)
Requires:       pkgconfig(hyprutils)
Requires:       pkgconfig(libdrm)
Requires:       pkgconfig(pixman-1)
Requires:       pkgconfig(xkbcommon)

%description devel
Headers and pkg-config file for building Hyprland plugins.

%prep
%autosetup -n Hyprland-%{version} -p1
tar -xzf %{SOURCE1}

%build
export GIT_COMMIT_HASH=%{commit}
export GIT_TAG=v%{version}
export GIT_BRANCH=main
export GIT_DIRTY=clean
%cmake \
    -DBUILD_TESTING=OFF \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DFETCHCONTENT_SOURCE_DIR_GLAZE=%{_builddir}/Hyprland-%{version}/glaze-%{glaze_version}
%cmake_build

%install
%cmake_install
# The bundled glaze is a header-only build dependency; don't ship its headers.
rm -rf %{buildroot}%{_includedir}/glaze %{buildroot}%{_datadir}/glaze %{buildroot}%{_libdir}/cmake/glaze

%files
%license LICENSE
%{_bindir}/Hyprland
%{_bindir}/hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_bindir}/start-hyprland
%{_datadir}/hypr/
%{_datadir}/wayland-sessions/hyprland.desktop
%{_datadir}/wayland-sessions/hyprland-uwsm.desktop
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_libdir}/systemd/user/hyprland-session.target
%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*
%{bash_completions_dir}/hyprpm
%{fish_completions_dir}/hyprpm.fish
%{zsh_completions_dir}/_hyprpm

%files devel
%{_includedir}/hyprland/
%{_datadir}/pkgconfig/hyprland.pc

%changelog
* Fri Nov 27 2026 Jari Lehtinen <jari@feature.fi> - 0.57.2-4
- Backport upstream 1aa477bed3: skip a monitor without a mode when refreshing blur framebuffers (a display
  with no working mode crashed Hyprland in a loop)

* Wed Nov 25 2026 Jari Lehtinen <jari@feature.fi> - 0.57.2-3
- Backport upstream 79d3046f: input capture forwards wheel ticks as value120 only (Lan Mouse scrolled
  the wrong way on a Mac)

* Sat Nov 14 2026 Jari Lehtinen <jari@feature.fi> - 0.57.2-2
- Conflicts with quickshell < 0.3.2, whose Hyprland IPC crashes on 0.57's special workspaces

* Fri Nov 13 2026 Jari Lehtinen <jari@feature.fi> - 0.57.2-1
- 0.57.2: needs hyprutils 0.14.3, aquamarine 0.16.0 and libcanberra; installs hyprland-session.target;
  hyprctl's shell completions are gone upstream (hyprpm keeps its own)

* Sun Oct 18 2026 Jari Lehtinen <jari@feature.fi> - 0.56.2-3
- Obsoletes hyprland-uwsm, whose session file this package has now (Nightdrive COPR)

* Sun Oct 18 2026 Christoph Pracht - 0.56.2-2
- Rebuild against aquamarine 0.15.1 (the -1 build linked an older libaquamarine)

* Fri Oct 16 2026 Christoph Pracht - 0.56.2-1
- Initial package
