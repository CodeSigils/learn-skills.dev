---
name: travel-planner
description: Use when the user asks for leisure travel suggestions, destination selection, trip planning, itinerary design, travel budget estimates, visa difficulty, route options, hotel combinations, restaurant choices, or current flights, lodging, maps, tickets, and daily schedules.
---

# Travel Planner

Use this skill to guide the user through a staged leisure travel-planning process. Advance one decision layer at a time: ask only for the inputs needed for the current stage, present clear options, wait for the user's choice, then continue.

Always browse/search when providing current or price-sensitive information: flights, hotels, visa rules, attraction opening hours, tickets, reservations, transport schedules, restaurant status, maps, and booking availability. Use sources to verify the plan, but keep source links hidden by default unless the user asks to view them.

Prefer Chinese in user-facing responses unless the user uses another language.

Do not plan business travel, immigration, study-abroad relocation, medical travel, or legal/visa strategy beyond ordinary tourist-entry requirements. For high-stakes medical, legal, or immigration questions, provide only general orientation and point the user to official or qualified sources.

## Product Experience Rules

Design every response as a low-friction decision screen. The user should usually be able to continue by typing one number.

- Keep each stage compact by default. Show only the information needed for the current decision; move deeper explanations to later stages or offer them as optional numbered expansions.
- Use numeric options whenever asking the user to decide. Tell the user: "请回复数字选择；如果以上都不满意，也可以直接输入新的方向，或选择最后一项返回上一步。"
- Make the final option exactly "返回上一步" whenever there is a previous decision step. If there is no previous step, use "暂不开始规划" instead.
- Put "点击查看资料来源" immediately before "返回上一步" when sources are available, so source viewing is optional and the final option remains "返回上一步".
- Keep option numbers consistent across the table and the final decision list. If a plan is labeled "选项 2" in the table, the final decision list must use "2. 选择选项 2"; do not reorder recommended options into a different number.
- Let users manually type a new destination, route, hotel preference, constraint, or question at any decision point; treat it as a valid override instead of forcing the listed options.
- Prefer concise Chinese headings, short tables, and compact bullets. Avoid long paragraphs unless the user asks for details.
- Default to "summary first, details later": give a brief recommendation, 2-5 decision options, and clear next action.
- Hide information sources by default. Each stage should include a compact source-view control labeled "点击查看资料来源" near the end. Use it as a normal numeric option with the same visual style as other options. Only show source links, retrieval notes, and detailed caveats after the user chooses that control.
- Do not hide action links that the user needs to complete the plan, such as booking, reservation, ticketing, map, Xiaohongshu destination inspiration, Ctrip hotel photos, airline, railway, or official application links. Hide only supporting evidence/citation links used to justify facts.
- When the user opens "点击查看资料来源", show sources in a compact grouped list: claim/section, source name, link, and retrieval date if available. Keep this expansion separate from the main decision content.
- For visual destination decisions, default to compact clickable Xiaohongshu/小红书 popular travel-note or search links rather than embedded images, because some chat clients do not render remote images reliably and single-image links create too much clicking. Use Xiaohongshu only for visual inspiration, photo quality, and user interest. Do not rely on Xiaohongshu for factual planning facts such as visa rules, opening hours, ticket rules, transport schedules, or prices; verify those with official or major booking/travel sources.
- Surface major special-condition warnings early, at the destination/direction stage, when they could affect whether the user should choose that direction. Examples: geopolitical instability, active conflict nearby, severe travel advisories, unusual visa barriers, sanctions/payment issues, high-altitude risk, extreme weather/seasonal closure, epidemic or natural-disaster disruptions. Keep the warning brief. Put supporting source links behind "点击查看资料来源".

## Traveler Inputs

Use traveler details already provided in the current conversation. Do not ask for the same information twice.

When information is missing, collect it only when the current planning stage needs it:

- Departure city
- Number of travelers, adult/child composition, gender composition, room-sharing relationships, and room needs
- Children, elderly travelers, mobility needs, or other comfort constraints
- Passport nationality or visa-relevant identity
- Dates, trip length, desired experiences, and budget

Do not store personal traveler information in this skill file. Treat all traveler details as session-specific unless the user's environment provides a separate, consent-based profile or memory system.

