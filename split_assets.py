import zipfile, os, time, shutil

t0 = time.time()
src_zip = 'D:/dwload/cs11port/valve.zip'
pak_out = 'D:/dwload/cs11port/pak0.pak'
assets_out = 'D:/dwload/cs11port/assets.zip'

# 1. Extract pak0.pak as a loose raw file for direct HTTP serving
print('Extracting pak0.pak...')
with zipfile.ZipFile(src_zip) as zf:
    with zf.open('valve/pak0.pak') as src, open(pak_out, 'wb') as dst:
        shutil.copyfileobj(src, dst)
pak_size = os.path.getsize(pak_out)
print(f'pak0.pak extracted: {pak_size // 1024 // 1024} MB')

# 2. Repack assets.zip without pak0.pak
print('Repacking assets.zip without pak0.pak...')
with zipfile.ZipFile(src_zip) as zf_in:
    with zipfile.ZipFile(assets_out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf_out:
        count = 0
        for item in zf_in.infolist():
            if item.is_dir() or 'pak0.pak' in item.filename:
                continue
            data = zf_in.read(item.filename)
            zf_out.writestr(item, data)
            count += 1
            if count % 200 == 0:
                print(f'  {count} files...')

elapsed = time.time() - t0
assets_size = os.path.getsize(assets_out)
print(f'Done in {elapsed:.2f}s')
print(f'assets.zip: {assets_size // 1024 // 1024} MB, {count} files')
