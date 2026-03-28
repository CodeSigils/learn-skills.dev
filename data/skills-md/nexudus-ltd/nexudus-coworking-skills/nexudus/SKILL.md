---
name: nexudus
description: Manage Nexudus coworking spaces via the `nexudus` CLI — businesses, products, authentication, and configuration.
metadata:
  triggers:
    - nexudus
    - coworking
    - business management
    - product management
    - spaces
user-invocable: true
---

# Nexudus CLI Agent Skill

You can manage Nexudus coworking spaces through the `nexudus` CLI tool. This skill teaches you how to authenticate, query data, and perform CRUD operations against the Nexudus platform API.

## Agent Invariants

1. **Always use `--agent` flag** on every CLI call. This returns a structured JSON envelope optimised for machine consumption.
2. **Parse the JSON envelope** before acting on results. The envelope has this shape:
   ```json
   {
     "ok": true,
     "data": { ... },
     "summary": "Human-readable summary",
     "breadcrumbs": ["entity", "action"],
     "meta": { "total": 10, "page": 1, "pageSize": 25, "totalPages": 1 }
   }
   ```
3. **Check `ok` first.** If `ok` is `false`, read `summary` for the error message and stop.
4. **Never prompt the user for credentials interactively.** If `ok` is `false` with an auth error, tell the user to run `nexudus login` manually.
5. **Use `--yes` or `-y` on delete commands** to skip interactive confirmation prompts.
6. **Use `--json` when you need raw data for scripting.** Use `--agent` when you want the envelope with summary.
7. **List responses omit collection properties.** The API only returns list/array fields (e.g., `Tariffs`, `Teams`, `LinkedResources`) when fetching a **single entity by ID** (`get <id>`). List commands return a simplified projection without these fields. If you need to read or verify a collection property, always fetch the individual entity first.
8. **Use the current user's defaults for business, currency, country, and timezone.** Before creating or updating entities that require a business (location), currency, country, or timezone, run `nexudus whoami --agent` and use the defaults from the response:
   - `DefaultBusinessId` — use as `--business` when creating entities scoped to a location.
   - `DefaultCurrencyId` — use as `--currency-id` when a currency is needed.
   - `DefaultCurrencyCode` — for display/reference purposes.
   - `DefaultCountryId` — use as `--country-id` when a country is needed.
   - `DefaultSimpleTimeZoneId` — use as `--timezone-id` when a timezone is needed.

   Only ask the user to specify these values if they explicitly want to override the defaults.

## Bootstrapping

Run diagnostics first to verify the CLI is ready:

```shell
nexudus doctor --agent
```

This returns CLI version, .NET runtime, OS, credential status, config file location, API connectivity, and all available commands. Check `data.CredentialsStored` and `data.ApiStatus` before proceeding.

If credentials are missing, instruct the user:

> Run `nexudus login` to authenticate with your Nexudus account.

## CLI Introspection

Discover available commands and options at any time:

```shell
nexudus --help
nexudus businesses --help
nexudus products --help
nexudus config --help
```

Each command also supports `--help` for detailed option information:

```shell
nexudus businesses update --help
nexudus products create --help
```

## Command Reference

### Authentication

| Command          | Description                       |
| ---------------- | --------------------------------- |
| `nexudus login`  | Authenticate (interactive prompt) |
| `nexudus logout` | Clear stored credentials          |
| `nexudus whoami` | Show current authenticated user   |

### Configuration

| Command                            | Description         |
| ---------------------------------- | ------------------- |
| `nexudus config get <key>`         | Read a config value |
| `nexudus config set <key> <value>` | Set a config value  |

Config keys: `base-url`

### Businesses

Businesses support Search, Get, and Update (no Create or Delete via API).

| Command                                                    | Description               |
| ---------------------------------------------------------- | ------------------------- |
| `nexudus businesses list --agent`                          | List all businesses       |
| `nexudus businesses list --query "London" --agent`         | Search businesses by name |
| `nexudus businesses list --page 2 --size 10 --agent`       | Paginated list            |
| `nexudus businesses get <id> --agent`                      | Get single business       |
| `nexudus businesses update <id> --name "New Name" --agent` | Update business fields    |

