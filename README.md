# NVDA TabSet

NVDA TabSet is an NVDA add-on for checking Thailand Stock Exchange (SET) stock prices and stock factsheet information from `set.or.th` without leaving the keyboard.

The add-on adds a temporary TabSet mode for fast stock lookup. When the mode is enabled, each configured favorite key fetches the stock symbol assigned to that key and reports the result with NVDA speech. Results can also be copied to the clipboard.

## Features

- Keyboard-driven stock lookup mode toggled with `NVDA+Alt+T`.
- Favorite stock shortcuts for letters, numbers, and common punctuation keys.
- Price view with company name, last price, change, change percentage, prior, open, high, low, and last update time.
- Factsheet view with company name, P/E, P/BV, market cap, and dividend yield when available from SET.
- English or Thai label selection from the settings panel.
- Optional automatic copy of stock information to the clipboard.
- Sound feedback for start, loading, completion, failure, and close events.
- NVDA Settings panel for editing favorite symbols and display options.

## Compatibility

- Minimum NVDA version: 2025.3.0
- Last tested NVDA version: 2026.1.1
- Update channel: stable for tagged releases, dev for branch artifacts

## Installation

Download the latest `NVDATabSet-<version>.nvda-addon` file from GitHub Releases and open it while NVDA is running. Restart NVDA when prompted.

## Usage

- Press `NVDA+Alt+T` to enable TabSet mode.
- Press a configured favorite key to fetch stock data.
- Press `=` while TabSet mode is enabled to open NVDA TabSet settings.
- Press `Escape` while TabSet mode is enabled to close TabSet mode.

## Settings

Open the NVDA TabSet settings panel from NVDA Settings, or press `=` while TabSet mode is enabled.

Available settings:

- Edit favorite stock symbols assigned to shortcut keys.
- Choose whether shortcuts report stock price data or stock factsheet data.
- Choose English or Thai labels for reported fields.
- Enable or disable copying result text to the clipboard.

## Data Source

NVDA TabSet fetches public stock quote and factsheet pages from `set.or.th`.

The SET website can change its page structure or omit some fields for a symbol. When a field is unavailable, the add-on leaves that field blank rather than blocking the lookup.

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
git tag v2026.5.1
git push origin main --tags
```

The GitHub workflow builds `*.nvda-addon` and attaches it to the GitHub release.

## Add-on Updates

NVDA automatic add-on updates are provided through the NVDA Add-on Store. The manifest uses `updateChannel = stable`, and the release workflow packages tagged releases as stable builds.

To make users receive update notifications inside NVDA, submit each release to the NVDA Add-on Store through `nvaccess/addon-datastore`. Users can still manually update by downloading the `*.nvda-addon` file from GitHub Releases.
