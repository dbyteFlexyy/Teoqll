import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Heroku environment variable से token लें
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8333062611:AAH2fdhTTUNLQnBod0r3qtCjYsTjDG7fXWY')

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def format_caption_advanced(original_caption):
    """
    Advanced caption formatting with better parsing and BOLD text
    """
    try:
        lines = original_caption.split('\n')
        
        info_dict = {}
        for line in lines:
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                
                if "episode" in key:
                    info_dict['episode'] = value
                elif "quality" in key:
                    info_dict['quality'] = value
                elif "audio" in key:
                    info_dict['audio'] = value
                elif "season" in key:
                    info_dict['season'] = value
        
        # Default values यदि information नहीं मिली
        episode = info_dict.get('episode', '01')
        quality = info_dict.get('quality', '480p')
        audio = info_dict.get('audio', 'Hindi | #Official')
        
        # Final formatted caption with BOLD text using HTML
        formatted_caption = f"""<b>›› 𝖤𝗉𝗂𝗌𝗈𝖽𝖾 : {episode}</b>
<b>›› 𝖰𝗎𝖺𝗅𝗂𝗍𝗒 : {quality}</b> 
<b>›› 𝖠𝗎𝖽𝗂𝗈 : 𝖧𝗂𝗇𝖽𝗂 | #𝖮𝖿𝖿𝗂𝖼𝗂𝖺𝗅</b>
━━━━━━━━━━━━━━━━━━━━━━━
➥ᴊᴏɪɴ : [ @Crunchyroll_In_Hindi_Offcial ]
➥ʙʏ : [ @Anime_Hindi_Dub_Official ]"""
        
        return formatted_caption
        
    except Exception as e:
        logger.error(f"Advanced caption formatting error: {e}")
        return None

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video messages with advanced formatting and BOLD text"""
    try:
        if update.message.video and update.message.caption:
            original_caption = update.message.caption
            formatted_caption = format_caption_advanced(original_caption)
            
            if formatted_caption:
                await update.message.copy(
                    chat_id=update.message.chat_id,
                    caption=formatted_caption,
                    parse_mode='HTML'
                )
                await update.message.delete()
            else:
                await update.message.reply_text("❌ Error formatting caption!")
                
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ Something went wrong!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Anime Bot Ready!\n\n"
        "Send me videos with captions and I'll auto-format them with BOLD text.\n\n"
        "Use /help for more info"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Supported Format:\n\n"
        "Title • ✅\n"
        "Episode : 01\n" 
        "Season : 01\n"
        "Quality : 480p\n"
        "Audio : Hindi | #Official\n\n"
        "I'll convert it to the new format with BOLD text automatically!"
    )

def main():
    # Check if BOT_TOKEN is set
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables!")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(MessageHandler(filters.VIDEO & filters.CAPTION, handle_video))
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex("start"), start))
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex("help"), help_cmd))
    
    logger.info("🚀 Bot started on Heroku...")
    application.run_polling()

if __name__ == "__main__":
    main()
