import { ImageResponse } from 'next/og';
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function GET(req: NextRequest) {
  const searchParams = req.nextUrl.searchParams;
  const screen = searchParams.get('screen') || 'home';
  const data = searchParams.get('data') || '';
  const fid = searchParams.get('fid') || '';

  const width = 1200;
  const height = 630;

  let content;

  switch (screen) {
    case 'home':
      content = (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(to bottom right, #7c3aed, #2563eb)',
          padding: '40px',
        }}>
          <div style={{
            fontSize: 72,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: '20px',
          }}>
            🎯 Prediction Market
          </div>
          <div style={{
            fontSize: 36,
            color: 'rgba(255,255,255,0.9)',
            textAlign: 'center',
          }}>
            Bet on Farcaster User Stats
          </div>
          <div style={{
            fontSize: 28,
            color: 'rgba(255,255,255,0.8)',
            marginTop: '30px',
          }}>
            Choose your bet type to get started!
          </div>
        </div>
      );
      break;

    case 'bet_casts':
      content = (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(to bottom right, #7c3aed, #2563eb)',
          padding: '40px',
        }}>
          <div style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: '30px',
          }}>
            📝 Bet on Cast Count
          </div>
          <div style={{
            fontSize: 32,
            color: 'rgba(255,255,255,0.9)',
            textAlign: 'center',
            marginBottom: '20px',
          }}>
            Predict how many casts a user will make in 24 hours
          </div>
          <div style={{
            fontSize: 24,
            color: 'rgba(255,255,255,0.8)',
            textAlign: 'center',
            padding: '20px',
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '10px',
          }}>
            Format: [FID]:[Predicted Count]
            <br />
            Example: 123:10
          </div>
        </div>
      );
      break;

    case 'bet_likes':
      content = (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(to bottom right, #7c3aed, #2563eb)',
          padding: '40px',
        }}>
          <div style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: '30px',
          }}>
            ❤️ Bet on Likes
          </div>
          <div style={{
            fontSize: 32,
            color: 'rgba(255,255,255,0.9)',
            textAlign: 'center',
            marginBottom: '20px',
          }}>
            Predict if likes will be greater/less than threshold
          </div>
          <div style={{
            fontSize: 24,
            color: 'rgba(255,255,255,0.8)',
            textAlign: 'center',
            padding: '20px',
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '10px',
          }}>
            Format: [FID]:[Threshold]:[greater/less]
            <br />
            Example: 123:100:greater
          </div>
        </div>
      );
      break;

    case 'confirm':
      content = (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(to bottom right, #7c3aed, #2563eb)',
          padding: '40px',
        }}>
          <div style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: '30px',
          }}>
            ✅ Confirm Your Bet
          </div>
          <div style={{
            fontSize: 28,
            color: 'rgba(255,255,255,0.9)',
            marginBottom: '20px',
          }}>
            Bet Details: {data}
          </div>
          <div style={{
            fontSize: 24,
            color: 'rgba(255,255,255,0.8)',
            padding: '20px',
            background: 'rgba(255,255,255,0.1)',
            borderRadius: '10px',
          }}>
            Base Fee: $0.20
            <br />
            Winning Fee: 1.5%
          </div>
        </div>
      );
      break;

    case 'success':
      content = (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(to bottom right, #10b981, #059669)',
          padding: '40px',
        }}>
          <div style={{
            fontSize: 96,
            marginBottom: '20px',
          }}>
            🎉
          </div>
          <div style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: '20px',
          }}>
            Bet Placed!
          </div>
          <div style={{
            fontSize: 32,
            color: 'rgba(255,255,255,0.9)',
            textAlign: 'center',
          }}>
            Your bet will be resolved in 24 hours
          </div>
        </div>
      );
      break;

    case 'my_bets':
      content = (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(to bottom right, #7c3aed, #2563eb)',
          padding: '40px',
        }}>
          <div style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: '30px',
          }}>
            📊 Your Bets
          </div>
          <div style={{
            fontSize: 28,
            color: 'rgba(255,255,255,0.9)',
            textAlign: 'center',
          }}>
            FID: {fid}
          </div>
          <div style={{
            fontSize: 24,
            color: 'rgba(255,255,255,0.8)',
            marginTop: '20px',
          }}>
            Check the app for detailed bet history
          </div>
        </div>
      );
      break;

    case 'error':
      content = (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(to bottom right, #dc2626, #991b1b)',
          padding: '40px',
        }}>
          <div style={{
            fontSize: 96,
            marginBottom: '20px',
          }}>
            ❌
          </div>
          <div style={{
            fontSize: 64,
            fontWeight: 'bold',
            color: 'white',
            marginBottom: '20px',
          }}>
            Oops! Something went wrong
          </div>
          <div style={{
            fontSize: 32,
            color: 'rgba(255,255,255,0.9)',
          }}>
            Please try again
          </div>
        </div>
      );
      break;

    default:
      content = (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(to bottom right, #7c3aed, #2563eb)',
        }}>
          <div style={{
            fontSize: 72,
            fontWeight: 'bold',
            color: 'white',
          }}>
            Farcaster Prediction Market
          </div>
        </div>
      );
  }

  return new ImageResponse(content, {
    width,
    height,
  });
}
