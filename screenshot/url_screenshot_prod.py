def remove_all_auth_states():
    """Remove all storage_state_*.json files in the screenshots directory."""
    screenshots_dir = Path("screenshots")
    for f in screenshots_dir.glob("storage_state_*.json"):
        try:
            f.unlink()
            print(f"🚪 Removed auth state before guest screenshot: {f}")
        except Exception as e:
            print(f"⚠️ Could not remove auth state: {e}")
#!/usr/bin/env python3
"""
URL Screenshot Tool
Takes screenshots of a list of URLs and saves them as PNG files.
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime
import re
import os  # NEW
import json  # NEW
from dotenv import load_dotenv  # NEW

# Load .env from the same folder as this script
ENV_PATH = Path(__file__).parent / ".env"  # NEW
load_dotenv(dotenv_path=ENV_PATH)  # NEW

# Role-based auth storage paths
def get_auth_state_path(role: str) -> Path:
    role_key = (role or "default").lower()
    return Path("screenshots") / f"storage_state_{role_key}.json"


def sanitize_filename(url):
    """Convert URL to a safe filename."""
    filename = re.sub(r'^https?://', '', url)
    filename = re.sub(r'[^\w\-.]', '_', filename)
    if filename.startswith('www.studypug.com_'):
        filename = filename[len('www.studypug.com_'):]
    if len(filename) > 100:
        filename = filename[:100]
    return filename

def _debug_env(role: str, user_var: str, pass_var: str):
    u = os.getenv(user_var)
    p = os.getenv(pass_var)
    print(
        f"🔎 Env loaded from: {ENV_PATH} | role={role} | {user_var} set: {bool(u)} | {pass_var} set: {bool(p)}"
    )

# NEW: login helpers
async def login_and_save_state(p, auth_url: str, role: str, locale:str):




    # Choose role-specific env vars (fallback to generic)
    role_l = (role or "").lower()
    locale_l = (locale or "").lower()
    CREDENTIAL_ENV_MAP = {
        "ca": {
            "parent": ("SP_PARENT_USERNAME_PROD_CA", "SP_PARENT_PASSWORD_PROD_CA"),
            "student": ("SP_STUDENT_USERNAME_PROD_CA", "SP_STUDENT_PASSWORD_PROD_CA"),
        },
        "us": {
            "parent": ("SP_PARENT_USERNAME_PROD_US", "SP_PARENT_PASSWORD_PROD_US"),
            "student": ("SP_STUDENT_USERNAME_PROD_US", "SP_STUDENT_PASSWORD_PROD_US"),
        },
        "uk": {
            "parent": ("SP_PARENT_USERNAME_PROD_UK", "SP_PARENT_PASSWORD_PROD_UK"),
            "student": ("SP_STUDENT_USERNAME_PROD_UK", "SP_STUDENT_PASSWORD_PROD_UK"),
        },
        "au": {
            "parent": ("SP_PARENT_USERNAME_PROD_AU", "SP_PARENT_PASSWORD_PROD_AU"),
            "student": ("SP_STUDENT_USERNAME_PROD_AU", "SP_STUDENT_PASSWORD_PROD_AU"),
        },
    }

    email_env, pass_env = CREDENTIAL_ENV_MAP.get(
        locale_l,
        {}
    ).get(
        role_l,
        ("SP_USERNAME_DEV", "SP_PASSWORD_DEV")
    )

    _debug_env(role_l or "default", email_env, pass_env)
    username = os.getenv(email_env)
    password = os.getenv(pass_env)
    if not username or not password:
        raise RuntimeError(f"Missing credentials: set {email_env} and {pass_env} (env path: {ENV_PATH})")

    browser = await p.chromium.launch(headless=False)  # keep visible while debugging
    context = await browser.new_context()
    page = await context.new_page()

    print(f"🔐 Logging in at: {auth_url}")
    await page.goto(auth_url, wait_until='domcontentloaded', timeout=60000)
    
    # Wait for Material-UI form to render
    await page.wait_for_timeout(500)
    
    # Debug: screenshot the signin page
    await page.screenshot(path="screenshots/signin_form.png", full_page=True)
    print(f"  📸 Debug screenshot saved: screenshots/signin_form.png")
    
    # Inspect page structure to debug
    frames = page.frames
    print(f"🔍 Page frames: {len(frames)} frame(s)")
    for i, frame in enumerate(frames):
        print(f"   Frame {i}: {frame.name or '(unnamed)'}")
    
    # Get all input fields on the page
    all_inputs = await page.locator('input').all()
    print(f"🔍 Total input fields found: {len(all_inputs)}")
    for i, inp in enumerate(all_inputs):
        try:
            input_type = await inp.get_attribute('type')
            input_name = await inp.get_attribute('name')
            input_id = await inp.get_attribute('id')
            input_placeholder = await inp.get_attribute('placeholder')
            print(f"   Input {i}: type={input_type}, name={input_name}, id={input_id}, placeholder={input_placeholder}")
        except:
            pass

    # Fill credentials with concrete selectors
    try:
        # Email - try many selectors
        target = page  # assume top-level form
        email_filled = False
        email_selectors = [
            'input#Email',
            'input[id="Email"]',
            'input[type="email"]',
            'input[placeholder*="someone@email" i]',
            'input[name="email"]',
        ]
        
        for sel in email_selectors:
            if await target.locator(sel).first.count():
                try:
                    await target.fill(sel, username)
                    email_filled = True
                    print(f"  ✓ Filled email via {sel}")
                    break
                except:
                    continue

        # Password
        password_filled = False
        password_selectors = [
            'input#component-outlined2',
            'input[id="component-outlined2"]',
            'input[type="password"]',
            'input[placeholder*="6-40" i]',
            'input[name="password"]',
        ]
        
        for sel in password_selectors:
            count = await target.locator(sel).count()
            if count > 0:
                try:
                    await target.fill(sel, password)
                    password_filled = True
                    print(f"  ✓ Filled password via {sel}")
                    break
                except:
                    continue

        # Submit: look for the yellow "Log in" button
        submitted = False
        submit_selectors = [
            'button:has-text("Log in")',
            'button:has-text("Login")',
            'button[type="submit"]',
            'button:has-text("Sign in")',
            'button[name="login"]',
        ]
        
        for sel in submit_selectors:
            count = await target.locator(sel).count()
            if count > 0:
                print(f"  ✓ Clicking button via: {sel}")
                await target.locator(sel).first.click()
                submitted = True
                break
        
        if not submitted:
            print(f"  ⚠️ Could not find submit button, trying Enter key")
            # Try pressing Enter on password field
            pwd_fields = await target.locator('input[placeholder*="Password" i], input[type="password"]').all()
            if pwd_fields:
                await pwd_fields[0].press('Enter')
            else:
                print(f"  ⚠️ No password field found for Enter key")
    except Exception as e:
        print(f"⚠️ Login interaction failed: {e}")
        try:
            await page.screenshot(path="screenshots/login_error.png", full_page=True)
            print(f"  📸 Error state screenshot saved: screenshots/login_error.png")
        except:
            pass
        await browser.close()
        raise

    # Wait for navigation away from signin and network to settle
    try:
        await page.wait_for_url(re.compile(r'^(?!.*\/signin).*'), timeout=15000)
        print(f"  ✓ URL changed away from /signin")
    except Exception:
        print(f"  ℹ️ URL did not change away from /signin")

    # Give page a moment to stabilize but don't wait for full networkidle
    await page.wait_for_timeout(2000)

    # Debug screenshot to see what page we're actually on
    await page.screenshot(path="screenshots/login_attempt.png", full_page=True)
    print(f"  📸 Debug screenshot saved: screenshots/login_attempt.png")

    # Post-login signal: adjust to your app (avatar/menu/etc.)
    # Example selectors — replace with a reliable one in your UI:
    post_login_ok = False
    for sel in [
        '[data-test="user-menu"]',
        '.UserMenu',
        'nav [aria-label*="Account"]',
        'a[href*="/dashboard"]',
    ]:
        if await page.locator(sel).first.count():
            post_login_ok = True
            break

    url_after = page.url
    cookies = await context.cookies()
    all_cookies = [(c.get("name"), c.get("domain")) for c in cookies]
    has_session = any(
        ("studypug" in c.get("domain", "")) and (
            "session" in c.get("name", "").lower() or "auth" in c.get("name", "").lower()
        ) for c in cookies
    )
    print(f"🔎 Post-login URL: {url_after}")
    print(f"🔎 Cookies: {all_cookies}")
    print(f"🔎 Session cookie found: {has_session}")
    print(f"🔎 Post-login selector found: {post_login_ok}")

    if ("signin" in url_after and not has_session and not post_login_ok):
        print(f"⚠️ Still on sign-in page with no auth indicators. Check screenshots/login_attempt.png")
        await browser.close()
        raise RuntimeError("Login likely failed: still on sign-in with no session and no post-login selector.")

    auth_path = get_auth_state_path(role_l or "default")
    auth_path.parent.mkdir(parents=True, exist_ok=True)
    await context.storage_state(path=str(auth_path))
    print(f"✅ Auth state saved to: {auth_path}")
    await browser.close()


async def create_authenticated_context(p, role: str):
    auth_path = get_auth_state_path((role or "default").lower())
    if not auth_path.exists():
        raise RuntimeError(f"Auth state not found for role '{role}'. Run login first.")
    browser = await p.chromium.launch()
    context = await browser.new_context(storage_state=str(auth_path))
    return browser, context


async def take_screenshot(
    url,
    output_dir="screenshots",
    viewport_width=1920,
    viewport_height=1080,
    use_auth=False,
    auth_url="https://www.studypug.com/signin/ca/?role=student",
    role: str | None = None,
    locale: str | None = None
):
    """
    Take a screenshot of a single URL.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    filename = sanitize_filename(url) + '.png'
    filepath = Path(output_dir) / filename

    async with async_playwright() as p:
        # Prepare browser/context
        if use_auth:
            if not role:
                raise RuntimeError("use_auth=True requires a role ('parent' or 'student')")
            auth_path = get_auth_state_path(role)
            if not auth_path.exists():
                print(f"ℹ️ No auth state found for role '{role}'. Performing login...")
                await login_and_save_state(p, auth_url, role, locale)
            else:
                print(f"ℹ️ Using existing auth state at {auth_path}")
            browser, context = await create_authenticated_context(p, role)
        else:
            browser = await p.chromium.launch()
            context = await browser.new_context()

        page = await context.new_page()
        await page.set_viewport_size({'width': viewport_width, 'height': viewport_height})

        try:
            print(f"📸 Capturing: {url}")
            await page.goto(url, wait_until='networkidle', timeout=90000)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=str(filepath), full_page=True)
            print(f"✅ Saved: {filepath}")
        except Exception as e:
            print(f"❌ Error capturing {url}: {str(e)}")
        finally:
            await page.close()
            await browser.close()


