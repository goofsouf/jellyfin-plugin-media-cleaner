#!/usr/bin/env python3
"""Package a locally built Media Cleaner plugin for one Jellyfin server profile."""

import argparse
import datetime as dt
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROFILES = json.loads((ROOT / "eng/jellyfin-profiles.json").read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="12.1", help="Jellyfin server profile")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()

    server = next((p for p in PROFILES["serverProfiles"] if p["profile"] == args.profile), None)
    if server is None:
        parser.error(f"Unknown Jellyfin server profile: {args.profile}")
    build = next(p for p in PROFILES["buildProfiles"] if p["profile"] == server["buildProfile"])
    framework = build["targetFramework"]
    binary_dir = ROOT / "MediaCleaner/bin/Release" / framework
    files = [binary_dir / "MediaCleaner.dll", binary_dir / "MediaCleaner.Core.dll", ROOT / "LICENSE"]
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        parser.error("Build the plugin first; missing: " + ", ".join(missing))

    version = f"{PROFILES['baseVersion']}.{build['versionPatchOffset']}"
    metadata = {
        "category": "General",
        "changelog": "Fix task lookup so cleanup and schedule controls enable after the Jellyfin response loads.",
        "description": "Rule-based media cleanup with manual and scheduled runs.",
        "guid": "607fee77-97eb-41fe-bf22-26844d99ffb0",
        "name": "Media Cleaner",
        "overview": "Rule-based media cleanup",
        "owner": "Media Cleaner local fork",
        "targetAbi": build["targetAbi"],
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "version": version,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    output = args.output / f"MediaCleaner-{args.profile}-local-{version}.zip"
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.name)
        archive.writestr("meta.json", json.dumps(metadata, indent=4) + "\n")
    print(output)


if __name__ == "__main__":
    main()