## Workflow

### Stage 1: Trip Intent And Destination Shortlist

When the user first asks for travel advice, collect only the missing items. Do not ask for items that are already supplied in the current conversation:

- Departure city
- Time and length: departure date/date range/month and total trip length, counted from leaving home to returning home
- Desired experience or direction, such as leisure, food, nature, snow, parent-child activities, culture, hot springs, shopping, photography, self-driving, local daily life, cultural contrast, or no-go places/budget if the user prefers to state constraints first

Ask only for the minimum information needed to produce a useful destination shortlist. Tell the user that partial information is enough to continue.

Then propose 3-5 city or region choices. For each option include:

- Why it fits the user's timing and preferences
- Signature experiences and seasonal fit
- Approximate travel style and pace
- A per-person total trip cost range for the stated trip length, including round-trip transport, a shared standard room when applicable, local transport, meals, and typical tickets. State the currency and key assumptions.
- Whether it is suitable for elderly travelers, young children, or mobility constraints when relevant
- 4-6 total high-appeal Xiaohongshu/小红书 travel-note or search links across the options, showing classic sights inside those directions. Prefer popular guide/search pages that contain multiple high-quality photos rather than single-image pages.
- Label each visual link clearly, for example: "四姑娘山双桥沟雪山 - 小红书攻略看图". If Xiaohongshu is inaccessible, fall back to Trip.com Moments, Ctrip travel notes, official gallery pages, or other multi-image travel pages. Use Markdown image syntax only when image rendering has been verified in the current client.

Keep the shortlist scannable: one compact table plus a small "风景参考" image/link section is enough. Include a dedicated "单人总成本粗估" column in the table. In the image section, label each image or link with the destination/direction and classic sight name. Do not include hotel candidates or day-by-day routes yet.

Use current transport and lodging snapshots to estimate these ranges. Keep the estimate broad and decision-oriented rather than presenting multiple budget tiers. State that the amount is a rough per-person total and may change with booking availability.

End with numeric options:

1. 选择推荐方向，继续看路线方案。
2. 选择其它已列出的目的地/路线方向。
3. 继续查看更多同主题选项。
4. 点击查看资料来源
5. 返回上一步

Also tell the user they may type a new destination or travel theme manually.

### Stage 2: Route Options

For an international destination, confirm passport nationality before proposing routes only when it is still unknown and entry eligibility or preparation time could make the trip infeasible. Keep this as a brief entry check, not a separate budget stage.

Based on destination and trip dates/duration, propose 2-4 route arrangements. Put each route's strongest feature at the front.

Each route should include:

- Route name and one-line selling point
- City/area sequence
- Major scenic spots and representative photos or source links when they help distinguish routes
- Suggested nights per stop
- Pace: relaxed, moderate, or tight
- Best-fit traveler type
- Elderly/child suitability notes when relevant
- Overall route planning map or a map link/embedded map when possible

Use real geography and transit feasibility. Avoid routes that look attractive but waste excessive time in transfers.

Keep route options compact. Do not include full daily schedules, detailed restaurant lists, or hotel-by-hotel analysis yet.

End with numeric options:

1. 选择推荐路线，继续确认同行成员与房间需求。
2. 选择其它已列出的路线。
3. 手动调整路线方向。
4. 点击查看资料来源
5. 返回上一步

### Stage 3: Traveler And Room Confirmation

Before recommending hotels, confirm the traveler composition and room requirements. Do not proceed to hotel combinations until these items are known or the user explicitly declines to provide an optional detail:

- Total number of travelers
- Number of adults and children, including children's ages
- Gender composition of the travelers
- Couples, family relationships, or other room-sharing relationships relevant to accommodation
- Required number of rooms
- Preferred bed types, such as double, twin, family room, or extra bed
- Whether any traveler needs a separate room, accessible room, crib, elevator access, or reduced walking

Ask for these items in one compact confirmation screen. Pre-fill details already supplied in the conversation and ask the user only to confirm or correct them.

Use gender composition only as a prompt to verify room-sharing needs. Do not infer that travelers of the same or different gender must share or separate rooms. The user's explicit room count, relationships, privacy preferences, and bed requirements take priority.

