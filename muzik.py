import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7706134135:AAHRzD8xnl4IGxoxpbrobRkBsCpdQAy46Qo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Merhaba! Şarkı indirmek için `/indir şarkı adı` komutunu kullanabilirsin.", parse_mode="Markdown")

async def indir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Lütfen şarkı adını yazınız.\n\nÖrnek:\n`/indir gördü dalgayı dedi malamine`", parse_mode="Markdown")
        return

    song_name = " ".join(context.args)
    mesaj = await update.message.reply_text(f"🔍 Şarkı aranıyor: `{song_name}`\n⏳ Lütfen bekleyin...", parse_mode="Markdown")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            entry = info['entries'][0]
            filename = ydl.prepare_filename(entry)
            mp3_file = filename.rsplit('.', 1)[0] + '.mp3'

        await mesaj.edit_text(f"🎶 Şarkı bulundu: *{entry['title']}*\n📤 Gönderiliyor...", parse_mode="Markdown")

        with open(mp3_file, 'rb') as f:
            await update.message.reply_audio(f, title=entry['title'])

        os.remove(mp3_file)

    except Exception as e:
        await mesaj.edit_text(f"❌ Hata oluştu: `{str(e)}`", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("indir", indir))

    print("✅ Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