#### Business update options

`--name`, `--short-intro`, `--about`, `--quote`, `--terms`, `--website`, `--web-contact`, `--privacy-url`, `--cookie-url`, `--address`, `--street-name`, `--street-number`, `--neighborhood`, `--city`, `--state`, `--postcode`, `--country-id`, `--longitude`, `--latitude`, `--phone`, `--fax`, `--email`, `--contact-phone`, `--contact-email`, `--currency-id`, `--timezone-id`, `--default-language`, `--venue-type`, `--tags`, `--floors`, `--floor-space`, `--floor-space-unit`, `--passport-published`, `--passport-name`, `--passport-tagline`, `--passport-description`, `--logo-url`, `--banner-url`, `--nexio-banner-url`, `--passport-banner-url`

### Products

Products support full CRUD plus entity commands.

| Command                                                                           | Description                    |
| --------------------------------------------------------------------------------- | ------------------------------ |
| `nexudus products list --agent`                                                   | List all products              |
| `nexudus products list --query "Pass" --agent`                                    | Search products by name        |
| `nexudus products list --business <id> --agent`                                   | Filter by business             |
| `nexudus products list --page 2 --size 10 --agent`                                | Paginated list                 |
| `nexudus products get <id> --agent`                                               | Get single product             |
| `nexudus products create --name "Day Pass" --price 25.00 --business <id> --agent` | Create product                 |
| `nexudus products update <id> --name "New Name" --price 30.00 --agent`            | Update product                 |
| `nexudus products delete <id> --yes --agent`                                      | Delete product (no prompt)     |
| `nexudus products commands --agent`                                               | List available entity commands |
| `nexudus products run-command <key> <ids> --agent`                                | Run entity command             |

#### Product create options

`--name` (required), `--business` (required), `--price` (required), `--description`, `--sku`, `--tags`, `--visible`, `--currency-id`, `--tax-rate-id`, `--display-order`, `--only-for-members`, `--only-for-contacts`, `--track-stock`, `--financial-account-id`

#### Product update options

`--name`, `--price`, `--description`, `--sku`, `--tags`, `--visible`, `--currency-id`, `--tax-rate-id`, `--display-order`, `--only-for-members`, `--only-for-contacts`, `--track-stock`, `--archived`, `--financial-account-id`

### Diagnostics

```shell
nexudus doctor --agent
```

### Global Flags

| Flag               | Description                           |
| ------------------ | ------------------------------------- |
| `--agent`          | JSON envelope with summary (use this) |
| `--json`           | Raw JSON envelope                     |
| `--md`             | Markdown output                       |
| `--base-url <url>` | Override API base URL                 |

## Output Envelope

All commands produce a JSON envelope when `--agent` or `--json` is used:

```json
{
  "ok": true,
  "data": [ ... ],
  "summary": "Found 3 businesses (page 1/1)",
  "breadcrumbs": ["businesses", "list"],
  "meta": {
    "total": 3,
    "page": 1,
    "pageSize": 25,
    "totalPages": 1
  }
}
```

- **`ok`**: `true` on success, `false` on failure.
- **`data`**: The response payload — an object for single-entity operations, an array for lists, or null on some failures.
- **`summary`**: Human-readable result description.
- **`breadcrumbs`**: Command path that produced the output (e.g., `["products", "create"]`).
- **`meta`**: Pagination metadata for list operations (present only on list commands).

### Error envelope

```json
{
  "ok": false,
  "data": null,
  "summary": "Not logged in. Run 'nexudus login' first.",
  "breadcrumbs": ["businesses", "list"]
}
```

## Decision Trees

### "Find and display a business"

1. `nexudus businesses list --agent` (or `--query "name"` if searching)
2. Parse `data` array, find the target business
3. `nexudus businesses get <id> --agent` for full details

### "Create a <entity>"

1. First find the business ID: `nexudus businesses list --agent`
2. `nexudus <entity> create --name "Day Pass" --price 25.00 --business <businessId> --agent`
3. Check `ok` is `true`, read `data.Id` for the new entity ID

### "Update a <entity> <property>"

