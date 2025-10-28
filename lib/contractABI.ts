export const PREDICTION_MARKET_ABI = [
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
    name: 'BetPlaced',
    type: 'event',
    inputs: [
      { name: 'betId', type: 'uint256', indexed: true },
      { name: 'bettor', type: 'address', indexed: true },
      { name: 'fid', type: 'uint256', indexed: false },
      { name: 'betType', type: 'uint8', indexed: false },
      { name: 'amount', type: 'uint256', indexed: false },
      { name: 'predictedValue', type: 'uint256', indexed: false },
    ],
  },
  {
    name: 'BetResolved',
    type: 'event',
    inputs: [
      { name: 'betId', type: 'uint256', indexed: true },
      { name: 'status', type: 'uint8', indexed: false },
      { name: 'actualValue', type: 'uint256', indexed: false },
      { name: 'payout', type: 'uint256', indexed: false },
    ],
  },
] as const;

export enum BetType {
  CASTS_COUNT = 0,
  LIKES_GREATER = 1,
  LIKES_LESS = 2,
  REPLIES_COUNT = 3,
  FOLLOWERS_GAIN = 4,
}

export enum BetStatus {
  ACTIVE = 0,
  RESOLVED_WON = 1,
  RESOLVED_LOST = 2,
  CANCELLED = 3,
}
