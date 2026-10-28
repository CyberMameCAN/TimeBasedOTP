import os
from pathlib import Path

import pyotp
import qrcode

# 1. 秘密鍵を読み出す処理
save_dir = Path(__file__).resolve().parent / "maruhi"
secret_path = save_dir / "secret.txt"
secret = secret_path.read_text(encoding="utf-8").strip()

# 2. TOTPオブジェクトを作成
totp = pyotp.TOTP(secret)

# 3. Authenticatorなどのアプリに登録するためのURI（プロビジョニングURL）を取得
uri = totp.provisioning_uri(name="user@example.com", issuer_name="MyPythonApp")

# 4. QRコードを生成して画像ファイルとして保存
img = qrcode.make(uri)
# 保存前に権限を制限し、既存ファイルの場合も600に設定する。
fd = os.open("otp_qr.png", os.O_WRONLY | os.O_CREAT, 0o600)
with os.fdopen(fd, "wb") as file:
    os.fchmod(file.fileno(), 0o600)
    file.truncate(0)
    img.save(file, format="PNG")
print("QRコードを 'otp_qr.png' として保存しました。スマホの認証アプリで読み込んでください。")

# 5. 現在のワンタイムパスワードを表示
current_otp = totp.now()
print(f"現在のワンタイムパスワード: {current_otp}")

# 6. ユーザーが入力したコードを検証する例
input_code = input("認証コードを入力してください: ")
if totp.verify(input_code):
    print("認証成功！")
else:
    print("認証失敗...")
