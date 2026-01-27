# 🎯 Complete End-to-End Audit Workflow

## 💡 Key Understanding: Two Separate Steps

Your workflow has **two independent steps**:

```
Step 1: Screenshot Capture          Step 2: Audit Screenshots
├─ Tool: url_screenshot.py          ├─ Tool: auto_audit_screenshots.py
├─ Technology: Playwright           ├─ Technology: Claude API
├─ Runs: Locally on your computer   ├─ Runs: API calls to Claude
├─ Cost: FREE ✅                    ├─ Cost: ~$0.15 per page ⚠️
└─ Speed: ~2-3 min per page         └─ Speed: ~10 seconds per page
```

## ⚡ Quick Start (All 280 Pages)

```bash
# 1. Install dependencies
pip install playwright anthropic python-dotenv
playwright install

# 2. Set up credentials
# Create .env file with login credentials (for parent/student pages)
# Set ANTHROPIC_API_KEY (for audit step)
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# 3. Run complete workflow
python end_to_end_audit.py
```

**Choose option 1** for complete workflow (capture → audit)

---

## 📊 Cost Breakdown

### Screenshot Capture (Step 1) - FREE
- **Cost**: $0 (runs locally with Playwright)
- **Time**: ~10 hours for 280 pages
- **Storage**: ~500MB-1GB of PNG files
- **Can run**: Anytime, as many times as you want

### Audit (Step 2) - PAID
- **Cost**: ~$0.15 per page with Claude API
- **Examples**:
  - 1 page: $0.15
  - 10 pages: $1.50
  - 50 pages: $7.50
  - 280 pages: $42.00
- **Time**: ~1 hour for 280 pages
- **Can run**: On specific screenshots only

---

## 🎯 Recommended Strategy

### Strategy 1: Selective Audit (Cost-Effective)
```bash
# Step 1: Capture ALL screenshots (FREE)
python url_screenshot.py

# Step 2: Review screenshots manually, pick the most important
# - High-traffic pages
# - New/changed pages
# - Problem pages

# Step 3: Audit only selected pages
# Edit urls.json to include only pages you want to audit
python auto_audit_screenshots.py

# Cost: $0 + (~$0.15 × selected pages)
# Example: Audit 30 key pages = $4.50 total
```

### Strategy 2: Region-by-Region (Incremental)
```bash
# Capture all screenshots once (FREE)
python url_screenshot.py

# Audit one region at a time
# 1. Canada first (~$5)
# 2. Then US (~$5)
# 3. Continue as budget allows

# Cost: ~$5 per region
```

### Strategy 3: Full Audit (Comprehensive)
```bash
# Complete workflow - everything
python end_to_end_audit.py
# Choose option 1

# Cost: ~$42 for all 280 pages
```

---

## 🛠️ Setup Guide

### Prerequisites

#### 1. Install Python Packages
```bash
# Core dependencies
pip install playwright anthropic python-dotenv

# Install browser for Playwright
playwright install chromium
```

#### 2. Set Up Screenshot Credentials

Create a `.env` file in the same directory as `url_screenshot.py`:

```bash
# .env file example

# Canada credentials
SP_PARENT_USERNAME_DEV_CA=parent@example.com
SP_PARENT_PASSWORD_DEV_CA=password123
SP_STUDENT_USERNAME_DEV_CA=student@example.com
SP_STUDENT_PASSWORD_DEV_CA=password123

# US credentials
SP_PARENT_USERNAME_DEV_US=parent.us@example.com
SP_PARENT_PASSWORD_DEV_US=password123
SP_STUDENT_USERNAME_DEV_US=student.us@example.com
SP_STUDENT_PASSWORD_DEV_US=password123

# Repeat for UK, AU, NZ, IE, SG...
```

**Note**: Only needed for **parent** and **student** pages. Guest pages don't need credentials.

#### 3. Set Up Audit API Key

```bash
# Get your key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# Or add to your ~/.bashrc for persistence:
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
```

---

## 📁 File Structure

After complete workflow:

