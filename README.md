# 🤖 AI Code Review Agent (Git Gatekeeper)

A DevOps automation tool that acts as a "Smart Gatekeeper" for your code. It leverages **Git Hooks** and **Gemini 3 Flash** to review changes locally before they are ever committed to your repository.

---

## 🚀 The Core Idea: "Shift-Left" Security
In DevOps, "Shift-Left" means moving testing and security to the earliest possible stage. This tool prevents "oops" commits by analyzing your **Git Staged Changes** and blocking the commit if it detects security risks or logic bugs.



---

## ✨ Key Features
- **Automated Git Hook:** Integrates directly into your workflow via `.git/hooks/pre-commit`.
- **Intelligent Analysis:** Uses Gemini 3 Flash to understand the *intent* of your code, not just syntax.
- **Security Guard:** Specifically looks for hardcoded API keys, dangerous shell commands (`rm -rf`), and SQL injection risks.
- **Context-Aware:** Only reviews the "diff" (the changes you made), making it fast and cost-effective.
- **Commit Blocking:** Exits with a non-zero status to physically stop a `git commit` if critical issues are found.

---

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **AI Brain:** Google Gemini 3 Flash (via `google-genai` SDK)
- **Automation:** Git Hooks (Bash/Shell)
- **Environment:** Miniconda / DevOps Virtual Env
- **APIs:** Google AI Studio

---

## 🏗️ How it Works
1. **Git Add:** You stage your files as usual.
2. **Git Commit:** This triggers the `pre-commit` hook.
3. **Diff Extraction:** The script runs `git diff --cached` to see exactly what you changed.
4. **AI Review:** The diff is sent to Gemini 3 with a custom "Senior Engineer" prompt.
5. **Decision:** - ✅ **PASS:** The commit continues.
   - ❌ **REJECT:** The commit is blocked, and a report is printed in your terminal.

---

## 🚦 Usage Example

When you try to commit code with a security flaw:
```bash
$ git commit -m "Add new feature"
🤖 AI (Gemini 3 Flash) is reviewing your changes...

| Line | Issue | Suggested Fix |
|------|-------|---------------|
| 12   | Hardcoded API Key | Use os.getenv('API_KEY') |
| 45   | Dangerous os.system call | Use the subprocess module with shell=False |

STATUS: REJECT
❌ [GATEKEEPER] Commit blocked. Fix the issues above.
