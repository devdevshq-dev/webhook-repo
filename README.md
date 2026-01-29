Here is a professional `README.md` file tailored for your **webhook-repo**. You can copy and paste this directly into your repository.

It is structured to explain the architecture, setup, and "Brownie Point" logic clearly, which will be helpful for the reviewer.

---

# TechStaX Webhook Receiver & Dashboard

This project is a **Flask-based Webhook Receiver** that listens for GitHub repository events (Push, Pull Request, and Merge), stores specific payload data into **MongoDB**, and displays the activity on a real-time **polling UI**.

## 🚀 Project Architecture

The application follows the flow described in the assessment :

1. **Trigger:** `action-repo` (GitHub) sends a webhook payload on Push, PR, or Merge.
2. **Receiver:** `webhook-repo` (Flask) accepts the JSON payload at `/webhook`.
3. **Storage:** Data is parsed and stored in **MongoDB** according to the required schema.


4. **Frontend:** A minimal UI polls the database every **15 seconds** to fetch and display the latest changes.



## 🛠️ Tech Stack

* **Backend:** Python (Flask) 


* **Database:** MongoDB 


* **Frontend:** HTML5, JavaScript (Fetch API for polling) 


* **Tools:** ngrok (for local webhook testing)

## ⚙️ Installation & Setup

### 1. Prerequisites

* Python 3.x
* MongoDB (Running locally on default port `27017` or via Atlas)

### 2. Clone the Repository

```bash
git clone <your-webhook-repo-url>
cd webhook-repo

```

### 3. Install Dependencies

```bash
pip install flask pymongo

```

### 4. Database Setup

Ensure your MongoDB instance is running. The application connects to `mongodb://localhost:27017/` by default and creates a database named `techstax_db`.

### 5. Run the Application

```bash
python app.py

```

The server will start at `http://localhost:5000`.

## 🔗 Webhook Configuration

To connect your **GitHub Action Repo** to this backend:

1. **Expose Localhost:** Use ngrok to create a public URL for your local server.
```bash
ngrok http 5000

```


2. **Add Webhook in GitHub:**
* Go to your `action-repo` > **Settings** > **Webhooks**.


* **Payload URL:** `https://<your-ngrok-url>/webhook`
* **Content type:** `application/json`
* **Events:** Select "Let me select individual events" and check:
* **Pushes**
* **Pull requests**





## 💡 Logic & Features implemented

### Data Formatting

The application parses the GitHub payload to match the strict schema requirements.

* **Request ID:** Stores the Commit Hash (for Push) or PR ID (for Pull Requests).
* **Timestamps:** Stored as UTC strings.

### The "Merge" Event Logic (Brownie Points)

GitHub does not have a dedicated `merge` event type. As per the requirement to capture Merge actions, the logic handles this by checking the `pull_request` payload:

* If `action == "closed"` **AND** `merged == true`, the system records it as a **"MERGE"** event.
* Otherwise, it is recorded as a standard **"PULL_REQUEST"**.

## 🖥️ Usage

1. Open the dashboard at `http://localhost:5000`.
2. Trigger events in your `action-repo`:
* **Push Code:** UI displays `{author} pushed to {branch}`.


* **Open PR:** UI displays `{author} submitted a pull request...`.


* **Merge PR:** UI displays `{author} merged branch...`.




3. Wait 15 seconds for the next poll to see the update.

## 📂 Project Structure

```text
/webhook-repo
  ├── app.py                # Main Flask application & Logic
  ├── templates/
  │   └── index.html        # UI with polling script
  └── README.md             # Project documentation

```

**Next Step:** Would you like me to create the **GitHub `action-repo**` content (e.g., a dummy Python script to push/modify) so you have something to trigger these events with?
