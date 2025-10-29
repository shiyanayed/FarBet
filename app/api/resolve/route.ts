import { NextRequest, NextResponse } from 'next/server';
import { createWalletClient, http, createPublicClient } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';
import axios from 'axios';

const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS as `0x${string}`;
const ORACLE_PRIVATE_KEY = process.env.ORACLE_PRIVATE_KEY as `0x${string}`;
const CRON_SECRET = process.env.CRON_SECRET;

const CONTRACT_ABI = [
  {
    name: 'resolveBet',
    type: 'function',
    stateMutability: 'nonpayable',
    inputs: [
      { name: '_betId', type: 'uint256' },
      { name: '_actualValue', type: 'uint256' },
    ],
    outputs: [],
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

/**
 * Oracle endpoint to resolve bets
 * Can be called by cron job or manually with secret
 */
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { secret, betId } = body;

    // Verify cron secret
    if (secret !== CRON_SECRET) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    if (!ORACLE_PRIVATE_KEY) {
      return NextResponse.json(
        { error: 'Oracle private key not configured' },
        { status: 500 }
      );
    }

    const account = privateKeyToAccount(ORACLE_PRIVATE_KEY);
    
    const publicClient = createPublicClient({
      chain: base,
      transport: http(process.env.BASE_RPC_URL || 'https://mainnet.base.org'),
    });

    const walletClient = createWalletClient({
      account,
      chain: base,
      transport: http(process.env.BASE_RPC_URL || 'https://mainnet.base.org'),
    });

    // Get bet details
    const bet = await publicClient.readContract({
      address: CONTRACT_ADDRESS,
      abi: CONTRACT_ABI,
      functionName: 'bets',
      args: [BigInt(betId)],
    });

    const fid = Number(bet[2]);
    const betType = Number(bet[3]);
    const resolutionTime = Number(bet[7]);
    const status = Number(bet[8]);

    // Check if bet is ready to resolve
    const now = Math.floor(Date.now() / 1000);
    if (now < resolutionTime) {
      return NextResponse.json(
        { error: 'Bet not ready to resolve yet', timeRemaining: resolutionTime - now },
        { status: 400 }
      );
    }

    if (status !== 0) {
      // Status 0 = ACTIVE
      return NextResponse.json(
        { error: 'Bet already resolved or cancelled' },
        { status: 400 }
      );
    }

    // Fetch actual value from Farcaster
    const statsResponse = await axios.get(
      `${process.env.NEXT_PUBLIC_APP_URL}/api/farcaster/stats?fid=${fid}`
    );
    const stats = statsResponse.data;

    let actualValue = 0;

    // Determine actual value based on bet type
    switch (betType) {
      case 0: // CASTS_COUNT
        actualValue = stats.castsCount24h;
        break;
      case 1: // LIKES_GREATER
      case 2: // LIKES_LESS
        actualValue = stats.totalLikes24h;
        break;
      case 3: // REPLIES_COUNT
        actualValue = stats.totalReplies24h;
        break;
      case 4: // FOLLOWERS_GAIN
        actualValue = stats.followerCount;
        break;
      default:
        return NextResponse.json({ error: 'Invalid bet type' }, { status: 400 });
    }

    // Resolve the bet on-chain
    const hash = await walletClient.writeContract({
      address: CONTRACT_ADDRESS,
      abi: CONTRACT_ABI,
      functionName: 'resolveBet',
      args: [BigInt(betId), BigInt(actualValue)],
    });

    // Wait for transaction confirmation
    const receipt = await publicClient.waitForTransactionReceipt({ hash });

    return NextResponse.json({
      success: true,
      betId,
      actualValue,
      transactionHash: hash,
      blockNumber: receipt.blockNumber,
    });
  } catch (error: any) {
    console.error('Resolution error:', error);
    return NextResponse.json(
      { error: 'Failed to resolve bet', details: error.message },
      { status: 500 }
    );
  }
}

/**
 * Get pending bets that need resolution
 */
export async function GET(req: NextRequest) {
  try {
    const searchParams = req.nextUrl.searchParams;
    const secret = searchParams.get('secret');

    if (secret !== CRON_SECRET) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // This would typically query events or maintain a database of pending bets
    // For simplicity, returning a message
    return NextResponse.json({
      message: 'Use POST /api/resolve with betId to resolve individual bets',
      note: 'Implement event listening or database tracking for production',
    });
  } catch (error: any) {
    console.error('Get pending bets error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch pending bets', details: error.message },
      { status: 500 }
    );
  }
}
