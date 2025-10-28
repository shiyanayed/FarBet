import { NextRequest, NextResponse } from 'next/server';

const APP_URL = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { untrustedData } = body;
    const { buttonIndex, fid } = untrustedData;

    // Step through the frame flow
    let imageUrl = `${APP_URL}/api/og`;
    let buttons: any[] = [];
    let postUrl = `${APP_URL}/api/frame`;
    let inputText = '';

    // State machine for frame navigation
    const state = req.nextUrl.searchParams.get('state') || 'home';

    switch (state) {
      case 'home':
        imageUrl = `${APP_URL}/api/og?screen=home`;
        buttons = [
          { label: 'Casts Count', action: 'post', target: `${APP_URL}/api/frame?state=bet_casts` },
          { label: 'Likes Prediction', action: 'post', target: `${APP_URL}/api/frame?state=bet_likes` },
          { label: 'View My Bets', action: 'post', target: `${APP_URL}/api/frame?state=my_bets&fid=${fid}` },
        ];
        break;

      case 'bet_casts':
        imageUrl = `${APP_URL}/api/og?screen=bet_casts`;
        inputText = 'Enter FID and predicted cast count (e.g., 123:10)';
        buttons = [
          { label: 'Place Bet', action: 'post', target: `${APP_URL}/api/frame?state=confirm_bet&type=casts` },
          { label: 'Back', action: 'post', target: `${APP_URL}/api/frame?state=home` },
        ];
        break;

      case 'bet_likes':
        imageUrl = `${APP_URL}/api/og?screen=bet_likes`;
        inputText = 'Enter FID and threshold (e.g., 123:100:greater)';
        buttons = [
          { label: 'Place Bet', action: 'post', target: `${APP_URL}/api/frame?state=confirm_bet&type=likes` },
          { label: 'Back', action: 'post', target: `${APP_URL}/api/frame?state=home` },
        ];
        break;

      case 'confirm_bet':
        const betType = req.nextUrl.searchParams.get('type');
        const inputData = untrustedData.inputText || '';
        
        // Parse input and create transaction
        imageUrl = `${APP_URL}/api/og?screen=confirm&data=${encodeURIComponent(inputData)}`;
        buttons = [
          { 
            label: 'Confirm & Pay', 
            action: 'tx',
            target: `${APP_URL}/api/transaction?type=${betType}&data=${encodeURIComponent(inputData)}&fid=${fid}`,
            post_url: `${APP_URL}/api/frame?state=success`
          },
          { label: 'Cancel', action: 'post', target: `${APP_URL}/api/frame?state=home` },
        ];
        break;

      case 'success':
        imageUrl = `${APP_URL}/api/og?screen=success`;
        buttons = [
          { label: 'Place Another Bet', action: 'post', target: `${APP_URL}/api/frame?state=home` },
          { label: 'View My Bets', action: 'post', target: `${APP_URL}/api/frame?state=my_bets&fid=${fid}` },
        ];
        break;

      case 'my_bets':
        const userFid = req.nextUrl.searchParams.get('fid') || fid;
        imageUrl = `${APP_URL}/api/og?screen=my_bets&fid=${userFid}`;
        buttons = [
          { label: 'Place New Bet', action: 'post', target: `${APP_URL}/api/frame?state=home` },
          { label: 'Refresh', action: 'post', target: `${APP_URL}/api/frame?state=my_bets&fid=${userFid}` },
        ];
        break;

      default:
        imageUrl = `${APP_URL}/api/og?screen=home`;
        buttons = [
          { label: 'Place a Bet', action: 'post', target: `${APP_URL}/api/frame?state=home` },
        ];
    }

    // Build frame response
    const frameResponse: any = {
      version: 'vNext',
      image: imageUrl,
      buttons: buttons.map((btn, idx) => ({
        index: idx + 1,
        label: btn.label,
        action: btn.action || 'post',
        target: btn.target,
        post_url: btn.post_url,
      })),
    };

    if (inputText) {
      frameResponse.input = {
        text: inputText,
      };
    }

    return NextResponse.json(frameResponse);
  } catch (error) {
    console.error('Frame error:', error);
    return NextResponse.json({
      version: 'vNext',
      image: `${APP_URL}/api/og?screen=error`,
      buttons: [
        { index: 1, label: 'Try Again', action: 'post', target: `${APP_URL}/api/frame` },
      ],
    });
  }
}

export async function GET() {
  return NextResponse.json({ message: 'Farcaster Frame API' });
}
