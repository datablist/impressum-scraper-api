# Impressum Scraper API — Python examples

Extract business details from website Impressum pages. Each file shows all the
HTTP calls in one place, using five editable German website URLs.

## Setup

Use Python 3.12 or newer. From this `python` folder:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DATABLIST_API_KEY='your-personal-api-key'
```

Create your key on the [Datablist API page](https://app.datablist.com/account/api).
Calls consume account credits; see the current
[credit cost and limits](https://platform.datablist.com/docs/enrichments/tools/impressum-scraper#credits-and-limits)
and [pricing](https://www.datablist.com/pricing).

## Run an example

**Synchronous, using Requests:**

```sh
python sync_requests.py
```

**Asynchronous, using HTTPX:**

```sh
python async_httpx.py
```

Edit the `websites` list at the bottom of either file. Both scripts submit a
background task, poll every three seconds, and read all result pages. Requests
uses blocking calls; HTTPX uses `await` and `asyncio.sleep`.

Each prints the full result objects. The [saved results](examples/results.json)
from the five example websites keep names and partially mask emails with `**`.
When you run a script, it prints the full email addresses returned by the API.

## Inputs and results

The only input is `websiteUrl`. No public settings are needed, so the payload
uses an empty `settings` object. The API finds the website's Impressum page.

Each result contains your `inputId`, `status`, `outputs`, `creditsUsed`, and
`error`. Available output fields include:

- `firstName`, `lastName`, and `gender`: managing director or founder details.
- `companyName` and `postalAddress`: business identity and address.
- `emailAddress` and `phoneNumber`: business contact details.
- `vatNumber` and `registrationNumber`: company identifiers.
- `impressumUrl`: the page used to extract the details.
- `agentConfidenceScore`: a confidence score from 0 to 100, when available.

Fields can be empty when the page does not provide them. Each script submits
one task with up to 10,000 URLs, within the API's request size limits. These
examples do not batch larger lists.

## When something fails

HTTP errors raise the library's normal exception. A failed or stopped task
raises an exception with its task ID. A completed task can still have individual
errors or missing fields; check each result's `status`.

If you stop a script, the submitted task continues on the server. List your
[tasks](https://platform.datablist.com/docs/enrichments/tasks) to check its status
before creating another task.