async def take_screenshots_batch(
    urls,
    output_dir="screenshots",
    viewport_width=1920,
    viewport_height=1080,
    use_auth=False,
    auth_url="https://www.studypug.com/signin/ca/?role=student",
    role: str | None = None,
    locale: str | None = None
):
    """
    Take screenshots of multiple URLs efficiently.
    """
    print(f"📋 take_screenshots_batch called with use_auth={use_auth}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        # Prepare browser/context
        if use_auth:
            if not role:
                raise RuntimeError("use_auth=True requires a role ('parent' or 'student')")
            print(f"🔐 Auth mode enabled for role '{role}'")
            auth_path = get_auth_state_path(role)
            if not auth_path.exists():
                print(f"ℹ️ No auth state found at {auth_path}. Performing login...")
                await login_and_save_state(p, auth_url, role, locale)
            else:
                print(f"ℹ️ Using existing auth state at {auth_path}")
            browser, context = await create_authenticated_context(p, role)
        else:
            browser = await p.chromium.launch()
            context = await browser.new_context()

        for url in urls:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            filename = sanitize_filename(url)

            # replace signin with start for auth-related pages
            if use_auth and "signin" in filename:
                filename = filename.replace('signin', 'start')

            filename += '.png'
            filepath = Path(output_dir) / filename

            page = await context.new_page()
            await page.set_viewport_size({'width': viewport_width, 'height': viewport_height})

            try:
                print(f"📸 Capturing: {url}")
                await page.goto(url, wait_until='networkidle', timeout=90000)
                await page.wait_for_timeout(1000)
                await page.screenshot(path=str(filepath), full_page=True)
                print(f"✅ Saved: {filepath}")
            except Exception as e:
                print(f"❌ Error capturing {url}: {str(e)}")
            finally:
                await page.close()

        await browser.close()


async def main():
    """Main function with separate guest, parent, and student screenshot batches."""
    
    # Load URLs from JSON file
    json_path = Path(__file__).parent / "urls_prod.json"
    if not json_path.exists():
        print(f"❌ Error: URLs file not found at {json_path}")
        return
    
    with open(json_path, 'r') as f:
        urls_data = json.load(f)
    
    # Process CA region
    ca_data = urls_data.get("ca", {})
    ca_guest = ca_data.get("guest_urls", [])
    ca_parent = ca_data.get("parent_urls", [])
    ca_student = ca_data.get("student_urls", [])
    
    
    # Process US region
    us_data = urls_data.get("us", {})
    us_guest = us_data.get("guest_urls", [])
    us_parent = us_data.get("parent_urls", [])
    us_student = us_data.get("student_urls", [])
    
    # Process UK region
    uk_data = urls_data.get("uk", {})
    uk_guest = uk_data.get("guest_urls", [])
    uk_parent = uk_data.get("parent_urls", [])
    uk_student = uk_data.get("student_urls", [])
    
    # Process AU region
    au_data = urls_data.get("au", {})
    au_guest = au_data.get("guest_urls", [])
    au_parent = au_data.get("parent_urls", [])
    au_student = au_data.get("student_urls", [])
    
    # Shared URLs
    shared_data = urls_data.get("shared", {})
    shared_guest = shared_data.get("guest_urls", [])

    print(f"🚀 Starting screenshot capture")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Take Canada guest screenshots
    if ca_guest:
        remove_all_auth_states()
        print(f"📸 Canada Guest Screenshots: {len(ca_guest)} URLs (no authentication)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=ca_guest,
            output_dir="screenshots/prod/desktop/ca/guest",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=False
        )
        print()

    # Take Canada parent authenticated screenshots
    if ca_parent:
        print(f"🔐 Canada Parent Screenshots: {len(ca_parent)} URLs (requires parent login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=ca_parent,
            output_dir="screenshots/prod/desktop/ca/parent",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://www.studypug.com/signin/ca/?role=parent",
            role="parent",
            locale="ca",
        )
        print()

    # Take Canada student authenticated screenshots
    if ca_student:
        remove_all_auth_states()
        print(f"🔐 Canada Student Screenshots: {len(ca_student)} URLs (requires student login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=ca_student,
            output_dir="screenshots/prod/desktop/ca/student",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://www.studypug.com/signin/ca/?role=student",
            role="student",
            locale="ca",
        )
        print()

    # Take US guest screenshots
    if us_guest:
        # Remove all storage_state_*.json files before guest screenshots
        remove_all_auth_states()
        print(f"📸 US Guest Screenshots: {len(us_guest)} URLs (no authentication)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=us_guest,
            output_dir="screenshots/prod/desktop/us/guest",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=False
        )
        print()

    # Take US parent authenticated screenshots
    if us_parent:
        print(f"🔐 US Parent Screenshots: {len(us_parent)} URLs (requires parent login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=us_parent,
            output_dir="screenshots/prod/desktop/us/parent",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://www.studypug.com/signin/us/?role=parent",
            role="parent",
            locale="us",
        )
        print()

    # Take US student authenticated screenshots
    if us_student:
        remove_all_auth_states()
        print(f"🔐 US Student Screenshots: {len(us_student)} URLs (requires student login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=us_student,
            output_dir="screenshots/prod/desktop/us/student",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://www.studypug.com/signin/us/?role=student",
            role="student",
            locale="us",
        )
        print()
    # Take UK guest screenshots
        
    if uk_guest:
        remove_all_auth_states()
        print(f"📸 UK Guest Screenshots: {len(uk_guest)} URLs (no authentication)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=uk_guest,
            output_dir="screenshots/prod/desktop/uk/guest",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=False
        )
        print()    
        
     # Take UK parent authenticated screenshots
    if uk_parent:
        print(f"🔐 UK Parent Screenshots: {len(uk_parent)} URLs (requires parent login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=uk_parent,
            output_dir="screenshots/prod/desktop/uk/parent",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://www.studypug.com/signin/uk/?role=parent",
            role="parent",
            locale="uk",
        )
        print()
     # Take UK parent authenticated screenshots
    if uk_student:
        remove_all_auth_states()
        print(f"🔐 UK Student Screenshots: {len(uk_student)} URLs (requires student login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=uk_student,
            output_dir="screenshots/prod/desktop/uk/student",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://www.studypug.com/signin/uk/?role=student",
            role="student",
            locale="uk",
        )
        print()

    if au_guest:
        remove_all_auth_states()
        print(f"📸 AU Guest Screenshots: {len(au_guest)} URLs (no authentication)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=au_guest,
            output_dir="screenshots/prod/desktop/au/guest",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=False
        )
        print()    
     # Take AU parent authenticated screenshots
    if au_parent:
        print(f"🔐 AU Parent Screenshots: {len(au_parent)} URLs (requires parent login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=au_parent,
            output_dir="screenshots/prod/desktop/au/parent",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://www.studypug.com/signin/au/?role=parent",
            role="parent",
            locale="au",
        )
        print()
    # Take AU student authenticated screenshots
    if au_student:
        remove_all_auth_states()
        print(f"🔐 AU Student Screenshots: {len(au_student)} URLs (requires student login)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=au_student,
            output_dir="screenshots/prod/desktop/au/student",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=True,
            auth_url="https://www.studypug.com/signin/au/?role=student",
            role="student",
            locale="au",
        )
        print()
        
  
    # Take shared guest screenshots
    if shared_guest:
        print(f"📸 Shared Guest Screenshots: {len(shared_guest)} URLs (no authentication)")
        print("=" * 60)
        await take_screenshots_batch(
            urls=shared_guest,
            output_dir="screenshots/prod/desktop/shared/guest",
            viewport_width=1920,
            viewport_height=1080,
            use_auth=False
        )
        print()

    print(f"✨ Done! Screenshots saved to 'screenshots' directory")
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    asyncio.run(main())