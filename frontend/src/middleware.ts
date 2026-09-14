import { NextRequest, NextResponse } from 'next/server';

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || '';

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (pathname === '/api/v1/webhooks/telegram' && request.method === 'POST') {
    try {
      const update = await request.json();
      const message = update.message || update.edited_message;

      if (message && message.chat && message.text) {
        const chatId = message.chat.id;
        const text = message.text.trim();

        let replyText = `💡 *Tip:* Please send a public video link from Instagram Reels, YouTube Shorts, or TikTok.`;

        if (text.startsWith('/start')) {
          replyText = `⚡ *Welcome to Universal Pro AI Bot!* 🤖\n\nSend or forward any *Instagram Reel*, *YouTube Short*, or *TikTok Video* link to extract recipes, ingredients, instructions, and 10-minute delivery links instantly!`;
        } else if (text.startsWith('/help')) {
          replyText = `ℹ️ *How to use Universal Pro AI Bot:*\n\n1. Copy any video link from Instagram, YouTube, or TikTok.\n2. Paste it directly into this chat.\n3. Receive structured steps and shoppable buy links automatically!`;
        } else {
          const videoMatch = text.match(/(https?:\/\/(?:www\.)?(?:instagram\.com\/(?:reel|reels|p)\/[a-zA-Z0-9_-]+\/?|youtube\.com\/(?:watch\?v=[a-zA-Z0-9_-]+|shorts\/[a-zA-Z0-9_-]+\/?)|youtu\.be\/[a-zA-Z0-9_-]+\/?|tiktok\.com\/@[a-zA-Z0-9._-]+\/video\/\d+\/?))/i);
          if (videoMatch) {
            const videoUrl = videoMatch[1];
            replyText = `⏳ *Analyzing video:* \`${videoUrl}\`\n\nProcessing audio, visual steps, and 10-minute delivery links with Universal Pro AI...`;
          }
        }

        // Send message to Telegram chat
        const res = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            chat_id: chatId,
            text: replyText,
            parse_mode: 'Markdown',
            disable_web_page_preview: false,
          }),
        });

        // Fallback without parse_mode if Markdown parsing encounters formatting entities
        if (!res.ok) {
          await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              chat_id: chatId,
              text: replyText,
              disable_web_page_preview: false,
            }),
          });
        }
      }
    } catch (err) {
      console.error('[Edge Middleware Telegram Error]', err);
    }

    return NextResponse.json({ ok: true, source: 'edge_middleware' });
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/api/v1/webhooks/telegram'],
};