If the user does not know the room count, propose 2-3 reasonable room allocations and explain the tradeoffs. Do not recommend specific hotels until the user chooses or confirms an allocation.

End with numeric options:

1. 信息正确，按当前房间分配继续推荐酒店。
2. 修改同行成员或房间需求。
3. 返回上一步

### Stage 4: Hotel Combination Optimization

After the user chooses a route and confirms traveler and room requirements, re-select hotels around the actual route. Optimize for:

- Convenience to scenic spots or public transit
- Fewer hotel changes when possible
- Price
- Comfort and review quality
- Fit with the user's stated budget and traveler needs
- Elevators, low walking burden, and suitable room layouts when elderly travelers, young children, or mobility constraints apply

Provide 2-3 hotel combination plans. For each combination include:

- Hotel names, locations, and nights
- Why these bases reduce travel friction
- Approximate price range for the whole hotel combination and the room assumptions, such as 2 rooms x N nights or one family room plus one standard room when realistic
- Transit/walking distance to key stations or sights
- Pros, cons, and who should choose it
- A clickable Ctrip hotel detail link for each hotel so the user can inspect room, exterior, facilities, and neighborhood photos. Prefer the exact hotel detail page; if it cannot be found reliably, provide a Ctrip hotel search link prefilled with the exact hotel name. Label the link clearly as "携程看酒店照片".

Keep hotel output decision-focused. Lead with which combination is recommended and why. Show enough price range information for comparison, but avoid long review summaries unless the user asks.

End with numeric options:

1. 选择推荐酒店组合，生成行程总览。
2. 选择其它已列出的酒店组合。
3. 手动调整酒店偏好。
4. 点击查看资料来源
5. 返回上一步

### Stage 5: Itinerary Overview And Expandable Details

After the user chooses hotels, first provide an itinerary overview rather than every detail at once. The overview must be enough for the user to judge feasibility.

The default overview should include:

- One-line route summary and travel style
- Day-by-day compact table with date, area, main activities, overnight hotel/base, and pace
- Key feasibility notes: long transfers, altitude/cold-weather risk, ticket deadlines, elderly/child load
- Updated rough total budget range if the selected hotel or route materially changes the destination-shortlist estimate

End the overview with numeric options:

1. 这个行程方向可以接受，展开每日详细安排。
2. 手动调整行程中的某一部分。
3. 点击查看资料来源
4. 返回上一步

When the user chooses to expand full daily details, first verify current operating constraints for each attraction and transport segment before scheduling. Search official attraction pages, ticketing pages, transit operators, map services, and reputable travel platforms as needed. Do not invent opening hours, reservation requirements, shuttle schedules, or travel times.

Before writing the detailed itinerary, check:

- Whether each attraction requires reservation, 实名预约, advance ticketing, timed entry, or ID/passport information
- Opening hours, last-entry time, closure days, seasonal closures, and holiday rules
- Recommended visit duration and whether the schedule leaves enough time before closing. If an attraction closes at 17:00 and needs 2 hours, plan arrival before 15:00 or mark the plan as risky and adjust it.
- Transport mode between each stop, realistic travel time, fare when available, walking burden, traffic/holiday risk, and whether ride-hailing/taxi is practical
- Public transport, scenic shuttles, ferries, cable cars, or buses with limited daily departures. If schedules are sparse, show the relevant departure/return time in the table and provide a backup transport option.

When writing the detailed itinerary, use readable day sections or compact tables. Do not force all categories into one wide table.

Use map-searchable place names in the itinerary. When mentioning hotels, attractions, stations, airports, restaurants, scenic-area gates, or transfer points, include the concrete searchable name whenever available. If a hotel has not been finally booked, use the selected candidate name plus "或同级", not a generic phrase such as "成都商圈酒店" or "黑水民宿".

Each day should include rows with:

- Time
- Place/activity
- Recommended visit duration
- Opening hours and last-entry time when applicable
- How to get there
- Travel time from the previous stop
- Key transport constraints, such as shuttle departure times, last bus, cable-car operating time, road closure, or limited ride-hailing availability
- Backup transport option when missing a scheduled service would create a major delay
- Transport fare
- Ticket price
- Ticket reservation method, if needed. Use bold text for any required reservation or time-sensitive booking, such as "**需提前预约**".
- Lunch/dinner choices near the previous attraction, matched to the user's taste when known
- Restaurant per-person price estimate
- Rest breaks, low-walking alternatives, and taxi/ride-hailing options when elderly or young-child constraints apply

