# COPR's "make_srpm" build method runs this for every build (copr-cli add-package-scm --method make_srpm):
#   make -f .copr/Makefile srpm outdir=<dir> spec=<package>/<package>.spec
# It downloads the spec's sources (its Source lines are URLs) and makes the SRPM in outdir. A package whose source
# can't be just downloaded (Ghostty's fetched Zig dependencies) has a <package>/sources.sh that makes it after that.
# A package with a <package>/sources.sha256 has its downloads checked against it first (tools/verify-sources.sh).
# COPR runs this from the package's folder, so the tools are found from this file's own path.
tools := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))../tools)
spec ?= $(error spec=<package>/<package>.spec is required)
outdir ?= $(CURDIR)/out

srpm:
	dnf -y install rpmdevtools rpm-build
	spectool -g -C "$(outdir)" "$(spec)"
	"$(tools)/verify-sources.sh" "$(spec)" "$(outdir)"
	if [ -x "$(dir $(spec))sources.sh" ]; then "$(dir $(spec))sources.sh" "$(spec)" "$(outdir)"; fi
	rpmbuild -bs --define "_sourcedir $(outdir)" --define "_srcrpmdir $(outdir)" "$(spec)"