1. `nexudus <entity> get <id> --agent` to verify the entity exists
2. `nexudus <entity> update <id> --<property> <value> --agent`
3. Verify the update by checking the returned `data`

### "Delete a <entity>"

1. `nexudus <entity> get <id> --agent` to confirm the entity exists
2. `nexudus <entity> delete <id> --yes --agent`
3. Check `ok` is `true`

### "List <entity> for a specific business"

1. `nexudus <entity> list --business <businessId> --agent`
2. For pagination: add `--page N --size M`

### "Run an entity command on <entity>"

1. `nexudus <entity> commands --agent` to discover available commands
2. `nexudus <entity> run-command <commandKey> <id1,id2> --agent`
3. Add parameters with `-p Name=Value` if the command requires them

### "Check CLI health"

1. `nexudus doctor --agent`
2. Verify `data.CredentialsStored` is `true`
3. Verify `data.ApiStatus` is `"OK"`

### "Add passes to a product"

ProductTimePasses link a TimePass to a Product so that customers purchasing the product automatically receive those passes.

1. Find the product: `nexudus products list --query "Dat Pass Bundle" --agent` → note the `Id`
2. Find (or create) the time pass: `nexudus timepasses list --query "Day Pass" --agent` → note the `Id`
3. Create the link:
   ```shell
   nexudus producttimepasses create \
     --product-id <productId> \
     --time-pass-id <timePassId> \
     --passes-included 10 \
     --expire-time-in-months 1 \
     --expire-time-in-weeks 0 \
     --expires-in 30 \
     --agent
   ```
4. Check `ok` is `true`, read `data.Id` for the new link ID

### "List passes included in a product"

1. `nexudus producttimepasses list --agent`
2. Filter results where `ProductId` matches the target product

### "Update passes included in a product"

1. `nexudus producttimepasses list --agent` → find the link by `ProductId` and `TimePassId`
2. `nexudus producttimepasses update <id> --passes-included 20 --agent`
3. Verify the update by checking the returned `data`

### "Remove a pass from a product"

1. `nexudus producttimepasses list --agent` → find the link by `ProductId` and `TimePassId`
2. `nexudus producttimepasses delete <id> --yes --agent`
3. Check `ok` is `true`

## Error Handling

| Error                                            | Meaning                  | Action                                        |
| ------------------------------------------------ | ------------------------ | --------------------------------------------- |
| `ok: false`, summary contains "Not logged in"    | No stored credentials    | Tell user to run `nexudus login`              |
| `ok: false`, summary contains "Unauthorized"     | Invalid credentials      | Tell user to run `nexudus login` again        |
| `ok: false`, summary contains "Forbidden"        | Insufficient permissions | Inform user they lack API permissions         |
| `ok: false`, summary contains "not found"        | Entity doesn't exist     | Check the ID and try again                    |
| `ok: false`, summary contains "Failed to create" | Create validation error  | Check required fields (name, business, price) |
| Non-zero exit code                               | Command failed           | Read stderr or the JSON envelope for details  |

## Entity Models

### Business (key fields)

`Id`, `Name`, `Address`, `TownCity`, `State`, `PostalCode`, `CountryName`, `Phone`, `EmailContact`, `WebAddress`, `CurrencyCode`, `Tags`, `PassportPublished`, `VenueType`

### Products

Products support Search, Get, Create, Update, Delete.
Products also support entity commands.

| Command                                                                                                   | Description                    |
| --------------------------------------------------------------------------------------------------------- | ------------------------------ |
| `nexudus products list --agent`                                                                           | List all products              |
| `nexudus products list --query "search" --agent`                                                          | Search products by name        |
| `nexudus products list --page 2 --size 10 --agent`                                                        | Paginated list                 |
| `nexudus products get <id> --agent`                                                                       | Get single product             |
| `nexudus products create --business <value> --name <value> --price <value> --description <value> --agent` | Create product                 |
| `nexudus products update <id> --name "New Name" --agent`                                                  | Update product                 |
| `nexudus products delete <id> --yes --agent`                                                              | Delete product (no prompt)     |
| `nexudus products commands --agent`                                                                       | List available entity commands |
| `nexudus products run-command <key> <ids> --agent`                                                        | Run entity command             |

