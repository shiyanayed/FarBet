import { NextRequest, NextResponse } from 'next/server';
import { encodeFunctionData, parseEther } from 'viem';

const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS as `0x${string}`;
const BASE_FEE = '0.0002'; // 0.0002 ETH ≈ $0.20 (adjust based on ETH price)

// ABI for placeBet function
const PLACE_BET_ABI = [
  {
    name: 'placeBet',
    type: 'function',
    stateMutability: 'payable',
    inputs: [
      { name: '_fid', type: 'uint256' },
      { name: '_betType', type: 'uint8' },
      { name: '_predictedValue', type: 'uint256' },
      { name: '_betAmount', type: 'uint256' },
    ],
    outputs: [{ name: '', type: 'uint256' }],
  },
] as const;

export async function POST(req: NextRequest) {
  try {
    const searchParams = req.nextUrl.searchParams;
    const betType = searchParams.get('type');
    const data = searchParams.get('data');
    const userFid = searchParams.get('fid');

    if (!data) {
      return NextResponse.json({ error: 'Missing bet data' }, { status: 400 });
    }

    let fid: number;
    let betTypeEnum: number;
    let predictedValue: number;
    let betAmount = parseEther('0.001'); // Minimum bet amount (adjust as needed)

    // Parse input based on bet type
    if (betType === 'casts') {
      const [targetFid, count] = data.split(':').map(Number);
      fid = targetFid;
      betTypeEnum = 0; // BetType.CASTS_COUNT
      predictedValue = count;
    } else if (betType === 'likes') {
      const parts = data.split(':');
      fid = Number(parts[0]);
      const threshold = Number(parts[1]);
      const direction = parts[2]?.toLowerCase();
      
      betTypeEnum = direction === 'greater' ? 1 : 2; // LIKES_GREATER or LIKES_LESS
      predictedValue = threshold;
    } else {
      return NextResponse.json({ error: 'Invalid bet type' }, { status: 400 });
    }

    // Calculate total payment (bet amount + base fee)
    const totalValue = parseEther('0.001') + parseEther(BASE_FEE);

    // Encode the function call
    const calldata = encodeFunctionData({
      abi: PLACE_BET_ABI,
      functionName: 'placeBet',
      args: [
        BigInt(fid),
        betTypeEnum,
        BigInt(predictedValue),
        parseEther('0.001'),
      ],
    });

    // Return transaction request in Farcaster Frames format
    return NextResponse.json({
      chainId: `eip155:${process.env.NEXT_PUBLIC_CHAIN_ID || '8453'}`, // Base mainnet
      method: 'eth_sendTransaction',
      params: {
        abi: PLACE_BET_ABI,
        to: CONTRACT_ADDRESS,
        data: calldata,
        value: totalValue.toString(),
      },
    });
  } catch (error) {
    console.error('Transaction error:', error);
    return NextResponse.json(
      { error: 'Failed to create transaction' },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({ message: 'Transaction API' });
}
