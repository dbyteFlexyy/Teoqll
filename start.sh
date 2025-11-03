#!/bin/bash

echo "🚀 Starting Anime Caption Formatter Bot..."

# Check if BOT_TOKEN is set
if [ -z "$BOT_TOKEN" ]; then
    echo "❌ ERROR: BOT_TOKEN environment variable is not set!"
    exit 1
fi

echo "✅ Environment variables checked successfully"
echo "🤖 Bot is starting..."

# Start the bot
python bot.py
