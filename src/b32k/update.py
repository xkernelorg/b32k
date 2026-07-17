"""Read-only discovery of registered component updates."""

from __future__ import annotations

import datetime
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


class B32KUpdateInspectionError(RuntimeError):
    pass


@dataclass(frozen=True)
class ComponentSource:
    component: str
    repository_url: str
    local_path: Path
    branch: str


@dataclass(frozen=True)
class ComponentUpdate:
    component: str
    repository_url: str
    local_path: str
    branch: str
    local_commit: str
    upstream_commit: str
    ahead_count: int
    behind_count: int
    working_tree_clean: bool
    update_available: bool
    checked_at: str
    fetch_performed: bool
    checkout_performed: bool = False
    merge_performed: bool = False
    installation_performed: bool = False
    authority_conferred: bool = False

    def as_dict(self):
        return asdict(self)


def registered_sources(home=None):
    root = Path.home() if home is None else Path(home)
    return {
        "kernel": ComponentSource(
            component="kernel",
            repository_url="git@github.com:xkernelorg/xkernel.git",
            local_path=(
                root
                / "dev/cori/research/computing/kernel/xkernel"
            ),
            branch="main",
        ),
    }


def _git(path, arguments, timeout=30):
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise B32KUpdateInspectionError(
            "git metadata inspection failed"
        ) from exc

    if result.returncode != 0:
        detail = result.stdout.strip()
        raise B32KUpdateInspectionError(
            detail or "git metadata inspection failed"
        )
    return result.stdout.strip()


def inspect_component_update(
    component,
    *,
    fetch=True,
    home=None,
):
    sources = registered_sources(home)
    if component not in sources:
        raise B32KUpdateInspectionError(
            "component is not registered for update discovery"
        )

    source = sources[component]
    root = source.local_path
    if not root.is_dir() or not (root / ".git").exists():
        raise B32KUpdateInspectionError(
            "registered component repository is unavailable"
        )

    origin = _git(root, ["remote", "get-url", "origin"])
    accepted_origins = {
        source.repository_url,
        "https://github.com/xkernelorg/xkernel.git",
    }
    if origin not in accepted_origins:
        raise B32KUpdateInspectionError(
            "component origin does not match its registration"
        )

    branch = _git(root, ["branch", "--show-current"])
    if branch != source.branch:
        raise B32KUpdateInspectionError(
            "component is not on its registered branch"
        )

    fetch_performed = False
    if fetch:
        _git(
            root,
            ["fetch", "--quiet", "--prune", "origin", source.branch],
            timeout=120,
        )
        fetch_performed = True

    local_commit = _git(root, ["rev-parse", "HEAD"])
    upstream_ref = f"origin/{source.branch}"
    upstream_commit = _git(root, ["rev-parse", upstream_ref])
    counts = _git(
        root,
        [
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...{upstream_ref}",
        ],
    ).split()

    if len(counts) != 2:
        raise B32KUpdateInspectionError(
            "git divergence result is malformed"
        )

    ahead_count, behind_count = map(int, counts)
    porcelain = _git(
        root,
        ["status", "--porcelain", "--untracked-files=normal"],
    )

    return ComponentUpdate(
        component=source.component,
        repository_url=source.repository_url,
        local_path=str(root),
        branch=source.branch,
        local_commit=local_commit,
        upstream_commit=upstream_commit,
        ahead_count=ahead_count,
        behind_count=behind_count,
        working_tree_clean=not bool(porcelain),
        update_available=behind_count > 0,
        checked_at=datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        fetch_performed=fetch_performed,
    )
