import os
from pathlib import Path

import pyotp

# 1. 秘密鍵（シークレット）をBase32形式で自動生成
secret = pyotp.random_base32()
print(f'(本来は表示しない)秘密鍵: {secret}')

save_dir = Path(__file__).resolve().parent / "maruhi"
save_dir.mkdir(parents=True, exist_ok=True)
secret_path = save_dir / "secret.txt"

# 新規作成時から所有者だけが読み書きできる権限にする。
fd = os.open(secret_path, os.O_WRONLY | os.O_CREAT, 0o600)
with os.fdopen(fd, "w", encoding="utf-8") as file:
    os.fchmod(file.fileno(), 0o600)
    file.truncate(0)
    file.write(secret)

print(f'保存先: {secret_path}')
