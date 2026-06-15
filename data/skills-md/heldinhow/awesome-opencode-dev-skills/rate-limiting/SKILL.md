---
name: rate-limiting
description: "Implement API rate limiting to control request frequency and prevent abuse."
---

# API Rate Limiting

## Overview
Rate limiting controls the number of requests a client can make within a time window, protecting APIs from abuse, ensuring fair usage, and preventing backend overload. This skill should be invoked when protecting APIs from abuse, ensuring fair usage among clients, or preventing backend services from being overwhelmed.

## Core Principles
- **Algorithm Selection**: Choose appropriate algorithm (token bucket, sliding window, fixed window)
- **Granularity**: Rate limit by user, IP, API key, or endpoint
- **Graceful Degradation**: Return proper HTTP status codes (429) with retry information
- **Transparency**: Include rate limit headers in responses

## Preparation Checklist
- [ ] Identify rate limit dimensions (per user, per IP, per endpoint)
- [ ] Choose storage backend (Redis for distributed, in-memory for single instance)
- [ ] Define rate limit parameters (requests per minute/hour)
- [ ] Plan response format for throttled requests

## Step-by-Step Process
1. **Select Algorithm**: Choose token bucket, sliding window, or fixed window
2. **Configure Limits**: Define requests per time window
3. **Implement Middleware**: Create rate checking middleware
4. **Add Headers**: Include X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
5. **Handle Throttling**: Return 429 with Retry-After header
6. **Test**: Verify limits work correctly under load

## Do's and Don'ts
- ✅ **Do** use Redis for distributed rate limiting across multiple instances
- ✅ **Do** include clear rate limit headers for client transparency
- ✅ **Do** implement differentiated limits (stricter for writes, looser for reads)
- ❌ **Don't** block legitimate users with overly aggressive limits
- ❌ **Don't** forget to handle edge cases (missing API keys)
- ❌ **Don't** rely solely on client-side rate limiting

## Anti-Patterns
- **Hard Limits Only**: No graduated limits or grace periods
- **Silent Failures**: Returning 200 OK with hidden restrictions
- **No Logging**: Not tracking who is hitting rate limits
- **Single Point**: Using in-memory storage in distributed systems
