# Impressum Scraper API

Extract company and contact details from German websites with the
[Datablist](https://www.datablist.com/) Impressum Scraper API.

Send a website URL. The API finds its Impressum or legal notice page and extracts
available business details: company name, managing director's name, postal
address, email, phone number, VAT number, and registration number. Each result
also includes the Impressum URL and a confidence score when available.

Use the results to enrich company records, research German businesses, or add
business contact details to your own application.

## Get started

Choose [Python](python/README.md) or [TypeScript](typescript/README.md).
The commands below use Python.

1. [Create a Personal API Key](https://app.datablist.com/account/api).
2. Run these commands from this repository's root:

```sh
cd python
python -m pip install -r requirements.txt
export DATABLIST_API_KEY='your-personal-api-key'
python sync_requests.py
```

Edit the `websites` list at the bottom of the script to use your own URLs.
See the [Python guide](python/README.md) for setup and the async version.

Each website uses account credits. See the current
[credit cost and limits](https://platform.datablist.com/docs/enrichments/tools/impressum-scraper#credits-and-limits)
and [pricing](https://www.datablist.com/pricing). Each result reports its actual
`creditsUsed`.

## Input and output

Send website URLs to `POST https://api.datablist.com/v1/enrichments/tasks`, with
your key in the `X-API-Key` header:

```json
{
  "enrichmentId": "impressum-scraper",
  "uniqueId": "impressum-example-001",
  "settings": {},
  "inputs": [
    {"inputId": "row-1", "data": {"websiteUrl": "https://www.trigema.de"}},
    {"inputId": "row-2", "data": {"websiteUrl": "https://www.hetzner.com"}},
    {"inputId": "row-3", "data": {"websiteUrl": "https://www.sipgate.de"}},
    {"inputId": "row-4", "data": {"websiteUrl": "https://www.manomama.de"}},
    {"inputId": "row-5", "data": {"websiteUrl": "https://www.vaude.com"}}
  ]
}
```

No settings are needed. Use a new `uniqueId` for each new task. Give each URL its
own `inputId` so you can match it to its result.

The API returns `202 Accepted` with a task ID in `@id`. Check the task status,
then retrieve the results.

### Results from five German websites

The examples use Trigema, Hetzner, sipgate, manomama, and VAUDE. See the
[complete results](python/examples/results.json). Names are kept as returned;
email addresses are partially masked with `**` in the saved examples. The API
returns the full email addresses. Here is the first result:

```json
{
  "taskId": "144ab27534854e1a8089ec0450b53bd5",
  "results": [
    {
      "inputId": "row-1",
      "status": "success",
      "outputs": {
        "emailAddress": "b**@trigema.de",
        "postalAddress": "Josef-Mayer-Str. 31-35, D-72393 Burladingen",
        "agentConfidenceScore": 85,
        "phoneNumber": "+49 (0) 7475/88 - 0",
        "registrationNumber": "HRA 740365",
        "firstName": "Wolfgang",
        "companyName": "Trigema W. Grupp KG",
        "impressumUrl": "https://www.trigema.de/kundenservice/rechtliches/impressum/",
        "vatNumber": "DE144846566",
        "lastName": "Grupp",
        "gender": "male"
      },
      "creditsUsed": "10",
      "error": null
    }
  ],
  "nextCursor": null
}
```

## Try with cURL

Set your key, then submit a website:

```sh
export DATABLIST_API_KEY='your-personal-api-key'

curl --request POST 'https://api.datablist.com/v1/enrichments/tasks' \
  --header "X-API-Key: $DATABLIST_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "enrichmentId": "impressum-scraper",
    "uniqueId": "impressum-curl-001",
    "settings": {},
    "inputs": [
      {"inputId": "row-1", "data": {"websiteUrl": "https://www.trigema.de"}}
    ]
  }'
```

Copy the returned `@id` into `TASK_ID`. Use a new `uniqueId` for a new task.

```sh
TASK_ID='paste-returned-task-id'

curl "https://api.datablist.com/v1/enrichments/tasks/$TASK_ID" \
  --header "X-API-Key: $DATABLIST_API_KEY"
```

Repeat the status command every few seconds until `status` is `completed`,
`failed`, or `stopped`. Then retrieve the results:

```sh
curl "https://api.datablist.com/v1/enrichments/tasks/$TASK_ID/results" \
  --header "X-API-Key: $DATABLIST_API_KEY"
```

If `nextCursor` is not `null`, pass it as `cursor` to fetch the next page.
The Python and TypeScript examples read every page for you.

## Python examples

| Example | What it shows |
| --- | --- |
| [Synchronous Requests](python/sync_requests.py) | Scrape Impressum details with blocking HTTP calls. |
| [Asynchronous HTTPX](python/async_httpx.py) | Use `async` and `await` for the same API workflow. |

Each file is self-contained: submit URLs, wait for the background task, and read
the results. Both clients use the API's background tasks; the difference is how
Python waits for HTTP calls.

## TypeScript example

Use [the standalone TypeScript example](typescript/example.ts) with Node.js 24.3+;
no packages to install. From the repository root:

```sh
export DATABLIST_API_KEY='your-personal-api-key'
node typescript/example.ts
```

Or run with `tsx`, without installing it globally:

```sh
npx tsx typescript/example.ts
```

See the [TypeScript guide](typescript/README.md) for editable inputs and settings.

## Documentation

- [Impressum Scraper API](https://platform.datablist.com/docs/enrichments/tools/impressum-scraper)
- [Enrichments API quickstart](https://platform.datablist.com/docs/enrichments/quickstart)
- [Task lifecycle](https://platform.datablist.com/docs/enrichments/tasks)

## Other Datablist API examples

- [Company Name to Domain API](https://github.com/datablist/company-name-to-domain-api): find company websites from names.
- [Company Name Cleaner API](https://github.com/datablist/company-name-cleaner-api): clean and standardize company names.
- [LinkedIn Profile Finder API](https://github.com/datablist/linkedin-profile-finder-api): find profiles from names and company keywords.
