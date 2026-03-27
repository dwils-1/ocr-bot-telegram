import os
import telebot
import pytesseract
from PIL import Image
from flask import Flask, request

# --- KONFIGURASI ---
TOKEN = 'ISI_TOKEN_BOT_ANDA' 
GROUP_ID = '-1003594385102'  # ID Grup yang sudah disesuaikan
PRIVATE_ID = '836686436'     # ID Akun pribadi Anda


app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

# --- TAMPILAN INTERFACE (HTML & CSS) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OCR Kerja - Pova & Vivo</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #eef2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 90%; max-width: 400px; text-align: center; }
        h2 { color: #0088cc; margin-bottom: 5px; }
        p { color: #666; font-size: 14px; margin-bottom: 25px; }
        .upload-box { border: 2px dashed #0088cc; padding: 30px; border-radius: 15px; cursor: pointer; display: block; margin-bottom: 20px; transition: 0.3s; }
        .upload-box:hover { background: #f0f9ff; }
        input[type="file"] { display: none; }
        button { background: #0088cc; color: white; border: none; padding: 15px; border-radius: 10px; width: 100%; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #006699; }
        #status { margin-top: 15px; font-size: 13px; color: #28a745; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>OCR Bot Kerja</h2>
        <p>Kirim foto dari Pova 7 ke Telegram Vivo V9</p>
        
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label class="upload-box">
                <span id="label-text">📸 Ketuk untuk Pilih Foto</span>
                <input type="file" name="file" accept="image/*" required onchange="showName(this)">
            </label>
            <button type="submit">PROSES & KIRIM</button>
        </form>
        <div id="status">Sistem Siap</div>
    </div>

    <script>
        function showName(input) {
            if (input.files.length > 0) {
                document.getElementById('label-text').innerText = "Terpilih: " + input.files[0].name;
            }
        }
    </script>
</body>
</html>
'''

# --- LOGIKA SERVER ---

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Tidak ada file"
    
    file = request.files['file']
    if file.filename == '':
        return "Nama file kosong"

    try:
        # 1. Ekstrak Teks (OCR)
        img = Image.open(file)
        text = pytesseract.image_to_string(img)

        # 2. Kirim ke Grup (Foto + Teks)
        file.seek(0)
        bot.send_photo(GROUP_ID, file, caption="✅ Dokumen Masuk")
        
        if text.strip():
            bot.send_message(GROUP_ID, f"📝 **HASIL EKSTRAK:**\n\n`{text}`", parse_mode='Markdown')
            # 3. Kirim ke Chat Pribadi (Backup)
            bot.send_message(PRIVATE_ID, f"📂 Salinan Teks Kerja:\n\n{text}")
            return "✅ BERHASIL! Teks sudah di grup & chat pribadi."
        else:
            bot.send_message(GROUP_ID, "⚠️ Gambar diterima, tapi teks tidak terbaca.")
            return "✅ Foto terkirim, tapi teks gagal diekstrak."

    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    # Menyesuaikan port untuk Cloud Hosting atau Lokal
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
