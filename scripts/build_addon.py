"""Build NVDA TabSet as a .nvda-addon package."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIRS = ("globalPlugins", "locale", "doc")
PACKAGE_FILES = ("manifest.ini",)
EXCLUDED_DIRS = {".git", ".github", "dist", "scripts", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def parse_manifest(path: Path) -> dict[str, str]:
	values: dict[str, str] = {}
	lines = path.read_text(encoding="utf-8-sig").splitlines()
	index = 0
	while index < len(lines):
		line = lines[index].strip()
		index += 1
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = (part.strip() for part in line.split("=", 1))
		if value.startswith('"""') and not value.endswith('"""'):
			parts = [value[3:]]
			while index < len(lines):
				next_line = lines[index]
				index += 1
				if next_line.endswith('"""'):
					parts.append(next_line[:-3])
					break
				parts.append(next_line)
			values[key] = "\n".join(parts)
		elif value.startswith('"""') and value.endswith('"""'):
			values[key] = value[3:-3]
		elif value.startswith('"') and value.endswith('"'):
			values[key] = value[1:-1]
		else:
			values[key] = value
	return values


def update_manifest(source: Path, destination: Path, version: str | None, channel: str | None, url: str | None) -> None:
	lines = source.read_text(encoding="utf-8-sig").splitlines()
	replacements = {
		"version": version,
		"updateChannel": channel,
		"url": url,
	}
	with destination.open("w", encoding="utf-8", newline="\n") as manifest:
		for line in lines:
			stripped = line.strip()
			key = stripped.split("=", 1)[0].strip() if "=" in stripped else ""
			if key in replacements and replacements[key] is not None:
				manifest.write(f"{key} = {replacements[key]}\n")
			else:
				manifest.write(f"{line}\n")


def should_include(path: Path) -> bool:
	relative = path.relative_to(ROOT)
	if any(part in EXCLUDED_DIRS for part in relative.parts):
		return False
	if path.suffix.lower() in EXCLUDED_SUFFIXES:
		return False
	return True


def copy_package_file(source: Path, destination: Path) -> None:
	destination.parent.mkdir(parents=True, exist_ok=True)
	shutil.copy2(source, destination)


def stage_package(stage: Path, version: str | None, channel: str | None, url: str | None) -> None:
	for file_name in PACKAGE_FILES:
		source = ROOT / file_name
		if file_name == "manifest.ini":
			update_manifest(source, stage / file_name, version, channel, url)
		else:
			copy_package_file(source, stage / file_name)
	for dir_name in PACKAGE_DIRS:
		source_dir = ROOT / dir_name
		if not source_dir.exists():
			continue
		for source in source_dir.rglob("*"):
			if source.is_file() and should_include(source):
				copy_package_file(source, stage / source.relative_to(ROOT))


def build(output_dir: Path, version: str | None, channel: str | None, url: str | None) -> Path:
	manifest = parse_manifest(ROOT / "manifest.ini")
	addon_name = manifest["name"]
	addon_version = version or manifest["version"]
	output_dir.mkdir(parents=True, exist_ok=True)
	output_file = output_dir / f"{addon_name}-{addon_version}.nvda-addon"

	with tempfile.TemporaryDirectory(prefix="nvda-tabset-build-") as temp_dir:
		stage = Path(temp_dir)
		stage_package(stage, version, channel, url)
		with zipfile.ZipFile(output_file, "w", compression=zipfile.ZIP_DEFLATED) as archive:
			for source in sorted(stage.rglob("*")):
				if source.is_file():
					archive.write(source, source.relative_to(stage).as_posix())
	return output_file


def main() -> int:
	parser = argparse.ArgumentParser(description="Build the NVDA TabSet add-on package.")
	parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
	parser.add_argument("--version")
	parser.add_argument("--channel")
	parser.add_argument("--url")
	args = parser.parse_args()

	output_file = build(args.output_dir, args.version, args.channel, args.url)
	print(output_file)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