```
your-project/
├── url_screenshot.py              ← Screenshot capture script
├── auto_audit_screenshots.py      ← Audit automation script
├── end_to_end_audit.py            ← Integrated workflow
├── urls.json                      ← URL configuration
├── .env                           ← Login credentials
├── screenshots/                   ← Generated screenshots (FREE)
│   ├── ca/
│   │   ├── guest/
│   │   ├── parent/
│   │   └── student/
│   ├── us/
│   ├── uk/
│   ├── au/
│   ├── nz/
│   ├── ie/
│   ├── sg/
│   └── shared/
└── audit_reports/                 ← Audit results (PAID)
    ├── audit_001_ca_guest_*.json
    ├── audit_002_ca_parent_*.json
    ├── consistency_audit.json
    └── batch_audit_summary.json
```

---

## 🎮 Usage Modes

### Mode 1: Integrated Workflow (Easiest)
```bash
python end_to_end_audit.py
```

**Interactive menu:**
1. Complete workflow (capture + audit)
2. Capture screenshots only
3. Audit existing screenshots only
4. Exit

### Mode 2: Manual Step-by-Step
```bash
# Step 1: Capture screenshots (FREE)
python url_screenshot.py

# Step 2: Review screenshots manually
# Check screenshots/ directory

# Step 3: Audit (PAID)
python auto_audit_screenshots.py
```

### Mode 3: Individual Tools
```bash
# Just capture screenshots
python url_screenshot.py

# Just audit one page
python studypug_audit_tool.py audit \
  --url "https://dev.studypug.com/parents/ca/" \
  --region ca \
  --screenshot screenshots/ca/guest/parents_ca.png
```

---

## 💰 Cost Control Strategies

### 1. Test First
```bash
# Capture all screenshots (FREE)
python url_screenshot.py

# Audit just 5 pages to test (~$0.75)
# Manually edit urls.json to have only 5 URLs
python auto_audit_screenshots.py

# If satisfied with quality, run full audit
```

### 2. Prioritize Critical Pages
```bash
# Audit only:
# - High-traffic landing pages
# - New/updated pages
# - Pages with known issues

# Example: 20 critical pages = $3
```

### 3. Set API Limits
In Anthropic console (console.anthropic.com):
- Go to Settings → Billing
- Set monthly spending limit
- Get email alerts at threshold

### 4. Incremental Auditing
```bash
# Week 1: Audit Canada pages (~$5)
# Week 2: Audit US pages (~$5)
# Week 3: Continue as needed
```

---

## 🔍 What Gets Audited?

### Per Screenshot:
✅ CTA compliance (no "Try Free" language)
✅ Feature accuracy by grade level
✅ Regional localization (Math vs Maths, etc.)
✅ Copy quality (grammar, readability)
✅ UI/UX elements (with screenshots)
✅ Social proof numbers validation
✅ Testimonial quality and placement

### Cross-Page Analysis:
✅ CTA consistency across pages
✅ Social proof number logic
✅ Feature naming consistency
✅ Testimonial uniqueness
✅ Pricing consistency
✅ Regional cross-contamination detection

---

## ⚙️ Configuration

### Customize Screenshot Settings

Edit `url_screenshot.py`:

```python
# Viewport size
viewport_width=1920,   # Default: 1920
viewport_height=1080,  # Default: 1080

# Wait times
await page.wait_for_timeout(2000)  # Adjust if pages load slowly
```

### Customize Audit Settings

Edit `auto_audit_screenshots.py`:

```python
# Audit specific regions only
regions = ['ca', 'us']  # Only audit Canada and US

# Audit specific user states only
states = ['guest']  # Only audit guest pages
```

---

## 🆘 Troubleshooting

### Screenshot Capture Issues

**"Playwright not found"**
```bash
pip install playwright
playwright install chromium
```

**"Login failed"**
- Check `.env` file exists
- Verify credentials are correct
- Check network connection
- Look at debug screenshots in `screenshots/` folder

