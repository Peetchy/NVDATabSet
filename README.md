# NVDA TabSet

NVDA TabSet is an NVDA add-on for checking Thailand SET stock prices and stock factsheet information from `set.or.th`.

## Compatibility

- Minimum NVDA version: 2025.3.0
- Last tested NVDA version: 2026.1.1
- Update channel: stable for tagged releases, dev for branch artifacts

## Usage

- Press `NVDA+Alt+T` to enable TabSet mode.
- Press a configured favorite key to fetch stock data.
- Press `=` while TabSet mode is enabled to open NVDA TabSet settings.
- Press `Escape` while TabSet mode is enabled to close TabSet mode.

## Build Locally

```powershell
python scripts\build_addon.py
```

The package is written to `dist\NVDATabSet-<version>.nvda-addon`.

## Release From GitHub

### First Publish

```powershell
gh auth login -h github.com
gh repo create NVDATabSet --public --source . --remote origin --push
```

After the repository exists, update `url` in `manifest.ini` to the repository URL if you want local builds to include it. GitHub Actions release builds automatically package the correct repository URL.

### Create a Release

Create and push a version tag:

```powershell
git tag v2026.5.28
git push origin main --tags
```

The GitHub workflow builds `*.nvda-addon` and attaches it to the GitHub release.

## Add-on Updates

NVDA automatic add-on updates are provided through the NVDA Add-on Store. The manifest uses `updateChannel = stable`, and the release workflow packages tagged releases as stable builds.

To make users receive update notifications inside NVDA, submit each release to the NVDA Add-on Store through `nvaccess/addon-datastore`. Users can still manually update by downloading the `*.nvda-addon` file from GitHub Releases.
