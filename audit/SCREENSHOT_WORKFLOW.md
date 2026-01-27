# 🚀 QUICK START - Screenshot Directory Workflow

## For Screenshots in `/screenshot/screenshots/`

This is the **fastest way** to audit all your screenshots at once!

---

## ⚡ Super Quick Method (Recommended)

```bash
# 1. Set your API key
export ANTHROPIC_API_KEY='your-key-here'

# 2. Run the specialized script
python quick_audit_screenshots.py
```

That's it! The script will:
- ✅ Find all screenshots in `/screenshot/screenshots/`
- ✅ Auto-detect region from filenames (if possible)
- ✅ Ask you for URL and region for each
- ✅ Run complete audit with consistency check
- ✅ Save reports in `audit_reports/`

---

## 📝 Screenshot Naming Tips

For **auto-detection** to work, name your files like:

### Good Examples (Auto-detected)
- `ca_grade5_math.png` → auto-detects Canada
- `us-grade6-math.png` → auto-detects US
- `uk_year7_maths.png` → auto-detects UK
- `au_year8.png` → auto-detects Australia
- `studypug_nz_grade4.png` → auto-detects New Zealand

### Region Keywords
- **Canada**: `ca`, `canada`, `canadian`
- **US**: `us`, `usa`, `american`
- **UK**: `uk`, `britain`, `british`
- **Australia**: `au`, `australia`, `australian`
- **New Zealand**: `nz`, `newzealand`, `kiwi`
- **Ireland**: `ie`, `ireland`, `irish`
- **Singapore**: `sg`, `singapore`

---

## 🎯 Step-by-Step Walkthrough

### Step 1: Prepare Screenshots
Put all screenshots in: `/screenshot/screenshots/`

```bash
/screenshot/screenshots/
├── ca_grade5.png
├── ca_grade6.png
├── us_grade5.png
└── uk_year6.png
```

### Step 2: Set API Key
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

### Step 3: Run Quick Audit
```bash
python quick_audit_screenshots.py
```

### Step 4: Follow Prompts
```
📸 Screenshot 1/4: ca_grade5.png
   🔍 Auto-detected region: CA
   URL: https://www.studypug.com/ca/grade-5-math
   Region [ca] (ca/us/uk/au/nz/ie/sg): ← just press Enter!
   ✅ Added to batch
```

### Step 5: Review Reports
```
audit_reports/
├── audit_001_ca_www.studypug.com_ca_grade-5-math.json
├── audit_002_ca_www.studypug.com_ca_grade-6-math.json
├── consistency_audit.json
└── batch_audit_summary.json
```

---

## 📊 What You'll Get

### Individual Reports
Each page gets a detailed JSON report with:
- ❌ **Critical issues** - Must fix before launch
  - Banned CTA phrases ("Try Free")
  - Wrong features for grade level
  - Regional cross-contamination
  
- ⚠️ **High issues** - Should fix
  - Social proof contradictions
  - Feature naming inconsistencies
  
- 📝 **Medium/Low issues** - Nice to fix
  - Copy quality
  - UI/UX improvements

### Consistency Report
Checks across ALL pages for:
- ✅ CTA consistency
- ✅ Social proof logic
- ✅ Feature naming standards
- ✅ Testimonial uniqueness
- ✅ Pricing consistency
- ✅ Regional contamination

### Summary Report
Overall statistics:
- Pages audited
- Total issues by severity
- Deployment recommendation
- Top fixes needed

---

## 🔧 Alternative Methods

### Method A: Manual Batch Config

Create `my_audit.json`:
```json
{
  "pages": [
    {
      "url": "https://www.studypug.com/ca/grade-5-math",
      "region": "ca",
      "screenshot": "/screenshot/screenshots/ca_grade5.png"
    }
  ]
}
```

Run:
```bash
python studypug_audit_tool.py batch --config my_audit.json
```

### Method B: One-at-a-Time

```bash
python studypug_audit_tool.py audit \
  --url "https://www.studypug.com/ca/grade-5-math" \
  --region ca \
  --screenshot /screenshot/screenshots/ca_grade5.png
```

---

## ⚠️ Common Issues

### "Directory not found"
**Problem:** `/screenshot/screenshots/` doesn't exist
**Solution:** Check the path, or update the script with your actual path

### "ANTHROPIC_API_KEY not found"
**Problem:** API key not set
**Solution:** `export ANTHROPIC_API_KEY='your-key'`

### "No screenshots found"
**Problem:** No PNG/JPG files in directory
**Solution:** Make sure screenshots are in correct format (PNG, JPG, JPEG, WEBP)

---

## 💡 Pro Tips

1. **Name files with region codes** for auto-detection
   - `ca_grade5.png` → auto-detects Canada ✅
   - `grade5.png` → must enter manually ❌

2. **Run audits in batches** for efficiency
   - Batch of 10 pages: ~2 minutes, $1.80
   - Individual: ~20 minutes, $1.50

3. **Check consistency report** for cross-page issues
   - One page might pass individually
   - But fail consistency check with others

4. **Fix CRITICAL issues first**
   - "Try Free" CTAs block deployment
   - Regional contamination confuses users
   - Wrong features mislead customers

5. **Save audit reports** for comparison
   - Before/after updates
   - Track improvements over time

---

## 📈 Typical Workflow

```
1. Design team exports screenshots
   → /screenshot/screenshots/*.png

2. Run quick audit
   → python quick_audit_screenshots.py

3. Review reports
   → Check audit_reports/batch_audit_summary.json

4. Fix critical issues
   → Update pages

5. Re-audit to verify
   → python quick_audit_screenshots.py (with new screenshots)

6. Deploy ✅
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Audit all screenshots | `python quick_audit_screenshots.py` |
| Audit single page | `python studypug_audit_tool.py audit --url URL --region ca --screenshot /screenshot/screenshots/file.png` |
| Batch from config | `python studypug_audit_tool.py batch --config config.json` |
| Consistency only | `python studypug_audit_tool.py consistency --reports audit_reports/*.json` |

---

## 💰 Cost

- ~$0.15 per page
- 10 pages: ~$1.80
- 50 pages: ~$8.00

Uses Claude Sonnet 4 for best quality results.

---

## ✅ Ready to Start?

```bash
python quick_audit_screenshots.py
```

That's it! The tool will guide you through the rest.
