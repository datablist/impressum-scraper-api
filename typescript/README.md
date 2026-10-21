# Impressum Scraper API — TypeScript example

Extract business details from Impressum pages with async/await and the standard `fetch` API.
All HTTP calls are in [one standalone file](example.ts).

## Setup and run

Use **Node.js 24.3 or newer**. No packages or build step are needed.
From the repository root:

```sh
export DATABLIST_API_KEY='your-personal-api-key'
node typescript/example.ts
```

Or run with `tsx`, without installing it globally:

```sh
npx tsx typescript/example.ts
```

From this `typescript` folder, use `node example.ts` or `npx tsx example.ts`.
Create your key on the [Datablist API page](https://app.datablist.com/account/api).
Calls can consume credits; see the current
[credit cost and limits](https://platform.datablist.com/docs/enrichments/tools/impressum-scraper#credits-and-limits)
and [pricing](https://www.datablist.com/pricing).

## Customize the example

Edit `websites` at the bottom of the file. The example uses Trigema, Hetzner,
sipgate, manomama, and VAUDE. No public settings are needed; the payload uses an
empty `settings` object.

## How it works

The API function uses `fetch`, `crypto.randomUUID()`, and `setTimeout`, with no
imports. The example at the bottom reads your API key from the environment.

The script submits one background task, polls every three seconds, and reads
result pages until `nextCursor` is `null`. Using `await` in Node.js still uses
the same background tasks as the Python examples.

Each input gets its own `inputId`, including repeated values. The script prints
complete JSON results, keeping statuses, outputs, credits used, and errors.
Outputs include available company and managing director names, address, email, phone number,
VAT number, registration number, Impressum URL, and confidence score.

The [saved Python results](../python/examples/results.json) keep names and mask
email addresses with `**`. Running this script prints the full API response.

Each run submits one task with up to 10,000 inputs, within the API's request
size limits. This example does not batch larger lists.

## When something fails

HTTP errors and network failures stop the script. A failed or stopped task
raises an error with its task ID. A completed task can still contain individual
errors or missing fields; check each result's `status`.

If you stop the script, the submitted task continues on the server. List your
[tasks](https://platform.datablist.com/docs/enrichments/tasks) to check its status
before creating another task.
