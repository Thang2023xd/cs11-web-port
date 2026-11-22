import argparse
import shutil
import time
import zipfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(
        description="Split valve.zip into assets.zip and a standalone pak0.pak."
    )
    parser.add_argument(
        "source_zip",
        nargs="?",
        type=Path,
        default=SCRIPT_DIR / "valve.zip",
        help="input archive (defaults to valve.zip beside this script)",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        type=Path,
        default=None,
        help="output folder (defaults to the input archive's folder)",
    )
    args = parser.parse_args()
    source_zip = args.source_zip.resolve()
    output_dir = (args.output_dir or source_zip.parent).resolve()
    pak_out = output_dir / "pak0.pak"
    assets_out = output_dir / "assets.zip"

    if not source_zip.is_file():
        raise FileNotFoundError(f"Missing archive: {source_zip}")

    started = time.time()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Extracting pak0.pak...")
    with zipfile.ZipFile(source_zip) as archive:
        pak_member = next(
            (name for name in archive.namelist() if name.lower() == "valve/pak0.pak"),
            None,
        )
        if pak_member is None:
            raise FileNotFoundError("valve.zip does not contain valve/pak0.pak")
        with archive.open(pak_member) as source, pak_out.open("wb") as destination:
            shutil.copyfileobj(source, destination)
    print(f"pak0.pak extracted: {pak_out.stat().st_size // 1024 // 1024} MB")

    print("Repacking assets.zip without pak0.pak...")
    count = 0
    with zipfile.ZipFile(source_zip) as source, zipfile.ZipFile(
        assets_out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    ) as destination:
        for item in source.infolist():
            if item.is_dir() or item.filename.lower().endswith("/pak0.pak"):
                continue
            destination.writestr(item, source.read(item.filename))
            count += 1
            if count % 200 == 0:
                print(f"  {count} files...")

    elapsed = time.time() - started
    print(f"Done in {elapsed:.2f}s")
    print(f"assets.zip: {assets_out.stat().st_size // 1024 // 1024} MB, {count} files")
    print(f"Created: {assets_out}")


if __name__ == "__main__":
    main()
