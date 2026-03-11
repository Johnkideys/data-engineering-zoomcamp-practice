

Module 4 has 2 ways of learning dbt, local way (dbt Core + duckdb) and the cloud way (google BigQuery + dbt Cloud), I have chosen the cloud method for now.

## Setting up Google BigQuery

I have set up Application default credentials on my local laptop to connect to google cloud, the file is in the following folder: ~/.config/gcloud/application_default_credentials.json

To ensure the `gcloud` CLI is using the correct Google identity (email).
```bash
# Returns the email address of the currently active account
gcloud config get-value account
```
Set the default project for your CLI session. While dbt uses the project defined in your profiles.yml, keeping the CLI in sync prevents errors during manual testing or data loading.
```bash
# Replace NEW_PROJECT_ID with your specific GCP Project ID
gcloud config set project NEW_PROJECT_ID
```
For billing purposes so theres no confusion we also set below:
```bash
# Sets the project to be charged for API usage and quotas
gcloud auth application-default set-quota-project NEW_PROJECT_ID
```
To see the current active project
```bash
gcloud config list project
```

<details><summary>What the ThreadPoolExecutor does</summary>
I saw this in the script for week3 and wnated to understand what it is exactly.

### What is ThreadPoolExecutor

Gemini said:
In your script, ThreadPoolExecutor(max_workers=4) is the engine that allows your code to do multiple things at the same time rather than one by one.

Normally, Python runs sequentially (top to bottom). To upload 48 files (2 taxi types × 2 years × 12 months), it would normally wait for file #1 to finish uploading to Google Cloud before starting file #2.

The ThreadPoolExecutor creates a "pool" of 4 worker threads.

- **Worker Threads:** Think of these as 4 separate assistants working for you.
- **Concurrency:** When you run executor.map, Python hands out the upload tasks to these 4 assistants. If Assistant 1 is waiting for a response from GitHub or Google Cloud, Assistants 2, 3, and 4 keep working on other files.

### Why use max_workers=4?

- **Network efficiency:** Uploading data is an I/O-bound task (the bottleneck is your internet speed, not your M4 processor). If you tried to upload all 48 files at once (max_workers=48), you might saturate your bandwidth or get "Rate Limited" (blocked) by GitHub or Google Cloud for making too many requests at once.
- **Balance:** 4 is a conservative, safe number. On an M4 chip, you could easily push this to 10 or 20 to speed things up without breaking a sweat.
- **Hardware details:** A "Thread" is a software concept, not a physical part of the chip. Your M4 chip has 10 physical cores. Each core can handle dozens or even hundreds of threads. By setting max_workers=4, you are simply telling Python: "Don't try to manage more than 4 tasks at the exact same time."

### Why ProcessPoolExecutor is "Heavyweight"

In Python, there is something called the Global Interpreter Lock (GIL). It basically says: "Only one thread can execute Python code at a time."

- **Threads** bypass this by "waiting" (while one thread waits for a GCS upload, another can start).
- **Processes** bypass this by starting 4 separate instances of Python. This allows your Mac to actually run 4 pieces of code at the exact same millisecond.

### When would you switch?

In your current script, you are just moving data (uploading to GCS). Threads are perfect for this because your Mac isn't actually "doing math"; it's just "waiting for the internet."

You would switch to ProcessPoolExecutor if you were:

- Decompressing the .gz files locally before uploading.
- Filtering millions of rows of taxi data using Pandas.
- Calculating the average tip for every trip in the dataset.

</details>