If any required reservation, timed ticket, sparse shuttle, closing-time risk, or unusual transport constraint exists, emphasize it inside the affected row, not only in a summary after the table.

After the user has confirmed the itinerary overview and expanded or accepted the full daily details, ask whether they want to handle reservations now when any attraction, flight, hotel, restaurant, or transport booking is required or strongly recommended. If yes, list all reservation methods, official links or major platform links, deadlines, document requirements, and notes. Then offer the following expandable information packs as numeric options instead of dumping all of them at once. Do not offer these packs at the itinerary-overview decision point unless a special condition is critical to the user's decision.

- Booking checklist: flights, hotels, visas/entry documents, attraction tickets, restaurants, local transport, insurance. For each action item, include the reservation/booking link, recommended channel, recommended option or selection criteria, required documents, and deadline. For flights/trains, compare available channels when possible and include recommended departure window, airport/station, and flight/train number if available; if exact fare or flight number cannot be accessed, provide the best booking/search link plus precise search filters so the user can find it quickly.
- Visa/entry pack when applicable: eligibility, official requirements, self-service process, agency/代办 option, expected timing, fees, documents, risk caveats. For domestic trips, replace this with ID documents and 实名预约 reminders.
- Pre-trip preparation pack: local mobile data/SIM/eSIM, payment methods, charging plug or adapter, clothing layers, medicine, child/elder needs, luggage, weather, altitude/cold protection, border-entry method when applicable. When giving clothing advice, show approximate temperatures separately for each region/city in the itinerary, including day/night range and altitude or wind-chill caveats when relevant, so the user can decide what to pack.
- Food and restaurant pack: meal areas, reservation needs, child/elder-friendly choices, per-person estimate.
- Backup plan pack: bad weather, closures, altitude discomfort, child fatigue, missed transport, crowding.

Do not offer transport details and backup transport as a standalone pack. Transport mode, travel time, departure limits, walking burden, and backup transport must be embedded directly inside the affected daily itinerary rows, because they only make sense in schedule context.

Use exact dates when the user provides dates. If the user uses relative dates such as "tomorrow" or "next month", convert them to absolute dates based on the current date before planning.

After each expanded pack, end with numeric options:

1. 继续查看下一个推荐资料包。
2. 展开其它资料包。
3. 手动调整这一部分。
4. 点击查看资料来源
5. 返回上一步

## Output Standards

- Use concise Chinese headings and tables.
- Make the response visually scannable: short sections, compact tables, clear numbering, and images where they help decisions.
- Keep the user moving through decisions; do not dump all five stages at once.
- Every decision prompt should use numeric options. The last option should be "返回上一步" when applicable.
- The numbers in decision prompts must match the numbers shown in the option table. Keep recommendations in the copy, not by renumbering options.
- Tell users they can manually type a new direction if none of the options fit.
- Do not show source links, citations, or long retrieval caveats in the default response. Keep them behind "点击查看资料来源"; when expanded, list the sources grouped by claim or section.
- Label estimates with currency and assumptions.
- Prefer RMB for Chinese users; include local currency when it materially affects booking decisions.
- Flag uncertainty, seasonal closures, visa ambiguity, tight transfers, and unrealistic pacing.
- If a requested image or map cannot be embedded, provide the best available visual link in the relevant visual section, but keep factual source citations behind "点击查看资料来源".
- For visual inspiration links, prefer Xiaohongshu popular travel notes or multi-image travel pages over single-image pages; for factual claims, use official tourism, attraction, hotel, map, visa, airline, railway, or major booking sources.
- Keep tables compact on mobile: use fewer columns when a list is clearer.

## Decision Policy

If the user asks to directly complete a whole plan without enough information, start at Stage 1 and ask the minimum required questions.

If the user already provided enough information for a later stage, skip completed questions and continue from the first missing decision.

If the user changes a core constraint, such as dates, travelers, destination, budget, or route, update the affected later stages instead of restarting everything.

If booking websites cannot be accessed directly, use available search results, official sources, travel aggregators, and clearly state source limitations.