#### Product create options

`--business` (required), `--name` (required), `--price` (required), `--description` (required), `--sku`, `--tags`, `--visible`, `--currency-id`, `--tax-rate-id`, `--display-order`, `--only-for-members`, `--only-for-contacts`, `--track-stock`, `--archived`, `--financial-account-id`

#### Product update options

`--name`, `--price`, `--description`, `--sku`, `--tags`, `--visible`, `--currency-id`, `--tax-rate-id`, `--display-order`, `--only-for-members`, `--only-for-contacts`, `--track-stock`, `--archived`, `--financial-account-id`

### Product (key fields)

`Id`, `BusinessId`, `BusinessName`, `Name`, `Price`, `Description`, `Sku`, `Tags`, `Visible`, `CurrencyCode`, `DisplayOrder`, `OnlyForMembers`, `OnlyForContacts`, `TrackStock`, `CurrentStock`, `Archived`

### TimePasses

Passes allow customers to check in to a coworking space. There are two kinds:

- **Day Pass** — valid for a single calendar day. Created with `--minutes-included` omitted (null). The customer can check in any number of times during that day.
- **Time Pass** — valid across multiple days up to a fixed amount of time. Created with `--minutes-included <minutes>` set. The customer can check in until the included minutes are exhausted.

TimePasses support Search, Get, Create, Update, Delete.

| Command                                                               | Description                 |
| --------------------------------------------------------------------- | --------------------------- |
| `nexudus timepasses list --agent`                                     | List all timepasses         |
| `nexudus timepasses list --query "search" --agent`                    | Search timepasses by name   |
| `nexudus timepasses list --page 2 --size 10 --agent`                  | Paginated list              |
| `nexudus timepasses get <id> --agent`                                 | Get single timepass         |
| `nexudus timepasses create --business <value> --name <value> --agent` | Create timepass             |
| `nexudus timepasses update <id> --name "New Name" --agent`            | Update timepass             |
| `nexudus timepasses delete <id> --yes --agent`                        | Delete timepass (no prompt) |

#### TimePass create options

`--business` (required), `--name` (required), `--invoice-display`, `--price`, `--minutes-included`, `--counts-towards-plan`, `--payg-members`, `--payg-contacts`, `--use-priority`, `--currency-id`, `--tax-rate-id`, `--reduced-tax-rate-id`, `--exempt-tax-rate-id`, `--financial-account-id`, `--kisi-group-id`, `--door-guard-group-id`, `--allow-network-checkin`, `--only-for-contacts`, `--only-for-members`, `--archived`

#### TimePass update options

`--name`, `--invoice-display`, `--price`, `--minutes-included`, `--counts-towards-plan`, `--payg-members`, `--payg-contacts`, `--use-priority`, `--currency-id`, `--tax-rate-id`, `--reduced-tax-rate-id`, `--exempt-tax-rate-id`, `--financial-account-id`, `--kisi-group-id`, `--door-guard-group-id`, `--allow-network-checkin`, `--only-for-contacts`, `--only-for-members`, `--archived`

### TimePass (key fields)

`Id`, `BusinessId`, `BusinessName`, `Name`, `Price`, `MinutesIncluded`, `CurrencyCode`, `OnlyForContacts`, `OnlyForMembers`, `Archived`

### ProductTimePasses

ProductTimePasses support Search, Get, Create, Update, Delete.

| Command                                                                                                                                                                                              | Description                        |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `nexudus producttimepasses list --agent`                                                                                                                                                             | List all producttimepasses         |
| `nexudus producttimepasses list --query "search" --agent`                                                                                                                                            | Search producttimepasses by name   |
| `nexudus producttimepasses list --page 2 --size 10 --agent`                                                                                                                                          | Paginated list                     |
| `nexudus producttimepasses get <id> --agent`                                                                                                                                                         | Get single producttimepass         |
| `nexudus producttimepasses create --product-id <value> --time-pass-id <value> --passes-included <value> --expire-time-in-months <value> --expire-time-in-weeks <value> --expires-in <value> --agent` | Create producttimepass             |
| `nexudus producttimepasses update <id> --name "New Name" --agent`                                                                                                                                    | Update producttimepass             |
| `nexudus producttimepasses delete <id> --yes --agent`                                                                                                                                                | Delete producttimepass (no prompt) |

