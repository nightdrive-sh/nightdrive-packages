# Deck, a Spotify player: Nightdrive's Deck app (plugins/deck) runs it. Packaged so that installing Deck doesn't compile
# Rust on every machine (a few minutes and a toolchain). Its crates aren't Fedora's: they are vendored from Deck's
# Cargo.lock into Source1 by sources.sh when the SRPM is made (.copr/Makefile), and the build runs offline.
# A new Deck release (its tag vX.Y.Z pushed): Version below, Release back to 1, a %%changelog entry (Deck's CLAUDE.md ›
# Releases).

Name:           deck
Version:        0.1.1
Release:        1%{?dist}
Summary:        Spotify player for the terminal, built around your own album shelf

# Deck is MIT; the vendored crates' licenses are listed in LICENSE.dependencies
License:        MIT
URL:            https://github.com/nightdrive-sh/deck
Source0:        %{url}/archive/v%{version}/deck-%{version}.tar.gz
Source1:        deck-%{version}-vendor.tar.gz

BuildRequires:  cargo-rpm-macros
BuildRequires:  gcc
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(openssl)

%description
Deck plays Spotify (Premium) through librespot: your own album shelf, a weekly Curated list of albums made with Claude
Code, genre radio and search. It runs in a terminal, or as a player that Nightdrive's Deck window talks to.

%prep
%autosetup -n deck-%{version} -a 1
# .cargo/config.toml: the vendored crates, offline, and Fedora's rpm profile
%cargo_prep -v vendor

# Cargo itself with Fedora's flags and profile, not %%cargo_build: that sets RUSTC_BOOTSTRAP=1, and rustix 0.37 (a
# librespot dependency) then takes the compiler for a nightly and uses attributes today's Rust no longer has
%build
RUSTFLAGS="%{build_rustflags}" cargo build -j%{_smp_build_ncpus} --profile rpm --locked --offline
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest

%install
install -Dm755 target/rpm/deck %{buildroot}%{_bindir}/deck
install -Dm644 assets/deck.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/deck.svg

%check
# Deck's tests touch neither the network nor the home folder (Deck's CLAUDE.md); the Spotify ones are #[ignore]d
# failed_save_rolls_back makes a folder read-only, which root (test-build.sh's container) writes in anyway
RUSTFLAGS="%{build_rustflags}" cargo test -j%{_smp_build_ncpus} --profile rpm --locked --offline -- \
    --skip shelf::tests::failed_save_rolls_back

%files
%license LICENSE LICENSE.dependencies cargo-vendor.txt
%doc README.md
%{_bindir}/deck
%{_datadir}/icons/hicolor/scalable/apps/deck.svg

%changelog
* Tue Oct 27 2026 Jari Lehtinen <jari@feature.fi> - 0.1.1-1
- Pausing no longer hangs the player on pipewire-alsa 1.6.10 (Deck's own ALSA output)
- One Deck at a time: a lock on $XDG_RUNTIME_DIR/deck/deck.lock from the start

* Fri Oct 23 2026 Jari Lehtinen <jari@feature.fi> - 0.1.0-1
- First package, for Nightdrive's Deck app
