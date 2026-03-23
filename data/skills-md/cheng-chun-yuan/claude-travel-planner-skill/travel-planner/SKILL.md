---
name: travel-planner
description: Comprehensive travel planning assistant that creates complete travel guides with transportation, accommodation, itineraries, and practical information. Use when users want to plan trips, find flights/hotels, or create travel guides.
---

# Travel Planner

## Core Capabilities

- **Transportation** - Flights (via Kiwi.com MCP), trains, buses, ferries
- **Accommodation** - Hotels, hostels, Airbnb with area recommendations
- **Itineraries** - Day-by-day schedules with attractions and dining
- **Practical Info** - Visa, currency, language phrases, local tips
- **Budget Planning** - Cost breakdowns and money-saving tips

## MCP Setup

```bash
claude mcp add kiwi-com --transport http https://mcp.kiwi.com
```

**Tool**: `mcp__kiwi-com__search-flight` - Search flights with flexible dates, passengers, and cabin class.

## Workflow

1. **Gather Info** - Ask about destination, dates, budget, group size, travel style, and constraints
2. **Research** - Use MCP tools and web search to find current options
3. **Build Guide** - Generate complete travel guide using the template below

## Output Template

```markdown
# [Destination] Travel Guide
**Dates**: [Start] - [End] ([X] days)
**Travelers**: [Number and type]
**Budget Level**: [Budget/Mid-range/Luxury]

---

## 1. Getting There

### Flights
| Route | Airline | Departure | Arrival | Duration | Price | Book |
|-------|---------|-----------|---------|----------|-------|------|
| [Origin] -> [Dest] | [Airline] | [Time] | [Time] | [Xh Xm] | $XXX | [Link] |

### Alternative: Train/Bus
| Mode | Route | Operator | Duration | Price |
|------|-------|----------|----------|-------|

### Airport Transfer
| Method | Route | Duration | Cost |
|--------|-------|----------|------|
| MRT/Metro | [Line] | XX min | $X |
| Taxi | Direct | XX min | $XX |

---

## 2. Where to Stay

### Recommended Areas
| Area | Vibe | Best For | Transit Access |
|------|------|----------|----------------|

### Hotel Options
| Hotel | Area | Rating | Price/Night | Highlights |
|-------|------|--------|-------------|------------|
| [Budget] | | 3-star | $XX | |
| [Mid-range] | | 4-star | $XXX | |
| [Luxury] | | 5-star | $XXX+ | |

---

## 3. Getting Around

### Public Transit
| Mode | Coverage | Cost | Pass Options |
|------|----------|------|--------------|

### Taxi/Rideshare
- Apps: [Grab, Uber, local alternatives]
- Starting fare, per km rate

---

## 4. Day-by-Day Itinerary

### Day X: [Theme/Area]

#### Morning (09:00-12:00)
| Time | Activity | Location | Duration | Cost |
|------|----------|----------|----------|------|

**Transport**: [How to get there]

#### Lunch
**Restaurant**: [Name] - [Cuisine] - $XX/person

#### Afternoon (13:30-18:00)
| Time | Activity | Location | Duration | Cost |
|------|----------|----------|----------|------|

#### Dinner & Evening
[Restaurant and optional evening activities]

#### Day Summary
- Transport cost: $X
- Advance tickets needed: [List]

---

## 5. Practical Information

### Money
| Currency | Exchange Rate | ATMs | Tipping |
|----------|---------------|------|---------|

### Communication
| SIM/eSIM | WiFi | VPN Needed |
|----------|------|------------|

### Essential Phrases
| Phrase | Local | Pronunciation |
|--------|-------|---------------|
| Hello | | |
| Thank you | | |
| How much? | | |

### Emergency
| Police | Ambulance | Embassy |
|--------|-----------|---------|

---

## 6. Budget Summary

| Category | Daily | Total ([X] days) |
|----------|-------|------------------|
| Accommodation | $XX | $XXX |
| Food | $XX | $XXX |
| Transport | $XX | $XXX |
| Activities | $XX | $XXX |
| **Total** | **$XXX** | **$X,XXX** |

---

## 7. Booking Checklist

- [ ] Flights
- [ ] Hotel
- [ ] Attraction tickets
- [ ] Travel insurance
- [ ] Visa (if needed)

---

## 8. Quick Reference

**Hotel**: [Name], [Address], [Phone]
**Emergency**: [Numbers]
**Help Phrase**: [Local language]
```

## Interaction Guidelines

- Ask clarifying questions upfront to personalize the guide
- Present multiple options (budget/mid-range/luxury) when relevant
- Include step-by-step transport directions
- Mention booking deadlines and advance reservation needs
- Provide backup options for weather or closures