#### ProductTimePass create options

`--product-id` (required), `--time-pass-id` (required), `--passes-included` (required), `--expire-time-in-months` (required), `--expire-time-in-weeks` (required), `--expiration-type`, `--expires-in` (required)

#### ProductTimePass update options

`--passes-included`, `--expire-time-in-months`, `--expire-time-in-weeks`, `--expiration-type`, `--expires-in`

### ProductTimePass (key fields)

`Id`, `ProductId`, `ProductName`, `TimePassId`, `TimePassName`, `PassesIncluded`

### Resources

Resources support Search, Get, Create, Update, Delete.

| Command                                                                                         | Description                 |
| ----------------------------------------------------------------------------------------------- | --------------------------- |
| `nexudus resources list --agent`                                                                | List all resources          |
| `nexudus resources list --query "search" --agent`                                               | Search resources by name    |
| `nexudus resources list --page 2 --size 10 --agent`                                             | Paginated list              |
| `nexudus resources get <id> --agent`                                                            | Get single resource         |
| `nexudus resources create --business <value> --name <value> --resource-type-id <value> --agent` | Create resource             |
| `nexudus resources update <id> --name "New Name" --agent`                                       | Update resource             |
| `nexudus resources delete <id> --yes --agent`                                                   | Delete resource (no prompt) |

#### Resource create options

`--business` (required), `--name` (required), `--system-resource-type`, `--resource-type-id` (required), `--description`, `--email-confirmation-content`, `--visible`, `--requires-confirmation`, `--display-order`, `--group-name`, `--projector`, `--internet`, `--conference-phone`, `--standard-phone`, `--white-board`, `--large-display`, `--catering`, `--tea-and-coffee`, `--drinks`, `--security-lock`, `--cctv`, `--voice-recorder`, `--air-conditioning`, `--heating`, `--natural-light`, `--standing-desk`, `--quiet-zone`, `--wireless-charger`, `--privacy-screen`, `--soundproof`, `--video-conferencing`, `--dual-display-screen`, `--display-screen`, `--wireless-presentation`, `--pa-system`, `--desktop-monitor`, `--flip-chart`, `--secure-storage`, `--allow-multiple-bookings`, `--allocation`, `--limit-visitors-to-allocation`, `--book-in-advance-limit`, `--late-booking-limit`, `--late-cancellation-limit`, `--interval-limit`, `--no-return-policy`, `--no-return-policy-all-resources`, `--no-return-policy-all-users`, `--max-booking-length`, `--min-booking-length`, `--tariffs` (list, repeat flag), `--added-tariffs` (list, repeat flag), `--removed-tariffs` (list, repeat flag), `--teams` (list, repeat flag), `--added-teams` (list, repeat flag), `--removed-teams` (list, repeat flag), `--shifts`, `--linked-resources` (list, repeat flag), `--added-linked-resources` (list, repeat flag), `--removed-linked-resources` (list, repeat flag), `--longitude`, `--latitude`, `--hide-in-calendar`, `--archived`, `--use-shared-zoom-account`, `--zoom-user-id`, `--last-cleaned-at`, `--linked-resource-ids`, `--only-for-contacts`, `--only-for-members`, `--only-for-invoicing-business`, `--booking-availability-exceptions` (list, repeat flag), `--added-booking-availability-exceptions` (list, repeat flag), `--removed-booking-availability-exceptions` (list, repeat flag), `--cancellation-fee-product-id`, `--charge-cancellation-fee`, `--cancellation-fee-type`, `--cancellation-fee-amount`, `--cancellation-fee-percentage`, `--repeat-booking-quantity-limit`, `--repeat-booking-period-limit-in-months`, `--new-picture-url`, `--picture-file-name`, `--clear-picture-file`

#### Resource update options

