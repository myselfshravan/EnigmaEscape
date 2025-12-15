# Enigma Escape API

A serverless Flask API for the Enigma Escape game, designed to be hosted on Vercel.

## Overview

This API powers the Enigma Escape game, where players need to craft clever prompts to make an AI assistant say specific phrases. The game features multiple levels of increasing difficulty.

## API Endpoints

### 1. Validate Response
```http
POST /api/validate
```

Validates a user's prompt against a level's target phrase and returns the AI's response.

#### Request Body
```json
{
    "level": 0,  // Level number (0 to N-1)
    "prompt": "string"  // User's input prompt
}
```

#### Response
```json
{
    "content": "string",  // AI's response
    "type": "success" | "info" | "warning" | "error",  // Response type
    "tokens": 123  // Token count (only included for successful matches)
}
```

Response Types:
- `success`: The AI's response matched the target phrase
- `info`: Normal response, but didn't match the target
- `warning`: Prompt contained forbidden words
- `error`: Invalid request or error occurred

### 2. Get Levels
```http
GET /api/levels
```

Returns all available game levels.

#### Response
```json
[
    {
        "name": "string",
        "model": "string",
        "max_token": 100,
        "points": 100,
        "description": "string",
        "clue": "string",
        "phrase": "string"
    }
]
```

### 3. Health Check
```http
GET /api/health
```

Returns API health status.

#### Response
```json
{
    "status": "healthy",
    "environment": "development" | "production"
}
```

## Game Rules

1. Users cannot include words from the target phrase in their prompts
2. Certain words are forbidden in prompts:
   - replace
   - swap
   - change
   - modify
   - alter
   - substitute

## Response Validation

The API uses a combination of techniques to validate if the AI's response matches the target phrase:
1. Direct string matching after normalization
2. Fuzzy string matching with a similarity threshold
3. Sliding window comparison for partial matches

## Environment Variables

Required environment variables:
- `GROQ_API_KEY`: API key for the Groq LLM service

## Example Usage

```javascript
// Example: Validating a prompt
const response = await fetch('https://your-api.vercel.app/api/validate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        level: 0,
        prompt: "What's the typical first program output?"
    })
});

const result = await response.json();
console.log(result);
// {
//     "content": "hello world",
//     "type": "success",
//     "tokens": 45
// }

// Example: Getting all levels
const levels = await fetch('https://your-api.vercel.app/api/levels')
    .then(res => res.json());
```

## Development

1. Clone the repository
2. Install dependencies with uv:
   ```bash
   uv sync
   ```
3. Create a .env file with:
   ```
   GROQ_API_KEY=your_api_key_here
   ```
4. Run locally:
   ```bash
   uv run flask --app api.index run --host 0.0.0.0 --port 8000
   ```

## Deployment

1. Connect your repository to Vercel
2. Add the `GROQ_API_KEY` environment variable in Vercel
3. Deploy!

## Frontend Integration Tips

1. Show appropriate feedback based on response types:
   - `success`: Celebrate the user's achievement
   - `info`: Show the response and encourage trying again
   - `warning`: Alert about forbidden words
   - `error`: Display error message

2. Track completed levels using the response type `success`

3. Display level information:
   - Show the target phrase
   - Display the clue/hint
   - Show points available

4. Implement proper error handling for API requests

5. Consider adding a loading state while waiting for API response

## Error Handling

Common error scenarios to handle:
1. Invalid level number
2. Missing required fields
3. Network errors
4. API rate limiting
5. Server errors
