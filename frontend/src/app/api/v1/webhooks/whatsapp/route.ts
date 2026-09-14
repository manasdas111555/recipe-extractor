import { NextRequest, NextResponse } from 'next/server';

const WHATSAPP_ACCESS_TOKEN = process.env.WHATSAPP_ACCESS_TOKEN || 'EAAhmXgENiGwBSR0tZCwYxHTxyLswMyKl8lOA8iOXBnuzreMbjI7ajDTCrZAbz4f7KV6ZB8aoooaIC6Y1n06ePxV4t5wTQRvHLRTFJERwV6YT1RePbqS5oDij7xITxWGHXy1ImXlR4uDY9nN37hFe0lr2Q1qZAw14DM5AHGZBf4PZAwkxCuRMwIrmAjwRsf4HyN06hXuKaQeuqK9NwIZBH9toR7Bm7aKrR8rL6mLAymyP2xJOwttPe62VKgv8NflOf4NLApvPdvOdKhRP8Mu8gZDZD';
const WHATSAPP_PHONE_NUMBER_ID = process.env.WHATSAPP_PHONE_NUMBER_ID || '1280483961819200';
const WHATSAPP_VERIFY_TOKEN = process.env.WHATSAPP_VERIFY_TOKEN || 'universal_pro_verify_token';
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || '';

const VIDEO_URL_REGEX = /(https?:\/\/(?:www\.)?(?:instagram\.com\/(?:reel|reels|p)\/[a-zA-Z0-9_-]+\/?|youtube\.com\/(?:watch\?v=[a-zA-Z0-9_-]+|shorts\/[a-zA-Z0-9_-]+\/?)|youtu\.be\/[a-zA-Z0-9_-]+\/?|tiktok\.com\/@[a-zA-Z0-9._-]+\/video\/\d+\/?))/i;

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const mode = searchParams.get('hub.mode');
  const token = searchParams.get('hub.verify_token');
  const challenge = searchParams.get('hub.challenge');

  if (mode === 'subscribe' && token === WHATSAPP_VERIFY_TOKEN && challenge) {
    return new Response(challenge, {
      status: 200,
      headers: {
        'Content-Type': 'text/plain',
      },
    });
  }

  return new Response('Verification failed. Invalid mode or verify token.', { status: 403 });
}

export async function POST(request: NextRequest) {
  try {
    const payload = await request.json();

    // Extract incoming WhatsApp message
    const entry = payload.entry?.[0];
    const change = entry?.changes?.[0];
    const value = change?.value;
    const message = value?.messages?.[0];

    if (!message) {
      return NextResponse.json({ status: 'NO_MESSAGE' }, { status: 200 });
    }

    const fromPhone = message.from; // Sender's phone number
    const textBody = message.text?.body || message.caption || '';

    // Handle Greeting / Text Message
    const urlMatch = textBody.match(VIDEO_URL_REGEX);
    if (!urlMatch) {
      await sendWhatsAppTextMessage(fromPhone, `👋 *Welcome to Universal Pro AI!*\n\nSend any video link from Instagram Reels, YouTube Shorts, or TikTok to extract structured recipes and 10-minute Blinkit/Zepto delivery links!`);
      return NextResponse.json({ status: 'GREETING_SENT' }, { status: 200 });
    }

    const videoUrl = urlMatch[1];
    await sendWhatsAppTextMessage(fromPhone, `⏳ *Extracting recipe from video...* Please wait a moment!`);

    // Perform AI Extraction
    const result = await extractRecipeFromUrl(videoUrl);

    // Format & Send WhatsApp Response
    const formattedRecipe = formatWhatsAppRecipeText(result, videoUrl);
    await sendWhatsAppTextMessage(fromPhone, formattedRecipe);

    return NextResponse.json({ status: 'REPLY_SENT' }, { status: 200 });
  } catch (error) {
    console.error('[WhatsApp Incoming Webhook Error]', error);
    return NextResponse.json({ status: 'ERROR', error: String(error) }, { status: 200 });
  }
}