`--name`, `--system-resource-type`, `--resource-type-id`, `--description`, `--email-confirmation-content`, `--visible`, `--requires-confirmation`, `--display-order`, `--group-name`, `--projector`, `--internet`, `--conference-phone`, `--standard-phone`, `--white-board`, `--large-display`, `--catering`, `--tea-and-coffee`, `--drinks`, `--security-lock`, `--cctv`, `--voice-recorder`, `--air-conditioning`, `--heating`, `--natural-light`, `--standing-desk`, `--quiet-zone`, `--wireless-charger`, `--privacy-screen`, `--soundproof`, `--video-conferencing`, `--dual-display-screen`, `--display-screen`, `--wireless-presentation`, `--pa-system`, `--desktop-monitor`, `--flip-chart`, `--secure-storage`, `--allow-multiple-bookings`, `--allocation`, `--limit-visitors-to-allocation`, `--book-in-advance-limit`, `--late-booking-limit`, `--late-cancellation-limit`, `--interval-limit`, `--no-return-policy`, `--no-return-policy-all-resources`, `--no-return-policy-all-users`, `--max-booking-length`, `--min-booking-length`, `--tariffs` (list, repeat flag), `--added-tariffs` (list, repeat flag), `--removed-tariffs` (list, repeat flag), `--teams` (list, repeat flag), `--added-teams` (list, repeat flag), `--removed-teams` (list, repeat flag), `--shifts`, `--linked-resources` (list, repeat flag), `--added-linked-resources` (list, repeat flag), `--removed-linked-resources` (list, repeat flag), `--longitude`, `--latitude`, `--hide-in-calendar`, `--archived`, `--use-shared-zoom-account`, `--zoom-user-id`, `--last-cleaned-at`, `--linked-resource-ids`, `--only-for-contacts`, `--only-for-members`, `--only-for-invoicing-business`, `--booking-availability-exceptions` (list, repeat flag), `--added-booking-availability-exceptions` (list, repeat flag), `--removed-booking-availability-exceptions` (list, repeat flag), `--cancellation-fee-product-id`, `--charge-cancellation-fee`, `--cancellation-fee-type`, `--cancellation-fee-amount`, `--cancellation-fee-percentage`, `--repeat-booking-quantity-limit`, `--repeat-booking-period-limit-in-months`, `--new-picture-url`, `--picture-file-name`, `--clear-picture-file`

### Resource (key fields)

`Id`, `BusinessId`, `BusinessName`, `Name`, `ResourceTypeId`, `ResourceTypeName`, `Visible`, `GroupName`, `Allocation`, `Archived`, `OnlyForContacts`, `OnlyForMembers`

**List properties (only returned by `get`, not by `list`):** `Tariffs`, `AddedTariffs`, `RemovedTariffs`, `Teams`, `AddedTeams`, `RemovedTeams`, `LinkedResources`, `AddedLinkedResources`, `RemovedLinkedResources`, `BookingAvailabilityExceptions`, `AddedBookingAvailabilityExceptions`, `RemovedBookingAvailabilityExceptions`

> **Resource Type (`ExtraService`):** Every resource requires a `ResourceTypeId` that references an `ExtraService` entity. The resource type defines the hourly/daily rates and billing rules for bookings. You cannot create a resource without first knowing the ID of an existing resource type.

### ResourceTypes

ResourceTypes support Search, Get, Create, Update, Delete.

| Command                                                       | Description                     |
| ------------------------------------------------------------- | ------------------------------- |
| `nexudus resourcetypes list --agent`                          | List all resourcetypes          |
| `nexudus resourcetypes list --query "search" --agent`         | Search resourcetypes by name    |
| `nexudus resourcetypes list --page 2 --size 10 --agent`       | Paginated list                  |
| `nexudus resourcetypes get <id> --agent`                      | Get single resourcetype         |
| `nexudus resourcetypes create --business <value> --agent`     | Create resourcetype             |
| `nexudus resourcetypes update <id> --name "New Name" --agent` | Update resourcetype             |
| `nexudus resourcetypes delete <id> --yes --agent`             | Delete resourcetype (no prompt) |

#### ResourceType create options

`--business` (required), `--name`

#### ResourceType update options

`--name`

### ResourceType (key fields)

`Id`, `BusinessId`, `BusinessName`, `Name`

