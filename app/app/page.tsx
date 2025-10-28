'use client';

import { useState, useEffect } from 'react';
import { useAccount, useConnect, useDisconnect, useWalletClient } from 'wagmi';
import { parseEther, formatEther } from 'viem';

export default function AppPage() {
  const { address, isConnected } = useAccount();
  const { connect, connectors } = useConnect();
  const { disconnect } = useDisconnect();
  const { data: walletClient } = useWalletClient();

  const [bets, setBets] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'place' | 'history'>('place');

  // Bet form state
  const [betType, setBetType] = useState<'casts' | 'likes_greater' | 'likes_less'>('casts');
  const [targetFid, setTargetFid] = useState('');
  const [predictedValue, setPredictedValue] = useState('');
  const [betAmount, setBetAmount] = useState('0.001');

  useEffect(() => {
    if (isConnected && address) {
      fetchUserBets();
    }
  }, [isConnected, address]);

  const fetchUserBets = async () => {
    if (!address) return;
    
    setLoading(true);
    try {
      const response = await fetch(`/api/bets?address=${address}`);
      const data = await response.json();
      setBets(data.bets || []);
    } catch (error) {
      console.error('Error fetching bets:', error);
    }
    setLoading(false);
  };

  const handlePlaceBet = async () => {
    if (!walletClient || !address) {
      alert('Please connect your wallet');
      return;
    }

    if (!targetFid || !predictedValue) {
      alert('Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS as `0x${string}`;
      const BASE_FEE = parseEther('0.0002'); // ~$0.20
      const amount = parseEther(betAmount);
      const total = amount + BASE_FEE;

      let betTypeEnum = 0;
      if (betType === 'likes_greater') betTypeEnum = 1;
      if (betType === 'likes_less') betTypeEnum = 2;

      const hash = await walletClient.writeContract({
        address: CONTRACT_ADDRESS,
        abi: [
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
        ],
        functionName: 'placeBet',
        args: [BigInt(targetFid), betTypeEnum, BigInt(predictedValue), amount],
        value: total,
      });

      alert(`Bet placed successfully! Transaction: ${hash}`);
      
      // Reset form
      setTargetFid('');
      setPredictedValue('');
      
      // Refresh bets
      setTimeout(fetchUserBets, 3000);
    } catch (error: any) {
      console.error('Error placing bet:', error);
      alert(`Error: ${error.message}`);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-600 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-800">
              🎯 Prediction Market
            </h1>
            
            {isConnected ? (
              <div className="flex items-center gap-4">
                <div className="text-sm">
                  <div className="text-gray-500">Connected</div>
                  <div className="font-mono text-xs">
                    {address?.slice(0, 6)}...{address?.slice(-4)}
                  </div>
                </div>
                <button
                  onClick={() => disconnect()}
                  className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-medium"
                >
                  Disconnect
                </button>
              </div>
            ) : (
              <button
                onClick={() => connect({ connector: connectors[0] })}
                className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium"
              >
                Connect Wallet
              </button>
            )}
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('place')}
              className={`flex-1 py-4 px-6 font-semibold ${
                activeTab === 'place'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Place Bet
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`flex-1 py-4 px-6 font-semibold ${
                activeTab === 'history'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              My Bets ({bets.length})
            </button>
          </div>

          <div className="p-6">
            {activeTab === 'place' && (
              <div className="max-w-2xl mx-auto">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">
                  Place a New Bet
                </h2>

                <div className="space-y-6">
                  {/* Bet Type */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Bet Type
                    </label>
                    <select
                      value={betType}
                      onChange={(e) => setBetType(e.target.value as any)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                      <option value="casts">Cast Count (exact match)</option>
                      <option value="likes_greater">Likes Greater Than</option>
                      <option value="likes_less">Likes Less Than</option>
                    </select>
                  </div>

                  {/* Target FID */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Target User FID
                    </label>
                    <input
                      type="number"
                      value={targetFid}
                      onChange={(e) => setTargetFid(e.target.value)}
                      placeholder="e.g., 3621"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                    <p className="mt-1 text-sm text-gray-500">
                      The Farcaster ID of the user you want to bet on
                    </p>
                  </div>

                  {/* Predicted Value */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {betType === 'casts' ? 'Predicted Cast Count' : 'Likes Threshold'}
                    </label>
                    <input
                      type="number"
                      value={predictedValue}
                      onChange={(e) => setPredictedValue(e.target.value)}
                      placeholder={betType === 'casts' ? 'e.g., 10' : 'e.g., 100'}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                    <p className="mt-1 text-sm text-gray-500">
                      {betType === 'casts'
                        ? 'Exact number of casts in next 24 hours'
                        : 'Threshold for total likes in next 24 hours'}
                    </p>
                  </div>

                  {/* Bet Amount */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Bet Amount (ETH)
                    </label>
                    <input
                      type="number"
                      step="0.001"
                      value={betAmount}
                      onChange={(e) => setBetAmount(e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                    <p className="mt-1 text-sm text-gray-500">
                      Base fee: 0.0002 ETH (~$0.20) • Winning fee: 1.5%
                    </p>
                  </div>

                  {/* Fee Summary */}
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-gray-800 mb-2">Fee Summary</h3>
                    <div className="space-y-1 text-sm text-gray-600">
                      <div className="flex justify-between">
                        <span>Bet Amount:</span>
                        <span className="font-medium">{betAmount} ETH</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Base Fee:</span>
                        <span className="font-medium">0.0002 ETH</span>
                      </div>
                      <div className="flex justify-between font-semibold text-gray-800 pt-2 border-t">
                        <span>Total:</span>
                        <span>{(parseFloat(betAmount) + 0.0002).toFixed(4)} ETH</span>
                      </div>
                    </div>
                  </div>

                  {/* Submit Button */}
                  <button
                    onClick={handlePlaceBet}
                    disabled={loading || !isConnected}
                    className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold py-4 px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all"
                  >
                    {loading ? 'Processing...' : 'Place Bet'}
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'history' && (
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-6">
                  Your Bet History
                </h2>

                {!isConnected ? (
                  <div className="text-center py-12 text-gray-500">
                    Connect your wallet to view your bets
                  </div>
                ) : loading ? (
                  <div className="text-center py-12 text-gray-500">
                    Loading...
                  </div>
                ) : bets.length === 0 ? (
                  <div className="text-center py-12 text-gray-500">
                    No bets yet. Place your first bet to get started!
                  </div>
                ) : (
                  <div className="space-y-4">
                    {bets.map((bet) => (
                      <div
                        key={bet.betId}
                        className="bg-gray-50 p-6 rounded-lg border-2 border-gray-200"
                      >
                        <div className="flex justify-between items-start mb-4">
                          <div>
                            <h3 className="text-lg font-semibold text-gray-800">
                              {bet.betType}
                            </h3>
                            <p className="text-sm text-gray-500">
                              Bet #{bet.betId} • Target FID: {bet.fid}
                            </p>
                          </div>
                          <span
                            className={`px-3 py-1 rounded-full text-sm font-medium ${
                              bet.status === 'Won'
                                ? 'bg-green-100 text-green-800'
                                : bet.status === 'Lost'
                                ? 'bg-red-100 text-red-800'
                                : 'bg-yellow-100 text-yellow-800'
                            }`}
                          >
                            {bet.status}
                          </span>
                        </div>

                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <div className="text-gray-500">Predicted Value</div>
                            <div className="font-semibold">{bet.predictedValue}</div>
                          </div>
                          {bet.actualValue > 0 && (
                            <div>
                              <div className="text-gray-500">Actual Value</div>
                              <div className="font-semibold">{bet.actualValue}</div>
                            </div>
                          )}
                          <div>
                            <div className="text-gray-500">Bet Amount</div>
                            <div className="font-semibold">{bet.betAmount} ETH</div>
                          </div>
                          {bet.timeRemaining > 0 && (
                            <div>
                              <div className="text-gray-500">Resolves In</div>
                              <div className="font-semibold">
                                {Math.floor(bet.timeRemaining / 3600)}h{' '}
                                {Math.floor((bet.timeRemaining % 3600) / 60)}m
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
