import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Farcaster Prediction Market',
  description: 'Bet on Farcaster user statistics and win!',
  openGraph: {
    title: 'Farcaster Prediction Market',
    description: 'Bet on Farcaster user statistics and win!',
    images: [`${process.env.NEXT_PUBLIC_APP_URL}/api/og`],
  },
  other: {
    'fc:frame': 'vNext',
    'fc:frame:image': `${process.env.NEXT_PUBLIC_APP_URL}/api/og`,
    'fc:frame:button:1': 'Place a Bet',
    'fc:frame:button:1:action': 'post',
    'fc:frame:post_url': `${process.env.NEXT_PUBLIC_APP_URL}/api/frame`,
  },
};

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-white rounded-2xl shadow-2xl p-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-4 text-center">
          🎯 Farcaster Prediction Market
        </h1>
        <p className="text-xl text-gray-600 mb-8 text-center">
          Bet on Farcaster user statistics and win big!
        </p>
        
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-purple-50 p-6 rounded-xl">
            <h2 className="text-2xl font-semibold text-purple-800 mb-3">📊 What You Can Bet On</h2>
            <ul className="space-y-2 text-gray-700">
              <li>✓ Number of casts in 24 hours</li>
              <li>✓ Total likes received in 24 hours</li>
              <li>✓ Number of replies</li>
              <li>✓ Follower growth</li>
              <li>✓ And more!</li>
            </ul>
          </div>
          
          <div className="bg-blue-50 p-6 rounded-xl">
            <h2 className="text-2xl font-semibold text-blue-800 mb-3">💰 Fee Structure</h2>
            <ul className="space-y-2 text-gray-700">
              <li>📌 Base Fee: $0.20 per bet</li>
              <li>🏆 Winning Fee: 1.5% on withdrawal</li>
              <li>💳 Direct wallet payment</li>
              <li>⚡ No deposits required</li>
            </ul>
          </div>
        </div>
        
        <div className="bg-gradient-to-r from-purple-100 to-blue-100 p-6 rounded-xl mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-3">🚀 How It Works</h2>
          <ol className="space-y-3 text-gray-700">
            <li><strong>1.</strong> Connect your wallet to your Farcaster account</li>
            <li><strong>2.</strong> Choose a user and prediction type</li>
            <li><strong>3.</strong> Place your bet (minimum $0.20 base fee)</li>
            <li><strong>4.</strong> Wait 24 hours for resolution</li>
            <li><strong>5.</strong> Collect your winnings (if you win!)</li>
          </ol>
        </div>
        
        <div className="text-center">
          <a 
            href="/app" 
            className="inline-block bg-gradient-to-r from-purple-600 to-blue-600 text-white font-bold py-4 px-8 rounded-full text-xl hover:shadow-lg transform hover:scale-105 transition-all"
          >
            Launch App
          </a>
        </div>
        
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>Built on Base • Powered by Farcaster</p>
        </div>
      </div>
    </main>
  );
}
