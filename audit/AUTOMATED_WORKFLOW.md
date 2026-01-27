# 🚀 Automated Screenshot Audit Workflow

**For organized screenshots with URL mapping from urls.json**

This is the **most powerful** way to audit your screenshots - fully automated with URL mapping!

---

## 📋 Overview

Your screenshot structure:
```
/screenshot/screenshots/
├── ca/
│   ├── guest/*.png          (29 URLs)
│   ├── parent/*.png         (2 URLs)
│   └── student/*.png        (2 URLs)
├── us/
│   ├── guest/*.png          (29 URLs)
│   ├── parent/*.png         (2 URLs)
│   └── student/*.png        (2 URLs)
├── uk/
│   ├── guest/*.png          (18 URLs)
│   ├── parent/*.png         (2 URLs)
│   └── student/*.png        (2 URLs)
├── au/
│   ├── guest/*.png          (18 URLs)
│   ├── parent/*.png         (2 URLs)
│   └── student/*.png        (2 URLs)
├── nz/
│   ├── guest/*.png          (18 URLs)
│   ├── parent/*.png         (2 URLs)
│   └── student/*.png        (2 URLs)
├── ie/
│   ├── guest/*.png          (18 URLs)
│   ├── parent/*.png         (2 URLs)
│   └── student/*.png        (2 URLs)
├── sg/
│   ├── guest/*.png          (18 URLs)
│   ├── parent/*.png         (2 URLs)
│   └── student/*.png        (2 URLs)
└── shared/
    └── guest/*.png          (32 URLs)
```

**Total: 280+ URLs across 7 regions + shared**

---

## ⚡ Quick Start (2 Steps!)

### Step 1: Generate Screenshot Naming Guide
```bash
python generate_screenshot_guide.py
```

This creates:
- `screenshot_naming_guide.txt` - Human-readable guide
- `screenshot_naming_guide.json` - Machine-readable mapping
- `create_screenshot_dirs.sh` - Script to create directory structure

### Step 2: Run Automated Audit
```bash
# Set API key
export ANTHROPIC_API_KEY='your-key-here'

# Run automated audit
python auto_audit_screenshots.py
```

**That's it!** The tool will:
1. ✅ Load URLs from `urls.json`
2. ✅ Scan all screenshot directories
3. ✅ Auto-map screenshots to URLs
4. ✅ Let you fill in any missing mappings
5. ✅ Run complete audit with consistency check
6. ✅ Generate all reports

---

## 📸 Screenshot Naming for Auto-Mapping

The tool auto-maps screenshots to URLs based on filename matching.

### Good Names (Auto-detected)
```
parents_ca.png              → https://dev.studypug.com/parents/ca/
students_us.png             → https://dev.studypug.com/students/us/
grade1.png                  → https://dev.studypug.com/ca/grade1/
grade1_practice-test.png    → https://dev.studypug.com/ca/grade1/practice-test
signin_role=parent.png      → https://dev.studypug.com/signin/ca/?role=parent
```

### How Auto-Mapping Works
The tool extracts key parts from the URL and matches them to screenshot names:
- URL: `https://dev.studypug.com/parents/ca/`
- Key parts: `parents`, `ca`
- Matches screenshots containing: `parents`, `ca`, `parents_ca`, etc.

### Generate Naming Guide
```bash
python generate_screenshot_guide.py
```

This creates a complete mapping showing suggested names for all 280+ URLs.

---

## 🏗️ Setup Workflow (First Time)

### 1. Create Directory Structure
```bash
# Generate the directory creation script
python generate_screenshot_guide.py

# Run the script
./create_screenshot_dirs.sh
```

This creates all necessary directories:
```
/screenshot/screenshots/
├── ca/guest/
├── ca/parent/
├── ca/student/
├── us/guest/
... etc
```

### 2. Take Screenshots

Follow the naming guide in `screenshot_naming_guide.txt`:

**Example for Canada guest pages:**
```
URL: https://dev.studypug.com/parents/ca/
Screenshot: parents_ca.png
Save to: /screenshot/screenshots/ca/guest/parents_ca.png

URL: https://dev.studypug.com/students/ca/
Screenshot: students_ca.png
Save to: /screenshot/screenshots/ca/guest/students_ca.png
```

### 3. Run Automated Audit
```bash
python auto_audit_screenshots.py
```

---

## 🎯 URL Mapping Strategies

The tool uses intelligent matching to map screenshots to URLs:

### Strategy 1: Exact Match
```
Screenshot: grade1.png
URL: /ca/grade1/
✅ Matched!
```

### Strategy 2: Partial Match
```
Screenshot: ca_grade1_main.png
URL: /ca/grade1/
✅ Matched! (contains "grade1")
```

### Strategy 3: Multi-part Match
```
Screenshot: parents_ca_homepage.png
URL: /parents/ca/
✅ Matched! (contains both "parents" and "ca")
```

### Manual Override
If auto-mapping fails, the tool prompts you:
```
📸 unknown_page.png
   Region: CA | State: guest
   URL: [enter URL here]
```

---

## 📊 What Gets Audited

### Per Region + User State
- **Canada (CA)**: 29 guest + 2 parent + 2 student = 33 pages
- **US**: 29 guest + 2 parent + 2 student = 33 pages
- **UK**: 18 guest + 2 parent + 2 student = 22 pages
- **Australia (AU)**: 18 guest + 2 parent + 2 student = 22 pages
- **New Zealand (NZ)**: 18 guest + 2 parent + 2 student = 22 pages
- **Ireland (IE)**: 18 guest + 2 parent + 2 student = 22 pages
- **Singapore (SG)**: 18 guest + 2 parent + 2 student = 22 pages
- **Shared**: 32 guest pages

