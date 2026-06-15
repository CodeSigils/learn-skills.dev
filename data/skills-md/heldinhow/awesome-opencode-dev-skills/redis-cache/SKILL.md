---
name: redis-cache
description: "Implement Redis caching strategies to improve application performance and reduce database load."
---

# Redis Caching

## Overview
Redis provides in-memory caching to improve application performance and reduce database load. This skill should be invoked when implementing caching for frequently accessed data, session storage, or rate limiting.

## Core Principles
- **Cache Strategy**: Choose write-through, write-behind, or look-aside
- **TTL**: Set appropriate time-to-live for cached data
- **Invalidation**: Handle cache invalidation properly
- **Patterns**: Use Redis data structures effectively

## Preparation Checklist
- [ ] Set up Redis server
- [ ] Choose client library
- [ ] Plan cache strategy
- [ ] Define cache keys

## Step-by-Step Process
1. **Connect**: Set up Redis client
2. **Define Strategy**: Choose caching approach
3. **Implement**: Write get/set/delete operations
4. **TTL**: Set expiration times
5. **Invalidate**: Handle cache updates
6. **Monitor**: Track cache hit rates

## Do's and Don'ts
- ✅ **Do** use appropriate TTL values
- ✅ **Do** implement cache invalidation
- ✅ **Do** use meaningful cache keys
- ❌ **Don't** cache data needing strong consistency
- ❌ **Don't** set indefinite TTL
- ❌ **Don't** ignore cache misses

## Anti-Patterns
- **No Expiry**: Cached data that never expires
- **Inconsistency**: Caching data that changes frequently
- **Key Collisions**: Poor key naming
- **No Monitoring**: Not tracking cache performance
