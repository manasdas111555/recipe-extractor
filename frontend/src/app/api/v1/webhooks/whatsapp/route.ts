import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const mode = searchParams.get('hub.mode');
  const token = searchParams.get('hub.verify_token');
  const challenge = searchParams.get('hub.challenge');

  const expectedToken = process.env.WHATSAPP_VERIFY_TOKEN || 'universal_pro_verify_token';

  if (mode === 'subscribe' && token === expectedToken && challenge) {
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
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
    
    // Forward incoming webhook asynchronously to FastAPI backend if available
    if (apiUrl && !apiUrl.includes('127.0.0.1')) {
      fetch(`${apiUrl}/api/v1/webhooks/whatsapp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      }).catch((err) => console.error('[WhatsApp Webhook Proxy Error]', err));
    }
    
    return NextResponse.json({ status: 'RECEIVED' }, { status: 200 });
  } catch (error) {
    return NextResponse.json({ status: 'ERROR', error: String(error) }, { status: 200 });
  }
}
