# 🌐 GitHub Top Languages Card — Custom SVG Generator (Flask API)

A fully customizable **Top Languages** card generator that analyzes your GitHub repositories using the GitHub API and generates a clean **SVG card** you can embed in your GitHub profile README.

This project works similar to `github-readme-stats`, but gives you full control over the UI, API, caching, themes, and customization.

---

## 🚀 Features

- Fetches your **real GitHub language usage** across all repos
- Aggregates total bytes per language
- Generates a **responsive SVG card**
- Easy to deploy on **Railway / Render / Fly.io / Localhost**
- Uses GitHub Token for faster & unlimited API calls
- Simple, lightweight Flask backend
- Extendable with themes, caching, and custom designs

---

## 📁 Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

---

## 🔧 Requirements

- Python **3.8+**
- GitHub Personal Access Token
- Scopes required: **public_repo** (public access only)

---

## 🛠️ Local Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/David234-star/top-langs.git
cd top-langs
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add your GitHub Token

**Linux / macOS:**

```bash
export GITHUB_TOKEN="your_token_here"
```

**Windows PowerShell:**

```powershell
$env:GITHUB_TOKEN="your_token_here"
```

### 4️⃣ Run the server

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/top-langs?username=YOUR_GITHUB_USERNAME
```

---

## 🌐 Deployment Options

This API works perfectly on the following platforms:

### 🚀 Deploy on Railway (BEST CHOICE)

1. Go to [https://railway.app](https://railway.app)
2. Create new project → **Deploy from GitHub repo**
3. Add environment variable:

```
GITHUB_TOKEN=your_token_here
```

4. Deploy → Railway gives a public URL

Your API will be available at:

```
https://your-app.up.railway.app/top-langs?username=YOUR_USERNAME
```

---

## ⚙️ API Documentation

### Endpoint

```
GET /top-langs
```

### Query Parameters

| Name | Required | Description |
| --- | --- | --- |
| username | Yes | GitHub username |
| top_n | No | Number of languages to display (default: 5) |

### Example

```
/top-langs?username=octocat
```

---

## 📄 Environment Variables

| Variable | Description |
| --- | --- |
| `GITHUB_TOKEN` | GitHub PAT for API access |

---

## 🧠 How It Works

1. Fetches all non-forked & non-archived repositories
2. For each repo, retrieves language breakdown from GitHub
3. Sums bytes of code per language
4. Sorts languages by usage
5. Generates an SVG with:
   - Bars
   - Percent values
   - Language labels

---

## 🧪 Example Output

Your final SVG will look like:

- White card background
- Language bars
- Percent calculations
- Clean typography
- Fully image-renderable on GitHub

---

## 🔥 Rate Limits

| Mode | Limit |
| --- | --- |
| With Token | **5000 requests/hour** |
| Without Token | 60 requests/hour (NOT recommended) |

---

## 🚧 Roadmap (Optional Add-ons)

- [ ] Add dark/light theme support
- [ ] Add caching layer (Redis / file-based)
- [ ] Add custom color palettes
- [ ] Add animations inside SVG
- [ ] Add multi-user support

PRs are welcome!

---

## 📜 License

This project is licensed under the **MIT License**.

---

## ❤️ Contributions

Feel free to open PRs, issues, or feature requests.
Custom themes and enhancements are welcome!