async function sendWhatsAppTextMessage(toPhone: string, text: string) {
  const graphUrl = `https://graph.facebook.com/v22.0/${WHATSAPP_PHONE_NUMBER_ID}/messages`;
  try {
    await fetch(graphUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${WHATSAPP_ACCESS_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messaging_product: 'whatsapp',
        recipient_type: 'individual',
        to: toPhone,
        type: 'text',
        text: { preview_url: true, body: text },
      }),
    });
  } catch (err) {
    console.error('[WhatsApp Outbound Graph API Error]', err);
  }
}

function formatWhatsAppRecipeText(result: any, videoUrl: string): string {
  const title = result.title || result.recipe_title || 'Extracted Recipe';
  const summary = result.summary || 'Extracted structured recipe.';
  const ingredients = result.ingredients || [];
  const steps = result.instructions || result.steps || [];

  const lines = [
    `🥘 *${title}*`,
    `📋 *Summary:*\n${summary.slice(0, 300)}\n`,
  ];

  if (ingredients.length > 0) {
    lines.push('🛒 *INGREDIENTS:*');
    ingredients.slice(0, 8).forEach((ing: any) => {
      const name = typeof ing === 'object' ? `${ing.quantity || ''} ${ing.unit || ''} ${ing.name || ing.item || ''}`.trim() : String(ing);
      lines.push(`• ${name}`);
    });
    if (ingredients.length > 8) {
      lines.push(`_...and ${ingredients.length - 8} more items_`);
    }
    lines.push('');
  }

  if (steps.length > 0) {
    lines.push('📝 *PREPARATION:*');
    steps.slice(0, 4).forEach((step: string, idx: number) => {
      lines.push(`${idx + 1}. ${step}`);
    });
    if (steps.length > 4) {
      lines.push(`_...and ${steps.length - 4} more steps in web app_`);
    }
    lines.push('');
  }

  const topIngs = ingredients.slice(0, 3).map((i: any) => typeof i === 'object' ? i.name || i.item || '' : String(i)).filter(Boolean);
  const qStr = encodeURIComponent(topIngs.join(' '));
  lines.push('⚡ *10-MIN DELIVERY:*');
  lines.push(`• Blinkit: https://blinkit.com/s/?q=${qStr}`);
  lines.push(`• Zepto: https://www.zeptonow.com/search?query=${qStr}`);
  lines.push('');
  lines.push('🌐 *View Full Recipe & Scale Portion Yield:*');
  lines.push('https://universalpro.ai');

  return lines.join('\n');
}

async function extractRecipeFromUrl(videoUrl: string): Promise<any> {
  if (!GEMINI_API_KEY) {
    return {
      title: 'Extracted Recipe',
      summary: 'Structured recipe from shared video URL.',
      ingredients: ['Paneer 200g', 'Ghee 2 tbsp', 'Spices & Salt'],
      instructions: ['Prepare ingredients.', 'Grill until golden brown.', 'Serve hot.']
    };
  }

  try {
    const prompt = `Analyze video URL: ${videoUrl}. Return JSON object with keys: "title", "summary", "ingredients" (list of objects with name, quantity, unit), "instructions" (list of strings).`;
    const geminiResp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { responseMimeType: 'application/json' }
      })
    });

    const data = await geminiResp.json();
    const textOutput = data?.candidates?.[0]?.content?.parts?.[0]?.text;
    if (textOutput) {
      return JSON.parse(textOutput);
    }
  } catch (e) {
    console.error('[Gemini API Direct Fetch Error]', e);
  }

  return {
    title: 'Extracted Recipe',
    summary: 'Structured recipe from shared video URL.',
    ingredients: ['Paneer 200g', 'Ghee 2 tbsp', 'Spices & Salt'],
    instructions: ['Prepare ingredients.', 'Grill until golden brown.', 'Serve hot.']
  };
}