**"Screenshots are blank"**
- Increase wait time in script
- Check if page requires JavaScript
- Verify URL is accessible

### Audit Issues

**"ANTHROPIC_API_KEY not found"**
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
# Verify:
echo $ANTHROPIC_API_KEY
```

**"Rate limit exceeded"**
- Wait a few minutes
- Set up spending limits in console
- Contact Anthropic support

**"Auto-mapping failed"**
- Follow naming guide from `generate_screenshot_guide.py`
- Or enter URLs manually when prompted

---

## 📊 Example Workflows

### Workflow A: New Feature Launch
```bash
# 1. Capture all pages (FREE)
python url_screenshot.py

# 2. Manually review - identify changed pages

# 3. Audit only changed pages (~$3-5)
# Edit urls.json to include only changed pages
python auto_audit_screenshots.py

# 4. Fix critical issues

# 5. Re-capture and re-audit changed pages (~$1-2)
```

### Workflow B: Quarterly QA Audit
```bash
# 1. Capture all pages (FREE)
python url_screenshot.py

# 2. Full audit (~$42)
python end_to_end_audit.py

# 3. Review reports
cat audit_reports/batch_audit_summary.json

# 4. Create fix list from critical/high issues

# 5. Implement fixes

# 6. Re-audit fixed pages only (~$5-10)
```

### Workflow C: Regional Expansion
```bash
# Launching new region (e.g., Australia)

# 1. Capture AU screenshots only (FREE)
# Edit urls.json to include only AU URLs
python url_screenshot.py

# 2. Audit AU pages (~$3.50 for 22 pages)
python auto_audit_screenshots.py

# 3. Fix issues before launch

# 4. Re-audit to verify (~$3.50)
```

---

## 🎯 Best Practices

### 1. Capture First, Audit Selectively
- Screenshot capture is FREE
- Run it regularly (weekly/monthly)
- Only audit when needed

### 2. Version Control Your Screenshots
```bash
# Create dated directories
screenshots_2024_12_29/
screenshots_2025_01_15/
```

### 3. Keep Audit Reports
```bash
# Archive reports for comparison
audit_reports_2024_12_29/
audit_reports_2025_01_15/
```

### 4. Test Before Full Audit
- Always test with 5-10 pages first
- Verify audit quality meets your needs
- Then scale to full audit

### 5. Set Up Monitoring
- Schedule weekly screenshot captures
- Audit critical pages monthly
- Full audit quarterly

---

## 📋 Quick Command Reference

```bash
# Complete workflow
python end_to_end_audit.py

# Screenshot capture only
python url_screenshot.py

# Audit only
python auto_audit_screenshots.py

# Generate naming guide
python generate_screenshot_guide.py

# Single page audit
python studypug_audit_tool.py audit --url URL --region ca --screenshot path.png

# View results
cat audit_reports/batch_audit_summary.json | python -m json.tool
```

---

## 💡 Pro Tips

1. **Screenshots are your safety net** - Capture everything regularly (it's free!)
2. **Audit strategically** - Focus budget on high-impact pages
3. **Use test accounts** - Set up dedicated test accounts in `.env`
4. **Monitor costs** - Set spending limits in Anthropic console
5. **Archive everything** - Keep screenshots and reports for comparison

---

## 🚀 Ready to Start?

### Minimal Setup (5 minutes):
```bash
pip install playwright anthropic python-dotenv
playwright install chromium
export ANTHROPIC_API_KEY='your-key'
python end_to_end_audit.py
```

### Complete Setup (15 minutes):
1. Install dependencies
2. Create `.env` with credentials
3. Set ANTHROPIC_API_KEY
4. Run test with 5 pages
5. Review results
6. Run full workflow

---

## 📚 Additional Resources

- **AUTOMATED_WORKFLOW.md** - Detailed audit workflow guide
- **SCREENSHOT_WORKFLOW.md** - Screenshot-specific guide
- **README.md** - Complete tool documentation
- **INDEX.md** - Master file index

---

**Questions?** Review the documentation or test with a small batch first!
