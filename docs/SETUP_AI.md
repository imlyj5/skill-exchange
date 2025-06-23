# AI Matching Setup Guide

This guide will help you set up the AI-powered matching feature using Google's Gemini API.

## Prerequisites

1. A Google account
2. Access to Google AI Studio (free)

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## Step 2: Set Environment Variable

Add the API key to your environment:

```bash
export GEMINI_API_KEY="your-actual-api-key-here"
```

For development, add it to your `.env` file in the backend directory:

```env
GEMINI_API_KEY=your-actual-api-key-here
```

## Step 3: Test the Setup

Start your Flask application and test the matching endpoint:

```bash
cd backend
flask run
```

Then make a request to test AI matching:

```bash
curl http://localhost:5000/matches/1
```

You should see a response like:
```json
{
  "matches": [
    {
      "id": 2,
      "name": "Jane",
      "email": "jane@gmail.com",
      "offer_matches": ["music matches music theory", "cooking matches cooking"],
      "learn_matches": ["python matches programming"]
    }
  ],
  "count": 1,
  "ai_enabled": true
}
```

## Step 4: Verify AI is Working

Check that AI matching is enabled by looking for `"ai_enabled": true` in the response. If you see `"ai_enabled": false`, the API key is not properly configured.

## Features Enabled

With AI matching enabled, your app will now:

1. Intelligently match skills: "violin" will match with "music", "cooking" with "baking", etc.
2. Find compatible skill pairs: Users can match if they can teach what the other wants to learn
3. Show match details: Display which specific skills matched between users
4. If AI is unavailable, falls back to exact matching

## How AI Matching Works

The AI matching system:

1. Checks skill compatibility: Uses AI to determine if skills are related (e.g., "piano" and "music theory")
2. Finds bidirectional matches: Ensures both users can benefit from the exchange
3. Returns match details: Shows exactly which skills matched for transparency
4. Falls back to exact matching if AI calls fail

## Troubleshooting

### "ai_enabled": false in response
- Make sure you've set the `GEMINI_API_KEY` environment variable correctly
- Restart your Flask application after setting the environment variable
- Check that the API key is valid and has proper permissions

### API Rate Limits
- The system includes rate limiting (0.1 second delay between calls)

### Fallback Behavior
- If the API is unavailable, the app falls back to exact matching
- No functionality is lost, just enhanced features are disabled
- Users will still find matches, but only with identical skill names