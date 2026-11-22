import argparse
import struct
import zipfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def find_default_game_dir():
    for candidate in (SCRIPT_DIR / "CS11", SCRIPT_DIR):
        if (candidate / "valve").is_dir() and (candidate / "cstrike").is_dir():
            return candidate
    return SCRIPT_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Package a Counter-Strike installation's valve/ and cstrike/ folders into valve.zip."
    )
    parser.add_argument(
        "game_dir",
        nargs="?",
        type=Path,
        default=find_default_game_dir(),
        help="folder containing valve/ and cstrike/ (defaults to this folder or its CS11/ subfolder)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=SCRIPT_DIR / "valve.zip",
        help="output ZIP path (defaults to valve.zip beside this script)",
    )
    args = parser.parse_args()
    game_dir = args.game_dir.resolve()
    output = args.output.resolve()

    pak_source = game_dir / "valve" / "pak0.pak"
    if not pak_source.is_file():
        raise FileNotFoundError(f"Missing file: {pak_source}")

    # Reject maps-only PAK variants that omit precached game assets.
    with pak_source.open("rb") as pak:
        header = pak.read(12)
        if len(header) != 12:
            raise ValueError("Invalid PAK header")
        signature, directory_offset, directory_size = struct.unpack("<4sII", header)
        if signature != b"PACK" or directory_size % 64:
            raise ValueError("pak0.pak is not a valid PACK archive")
        pak.seek(directory_offset)
        directory = pak.read(directory_size)
        if len(directory) != directory_size:
            raise ValueError("Truncated PAK directory")
        names = [directory[i:i + 56].split(b"\0", 1)[0] for i in range(0, directory_size, 64)]
        if b"sound/items/gunpickup2.wav" not in names:
            raise ValueError("pak0.pak is missing precached sound: sound/items/gunpickup2.wav")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for folder in ("valve", "cstrike"):
            base = game_dir / folder
            if not base.is_dir():
                raise FileNotFoundError(f"Missing folder: {base}")
            for path in base.rglob("*"):
                if path.is_file():
                    archive.write(path, path.relative_to(game_dir).as_posix())

    print(f"Done: {output}")


if __name__ == "__main__":
    main()