### Currencies

Currencies support Search, Get (no Create or Delete via API).

| Command | Description |
| --- | --- |
| `nexudus currencies list --agent` | List all currencies |
| `nexudus currencies list --query "search" --agent` | Search currencies by name |
| `nexudus currencies list --page 2 --size 10 --agent` | Paginated list |
| `nexudus currencies get <id> --agent` | Get single currency |

### Countries

Countries support Search, Get (no Create or Delete via API).

| Command | Description |
| --- | --- |
| `nexudus countries list --agent` | List all countries |
| `nexudus countries list --query "search" --agent` | Search countries by name |
| `nexudus countries list --page 2 --size 10 --agent` | Paginated list |
| `nexudus countries get <id> --agent` | Get single country |

### Country (key fields)

`Id`, `Name`, `TwoDigitsCode`, `Culture`

### Currency (key fields)

`Id`, `Name`, `Code`, `Format`

## Image Uploads

Some entities have image properties (logo, banner, picture, etc.). To set an image, use the corresponding `New{PropertyName}Url` property, which accepts a **publicly accessible URL**. The Nexudus back-end downloads the image from that URL and stores it, so the URL must be reachable from the internet — local file paths or authenticated URLs will not work.

The naming convention is: for an image property called `{PropertyName}`, the upload property is `New{PropertyName}Url`.

| Entity   | Image Property   | CLI Option              | API Property             |
| -------- | ---------------- | ----------------------- | ------------------------ |
| Business | Logo             | `--logo-url`            | `NewLogoUrl`             |
| Business | BannerImage      | `--banner-url`          | `NewBannerImageUrl`      |
| Business | NexIoBannerImage | `--nexio-banner-url`    | `NewNexIoBannerImageUrl` |
| Business | PassportBanner   | `--passport-banner-url` | `NewPassportBannerUrl`   |
| Resource | Picture          | `--new-picture-url`     | `NewPictureUrl`          |

Example — set a logo on a business:

```shell
nexudus businesses update <id> --logo-url "https://example.com/logo.png" --agent
```

Example — set a picture on a resource:

```shell
nexudus resources update <id> --new-picture-url "https://example.com/room.jpg" --agent
```

## Nexudus API Pattern

The Nexudus API follows a consistent REST pattern. Each entity at `/api/{module}/{entities}` supports:

| Operation   | HTTP   | URL                                       |
| ----------- | ------ | ----------------------------------------- |
| Search      | GET    | `/api/{module}/{entities}?page=1&size=25` |
| Get one     | GET    | `/api/{module}/{entities}/{id}`           |
| Create      | POST   | `/api/{module}/{entities}`                |
| Update      | PUT    | `/api/{module}/{entities}`                |
| Delete      | DELETE | `/api/{module}/{entities}/{id}`           |
| Commands    | GET    | `/api/{module}/{entities}/commands`       |
| Run command | POST   | `/api/{module}/{entities}/runCommand`     |

Current entity mappings:

| Entity          | Module  | Path              |
| --------------- | ------- | ----------------- |
| Business        | sys     | businesses        |
| Product         | billing | products          |
| TimePass        | billing | timepasses        |
| ProductTimePass | billing | producttimepasses |
| Resource        | spaces  | resources         |
| ResourceType    | spaces  | resourcetypes     |
| Currency        | sys     | currencies        |
| Country         | sys     | countries         |

## Passing Multiple Values (List Options)

Some options accept a list of IDs (e.g., `--tariffs`, `--teams`, `--linked-resources`). To pass multiple values, **repeat the flag** for each value:

```shell
nexudus resources update <id> --tariffs 101 --tariffs 202 --tariffs 303 --agent
```

Do **not** use comma-separated values or bracket syntax — each value needs its own flag.

## Tips

- Use `--size 100` to fetch larger pages when you need to scan many records.
- Combine `--query` with pagination for efficient searching.
- The `run-command` accepts comma-separated IDs to batch operations: `nexudus products run-command archive 123,456,789 --agent`.
- Business entities cannot be created or deleted via the API — only listed, viewed, and updated.
- Always pass `--yes` with delete commands whegin running non-interactively.
