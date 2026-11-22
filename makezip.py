import os
import struct
import zipfile

ROOT = "CS11"
OUTPUT = "valve.zip"
PAK_SOURCE = os.path.join(ROOT, "valve", "pak0.pak")

if not os.path.isfile(PAK_SOURCE):
    raise FileNotFoundError(f"Missing file: {PAK_SOURCE}")

# Reject maps-only PAK variants that omit precached game assets.
with open(PAK_SOURCE, "rb") as pak:
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

# Package the complete valve/ and cstrike/ trees, including the full pak0.pak.
with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for folder in ("valve", "cstrike"):
        base = os.path.join(ROOT, folder)

        if not os.path.isdir(base):
            raise FileNotFoundError(f"Missing folder: {base}")

        for current, _, files in os.walk(base):
            for filename in files:
                path = os.path.join(current, filename)
                archive_name = os.path.relpath(path, ROOT)
                archive.write(path, archive_name.replace("\\", "/"))

print(f"Done: {os.path.abspath(OUTPUT)}")