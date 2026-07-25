# 🛡️ GitGuard: AI-Powered Code Risk & PR Auditor

**Live App URL:** [Paste Your Live Streamlit URL Here](https://your-app-url.streamlit.app)

---

## 📌 Problem & Target Audience
Developers, open-source maintainers, and QA engineers lose hours manually reviewing pull requests, estimating risk levels, and identifying missed edge cases in unit tests. Junior developers often push code without proper PR descriptions or adequate test coverage, leading to silent bugs in production.

**GitGuard** solves this by acting as an automated AI reviewer that ingests code changes/diffs, flags security risks on a 1-10 scale, drafts formatted PR descriptions, and automatically generates PyTest code stubs for missing test coverage.

---

## ✨ Features List
- **Automated Risk Scoring:** Visual gauge (1-10 scale) categorizing change safety.
- **Change Classification:** Detects if code changes are Refactors, Features, Breaking Changes, or Security Patches.
- **PR Description Generator:** Outputs conventional commit titles and Markdown descriptions ready to paste into GitHub.
- **Missing Test Detection:** Pinpoints precise logic gaps that lack test coverage.
- **One-Click Unit Test Stub Generation:** Produces downloadable/copyable `pytest` stubs for identified missing scenarios.

---

## 🤖 AI Features & Prompt Architecture
Driven by OpenAI's `gpt-4o-mini` model with strict JSON response formatting.

### System Prompt Instructions:
> *"You are a Senior Security Auditor and QA Architect. Analyze the code/diff provided and return a JSON object with EXACTLY these keys: `change_type`, `pr_title`, `pr_body`, `missing_tests` (array), and `risk_score` (1-10)."*

---

## 🛠️ Stack & Tools Used
- **Frontend/UI:** Streamlit Framework
- **AI Integration:** OpenAI API (`gpt-4o-mini`)
- **Language:** Python 3.10+
- **Hosting:** Streamlit Community Cloud

---

## 📸 App Screenshots
*(Take 3 screenshots of your deployed live app and link them here)*
1. **Input Interface & Sidebar Configuration**
2. **AI Risk Assessment & Metrics Dashboard**
3. **Generated Test Stubs Output**

---

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/gitguard-pr-auditor.git](https://github.com/YOUR_USERNAME/gitguard-pr-auditor.git)
   cd gitguard-pr-auditor
