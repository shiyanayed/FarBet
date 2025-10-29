import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

const NEYNAR_API_KEY = process.env.NEYNAR_API_KEY;
const NEYNAR_BASE_URL = 'https://api.neynar.com/v2';

/**
 * Fetch Farcaster user statistics
 */
export async function GET(req: NextRequest) {
  try {
    const searchParams = req.nextUrl.searchParams;
    const fid = searchParams.get('fid');
    const statType = searchParams.get('type') || 'all';

    if (!fid) {
      return NextResponse.json({ error: 'FID is required' }, { status: 400 });
    }

    if (!NEYNAR_API_KEY) {
      return NextResponse.json(
        { error: 'Neynar API key not configured' },
        { status: 500 }
      );
    }

    // Fetch user data from Neynar
    const userResponse = await axios.get(
      `${NEYNAR_BASE_URL}/farcaster/user/bulk`,
      {
        params: { fids: fid },
        headers: { api_key: NEYNAR_API_KEY },
      }
    );

    const userData = userResponse.data.users[0];

    if (!userData) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 });
    }

    // Get user's recent casts for the last 24 hours
    const castsResponse = await axios.get(
      `${NEYNAR_BASE_URL}/farcaster/feed/user/${fid}/casts`,
      {
        params: { limit: 100 },
        headers: { api_key: NEYNAR_API_KEY },
      }
    );

    const now = Date.now();
    const twentyFourHoursAgo = now - 24 * 60 * 60 * 1000;

    const recentCasts = castsResponse.data.casts.filter((cast: any) => {
      const castTime = new Date(cast.timestamp).getTime();
      return castTime >= twentyFourHoursAgo;
    });

    // Calculate statistics
    const stats = {
      fid: Number(fid),
      username: userData.username,
      displayName: userData.display_name,
      followerCount: userData.follower_count || 0,
      followingCount: userData.following_count || 0,
      
      // 24-hour stats
      castsCount24h: recentCasts.length,
      totalLikes24h: recentCasts.reduce((sum: number, cast: any) => 
        sum + (cast.reactions?.likes_count || 0), 0
      ),
      totalReplies24h: recentCasts.reduce((sum: number, cast: any) => 
        sum + (cast.replies?.count || 0), 0
      ),
      totalRecasts24h: recentCasts.reduce((sum: number, cast: any) => 
        sum + (cast.reactions?.recasts_count || 0), 0
      ),
      
      // Overall stats
      totalCasts: userData.active_status?.casts_count || 0,
      pfpUrl: userData.pfp_url,
      bioText: userData.profile?.bio?.text || '',
      
      timestamp: now,
    };

    // Filter by requested stat type
    if (statType !== 'all') {
      const filteredStats: any = { fid: stats.fid, username: stats.username };
      
      switch (statType) {
        case 'casts':
          filteredStats.castsCount24h = stats.castsCount24h;
          break;
        case 'likes':
          filteredStats.totalLikes24h = stats.totalLikes24h;
          break;
        case 'replies':
          filteredStats.totalReplies24h = stats.totalReplies24h;
          break;
        case 'followers':
          filteredStats.followerCount = stats.followerCount;
          break;
        default:
          return NextResponse.json(stats);
      }
      
      return NextResponse.json(filteredStats);
    }

    return NextResponse.json(stats);
  } catch (error: any) {
    console.error('Farcaster stats error:', error.response?.data || error.message);
    return NextResponse.json(
      { error: 'Failed to fetch Farcaster stats', details: error.message },
      { status: 500 }
    );
  }
}
