"""Extract business details from Impressum pages with Datablist using async HTTPX.

This standalone example submits five German websites, waits for the background
task to finish, and reads all pages of results.
HTTP calls use await, and polling pauses use asyncio.sleep.

Results can include company and managing director names, postal address, email,
phone number, VAT number, registration number, and the Impressum page URL.
No public settings are required; the payload uses an empty settings object.

Set DATABLIST_API_KEY and run: python async_httpx.py
Edit the websites list at the bottom to try your own URLs. This example submits
one task of up to 10,000 websites. Calls consume account credits.
"""

import asyncio
import os
import uuid

import httpx


async def scrape_impressums(websites: list[str], api_key: str) -> list[dict]:
    """Submit one task, wait for it to finish, and return its results."""
    tasks_url = "https://api.datablist.com/v1/enrichments/tasks"
    headers = {"X-API-Key": api_key}
    inputs = [
        {"inputId": f"row-{index}", "data": {"websiteUrl": website}}
        for index, website in enumerate(websites, start=1)
    ]

    async with httpx.AsyncClient() as client:
        # 1. Submit the website URLs.
        payload = {
            "enrichmentId": "impressum-scraper",
            "uniqueId": str(uuid.uuid4()),
            "settings": {},
            "inputs": inputs,
        }
        response = await client.post(tasks_url, headers=headers, json=payload)
        response.raise_for_status()
        task = response.json()
        task_id = task["@id"]
        task_url = f"{tasks_url}/{task_id}"

        # 2. Wait for the background task to finish.
        while task["status"] not in ("completed", "failed", "stopped"):
            await asyncio.sleep(3)
            response = await client.get(task_url, headers=headers)
            response.raise_for_status()
            task = response.json()

        if task["status"] != "completed":
            raise RuntimeError(f"Task {task_id} {task['status']}: {task.get('error')}")

        # 3. Read the results, following pagination when needed.
        results = []
        results_url = f"{task_url}/results"
        params = {"limit": 100}
        while True:
            response = await client.get(
                results_url, headers=headers, params=params
            )
            response.raise_for_status()
            page = response.json()
            results.extend(page["results"])
            next_cursor = page["nextCursor"]
            if next_cursor is None:
                break
            params["cursor"] = next_cursor

    return results


async def main() -> None:
    api_key = os.environ["DATABLIST_API_KEY"]
    websites = [
        "https://www.trigema.de",
        "https://www.hetzner.com",
        "https://www.sipgate.de",
        "https://www.manomama.de",
        "https://www.vaude.com",
    ]

    results = await scrape_impressums(websites, api_key)
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