**Total: 208 unique pages**

### Audit Coverage
✅ Individual page audits (all pages)
✅ Regional consistency (per region)
✅ Cross-region consistency (all regions)
✅ User state consistency (guest vs parent vs student)

---

## 📈 Output Reports

After audit completes:

```
audit_reports/
├── audit_001_ca_guest_parents.json
├── audit_002_ca_guest_students.json
├── audit_003_ca_parent_payment.json
... (208 individual reports)
├── consistency_audit.json           ← Cross-page consistency
└── batch_audit_summary.json         ← Overall summary
```

### Summary Report Shows:
- Total pages audited
- Critical issues count (must fix)
- High priority issues
- Medium/low issues
- Deployment recommendation
- Pages requiring updates

---

## 🔍 Advanced Features

### Audit Specific Region Only
Edit `auto_audit_screenshots.py` and modify the `scan_screenshots()` function:
```python
# Scan only Canada
regions = ['ca']

# Scan only US and UK
regions = ['us', 'uk']
```

### Audit Specific User State
```python
# In scan_screenshots(), modify states:
states = ['guest']  # Only audit guest pages
states = ['parent', 'student']  # Only logged-in pages
```

### Re-run Failed Pages
If some pages fail, re-run just those:
```bash
python studypug_audit_tool.py audit \
  --url "URL" \
  --region ca \
  --screenshot /screenshot/screenshots/ca/guest/page.png
```

---

## 💰 Cost Estimation

With Claude Sonnet 4 at ~$0.15 per page:

| Scope | Pages | Cost |
|-------|-------|------|
| Single region (CA/US) | 33 | ~$5 |
| All regions | 208 | ~$31 |
| Just guest pages | 180 | ~$27 |
| Just logged-in pages | 28 | ~$4 |

**Tip:** Start with one region to test, then scale to all regions.

---

## ⚙️ Configuration

### URLs File
The tool uses `urls.json` with this structure:
```json
{
  "ca": {
    "guest_urls": [...],
    "parent_urls": [...],
    "student_urls": [...]
  },
  "us": { ... },
  ...
  "shared": {
    "guest_urls": [...]
  }
}
```

### Screenshot Base Path
Default: `/screenshot/screenshots/`

To change, edit `auto_audit_screenshots.py`:
```python
def scan_screenshots(base_path: Path = Path("/your/custom/path")):
```

---

## 🆘 Troubleshooting

### "urls.json not found"
**Solution:** Place `urls.json` in:
- Current directory, OR
- `/mnt/user-data/uploads/`, OR
- Run `python generate_screenshot_guide.py` from directory containing `urls.json`

### "Screenshot base path not found"
**Solution:** 
1. Create directories: `./create_screenshot_dirs.sh`
2. Or update path in `auto_audit_screenshots.py`

### "Auto-mapping failed for many screenshots"
**Solution:** 
1. Use the naming guide: `screenshot_naming_guide.txt`
2. Rename screenshots to match URL patterns
3. Or provide URLs manually when prompted

### "ANTHROPIC_API_KEY not found"
**Solution:** `export ANTHROPIC_API_KEY='your-key'`

---

## 🎯 Recommended Workflow

### For New Development
```bash
# 1. Generate naming guide
python generate_screenshot_guide.py

# 2. Create directories
./create_screenshot_dirs.sh

# 3. Take screenshots following the guide
# (Save to correct directories with correct names)

# 4. Run automated audit
python auto_audit_screenshots.py

# 5. Review reports
cat audit_reports/batch_audit_summary.json
```

### For Existing Screenshots
```bash
# 1. Organize screenshots into directory structure
# /screenshot/screenshots/{region}/{state}/*.png

# 2. Run automated audit
python auto_audit_screenshots.py

# 3. Provide URLs for unmapped screenshots when prompted

# 4. Review reports
cat audit_reports/batch_audit_summary.json
```

### For Updates/Changes
```bash
# 1. Update screenshots in their directories

# 2. Re-run audit
python auto_audit_screenshots.py

# 3. Compare with previous reports
diff audit_reports/batch_audit_summary.json previous_reports/batch_audit_summary.json
```

---

## 📚 Files in This Workflow

| File | Purpose |
|------|---------|
| `urls.json` | URL structure (provided by you) |
| `auto_audit_screenshots.py` | Main automated audit tool |
| `generate_screenshot_guide.py` | Creates naming guide |
| `screenshot_naming_guide.txt` | Human-readable naming guide |
| `screenshot_naming_guide.json` | Machine-readable mapping |
| `create_screenshot_dirs.sh` | Creates directory structure |

---

## ✅ Quick Command Reference

```bash
# Generate guides
python generate_screenshot_guide.py

# Create directories
./create_screenshot_dirs.sh

# Run automated audit
python auto_audit_screenshots.py

# Audit single page
python studypug_audit_tool.py audit --url URL --region ca --screenshot path.png

# Check consistency only
python studypug_audit_tool.py consistency --reports audit_reports/*.json

# View summary
cat audit_reports/batch_audit_summary.json | python -m json.tool
```

---

## 🚀 Ready to Start?

```bash
# Step 1: Generate guide
python generate_screenshot_guide.py

# Step 2: Run audit
python auto_audit_screenshots.py
```

That's it! The tool handles the rest.
