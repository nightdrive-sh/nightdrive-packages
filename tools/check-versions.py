#!/usr/bin/python3 -I
"""Compares each spec's Version with its upstream's newest release and prints the packages that are behind, as a
Markdown list (nothing when all are current). Exit 0 either way; 2 when an upstream couldn't be read.
  tools/check-versions.py
Upstream: the latest GitHub release (or tag) of the spec's github.com URL; Lua from lua.org's download list, within
the spec's major.minor (lua5.5 stays 5.5.x); a spec whose Source is a Forgejo archive (Quickshell's git.outfoxxed.me),
that forge's highest version tag. A library built into a package (Provides: bundled(NAME) = %{MACRO}, its
Source a github.com archive of that macro's version: wayvnc's neatvnc and aml, Hyprland's glaze) is checked too, within
its major version: the package pins that major (Hyprland needs glaze 7), and a fix is released in it.
GITHUB_TOKEN, if set, avoids the API's low anonymous rate limit."""
import glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(url, api=False):
    req = urllib.request.Request(url, headers={"User-Agent": "nightdrive-packages"})
    if api and os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


def key(v):
    return [int(x) for x in re.findall(r"\d+", v)]


def github_latest(repo, major=None):
    """The newest release; with major, the highest version tag of that major version."""
    if major is not None:
        return highest_tag(repo, major + ".")
    try:
        return json.loads(get(f"https://api.github.com/repos/{repo}/releases/latest", api=True))["tag_name"].lstrip("v")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    return highest_tag(repo)     # no releases


def highest_tag(repo, prefix=""):
    tags = [t["name"].lstrip("v") for t in json.loads(get(f"https://api.github.com/repos/{repo}/tags?per_page=100", api=True))]
    tags = [t for t in tags if re.fullmatch(r"\d+(\.\d+)*", t) and t.startswith(prefix)]
    return max(tags, key=key) if tags else None


def bundled(spec):
    """(name, version, github repo) of each library the spec builds in from a github.com archive."""
    found = []
    for name, macro in re.findall(r"^Provides:\s*bundled\(([^)]+)\)\s*=\s*%\{(\w+)\}", spec, re.M):
        version = re.search(r"^%%global\s+%s\s+(\S+)" % macro, spec, re.M)
        src = re.search(r"^Source\d*:\s*https://github\.com/([^/]+/[^/]+)/archive/\S*%%\{%s\}" % macro, spec, re.M)
        if version and src:
            found.append((name, version.group(1), src.group(1)))
    return found


def forgejo_latest(host, repo):
    """The highest version tag of a Forgejo (or Gitea) repo: its API answers as GitHub's tags list does."""
    tags = [t["name"].lstrip("v") for t in json.loads(get(f"https://{host}/api/v1/repos/{repo}/tags?limit=50"))]
    tags = [t for t in tags if re.fullmatch(r"\d+(\.\d+)*", t)]
    return max(tags, key=key) if tags else None


def lua_latest(major_minor):
    found = re.findall(r"lua-(%s\.\d+)\.tar\.gz" % re.escape(major_minor), get("https://www.lua.org/ftp/"))
    return max(found, key=key) if found else None


def field(spec, name):
    m = re.search(r"^%s:\s*(\S+)" % name, spec, re.M)
    return m.group(1) if m else ""


behind, errors = [], []
for path in sorted(glob.glob(os.path.join(ROOT, "*", "*.spec"))):
    spec = open(path).read()
    name, version, url = field(spec, "Name"), field(spec, "Version"), field(spec, "URL")
    try:
        gh = re.match(r"https://github\.com/([^/]+/[^/]+?)/?$", url)
        forge = re.search(r"^Source\d*:\s*https://(git\.outfoxxed\.me)/([^/]+/[^/]+)/archive/", spec, re.M)
        if gh:
            latest = github_latest(gh.group(1))
        elif forge:
            latest = forgejo_latest(forge.group(1), forge.group(2).replace("%{name}", name))
        elif "lua.org" in url:
            latest = lua_latest(".".join(version.split(".")[:2]))
        else:
            errors.append(f"{name}: no way to check {url}")
            continue
    except Exception as e:      # one unreachable upstream shouldn't hide the others
        errors.append(f"{name}: {e}")
        continue
    if latest and key(latest) > key(version):
        behind.append(f"- **{name}** {version} → {latest} ({url})")
    for lib, lib_version, repo in bundled(spec):
        try:
            latest = github_latest(repo, major=lib_version.split(".")[0])
        except Exception as e:
            errors.append(f"{name} ({lib}): {e}")
            continue
        if latest and key(latest) > key(lib_version):
            behind.append(f"- **{lib}** (built into {name}) {lib_version} → {latest} (https://github.com/{repo})")

if behind:      # nothing at all when all are current: the workflow closes the issue on an empty report
    print("\n".join(behind))
for e in errors:
    print("check-versions:", e, file=sys.stderr)
sys.exit(2 if errors else 0)
