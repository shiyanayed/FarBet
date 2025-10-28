import { NextRequest, NextResponse } from 'next/server';
import { createPublicClient, http, formatEther } from 'viem';
import { base } from 'viem/chains';

const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS as `0x${string}`;

// Contract ABI (subset for reading)
const CONTRACT_ABI = [
  {
    name: 'getUserBets',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: '_user', type: 'address' }],
    outputs: [{ name: '', type: 'uint256[]' }],
  },
  {
    name: 'getBet',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: '_betId', type: 'uint256' }],
    outputs: [
      {
        name: '',
        type: 'tuple',
        components: [
          { name: 'betId', type: 'uint256' },
          { name: 'bettor', type: 'address' },
          { name: 'fid', type: 'uint256' },
          { name: 'betType', type: 'uint8' },
          { name: 'predictedValue', type: 'uint256' },
          { name: 'betAmount', type: 'uint256' },
          { name: 'timestamp', type: 'uint256' },
          { name: 'resolutionTime', type: 'uint256' },
          { name: 'status', type: 'uint8' },
          { name: 'actualValue', type: 'uint256' },
        ],
      },
    ],
  },
  {
    name: 'bets',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: '', type: 'uint256' }],
    outputs: [
      { name: 'betId', type: 'uint256' },
      { name: 'bettor', type: 'address' },
      { name: 'fid', type: 'uint256' },
      { name: 'betType', type: 'uint8' },
      { name: 'predictedValue', type: 'uint256' },
      { name: 'betAmount', type: 'uint256' },
      { name: 'timestamp', type: 'uint256' },
      { name: 'resolutionTime', type: 'uint256' },
      { name: 'status', type: 'uint8' },
      { name: 'actualValue', type: 'uint256' },
    ],
  },
] as const;

const publicClient = createPublicClient({
  chain: base,
  transport: http(process.env.BASE_RPC_URL || 'https://mainnet.base.org'),
});

const BET_TYPE_NAMES = [
  'Casts Count',
  'Likes Greater',
  'Likes Less',
  'Replies Count',
  'Followers Gain',
];

const STATUS_NAMES = ['Active', 'Won', 'Lost', 'Cancelled'];

/**
 * Get bets for a user or specific bet
 */
export async function GET(req: NextRequest) {
  try {
    const searchParams = req.nextUrl.searchParams;
    const address = searchParams.get('address');
    const betId = searchParams.get('betId');

    if (!CONTRACT_ADDRESS) {
      return NextResponse.json(
        { error: 'Contract address not configured' },
        { status: 500 }
      );
    }

    // Get specific bet
    if (betId) {
      const bet = await publicClient.readContract({
        address: CONTRACT_ADDRESS,
        abi: CONTRACT_ABI,
        functionName: 'bets',
        args: [BigInt(betId)],
      });

      const formattedBet = {
        betId: Number(bet[0]),
        bettor: bet[1],
        fid: Number(bet[2]),
        betType: BET_TYPE_NAMES[bet[3]] || `Unknown (${bet[3]})`,
        betTypeEnum: Number(bet[3]),
        predictedValue: Number(bet[4]),
        betAmount: formatEther(bet[5]),
        timestamp: Number(bet[6]),
        resolutionTime: Number(bet[7]),
        status: STATUS_NAMES[bet[8]] || `Unknown (${bet[8]})`,
        statusEnum: Number(bet[8]),
        actualValue: Number(bet[9]),
        timeRemaining: Math.max(0, Number(bet[7]) - Math.floor(Date.now() / 1000)),
      };

      return NextResponse.json(formattedBet);
    }

    // Get user's bets
    if (address) {
      const betIds = await publicClient.readContract({
        address: CONTRACT_ADDRESS,
        abi: CONTRACT_ABI,
        functionName: 'getUserBets',
        args: [address as `0x${string}`],
      });

      const bets = await Promise.all(
        betIds.map(async (id) => {
          const bet = await publicClient.readContract({
            address: CONTRACT_ADDRESS,
            abi: CONTRACT_ABI,
            functionName: 'bets',
            args: [id],
          });

          return {
            betId: Number(bet[0]),
            bettor: bet[1],
            fid: Number(bet[2]),
            betType: BET_TYPE_NAMES[bet[3]] || `Unknown (${bet[3]})`,
            betTypeEnum: Number(bet[3]),
            predictedValue: Number(bet[4]),
            betAmount: formatEther(bet[5]),
            timestamp: Number(bet[6]),
            resolutionTime: Number(bet[7]),
            status: STATUS_NAMES[bet[8]] || `Unknown (${bet[8]})`,
            statusEnum: Number(bet[8]),
            actualValue: Number(bet[9]),
            timeRemaining: Math.max(0, Number(bet[7]) - Math.floor(Date.now() / 1000)),
          };
        })
      );

      return NextResponse.json({
        address,
        betsCount: bets.length,
        bets: bets.sort((a, b) => b.timestamp - a.timestamp), // Most recent first
      });
    }

    return NextResponse.json(
      { error: 'Address or betId parameter required' },
      { status: 400 }
    );
  } catch (error: any) {
    console.error('Bets API error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch bets', details: error.message },
      { status: 500 }
    );
  }
}
