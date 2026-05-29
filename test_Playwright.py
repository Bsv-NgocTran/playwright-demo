
from playwright.sync_api import Page, expect
import pytest
import os

@pytest.fixture
def base_page(page: Page):
 page.goto("https://bsv-nhungnguyen.github.io/")
 page.wait_for_load_state("networkidle")
 return page


# =====================================================
# FRAMES & IFRAMES
# =====================================================

def test_frm_001(base_page: Page):
 # Iframe đơn
 frame = base_page.frame_locator("iframe").nth(0)
 frame.locator('input[type="text"]').fill("Ngoc")
 frame.locator("#iframe-submit-btn").click()
 expect(frame.get_by_text("Success: Hello Ngoc!")).to_be_visible()


def test_frm_002(base_page: Page):
 # Iframe A

 base_page.get_by_role("button",name="Load Nested Frames (A → B → C)").click()
 frame = base_page.frame_locator("iframe").nth(1)
 expect(frame.get_by_text("Iframe A")).to_be_visible()
 expect(frame.get_by_role("button",name="Click button")).to_be_visible()
 expect(frame.get_by_role("button",name="Open Iframe B")).to_be_visible()


def test_frm_003(base_page: Page):
 # Iframe B

 base_page.get_by_role("button",name="Load Nested Frames (A → B → C)").click()
 frame = base_page.frame_locator("iframe").nth(1)
 frame.get_by_role("button",name="Open Iframe B").click()
 iframe_b = frame.frame_locator("iframe").first
 expect(iframe_b.get_by_text("Iframe B")).to_be_visible()
 expect(iframe_b.get_by_role("button",name="Click button")).to_be_visible()
 expect(iframe_b.get_by_role("button",name="Open Iframe C")).to_be_visible()


def test_frm_004(base_page: Page):
 # Iframe C

 base_page.get_by_role("button",name="Load Nested Frames (A → B → C)").click()
 frame = base_page.frame_locator("iframe").nth(1)
 frame.get_by_role("button",name="Open Iframe B").click()
 iframe_b = frame.frame_locator("iframe").first
 iframe_b.get_by_role("button",name="Open Iframe C").click()
 iframe_c = iframe_b.frame_locator("iframe").first
 expect(iframe_c.get_by_text("Iframe C")).to_be_visible()
 expect(iframe_c.get_by_role("button",name="Click button")).to_be_visible()


def test_frm_005(base_page: Page):
 # Click button trong iframe C

 base_page.get_by_role("button",name="Load Nested Frames (A → B → C)").click()
 frame = base_page.frame_locator("iframe").nth(1)
 frame.get_by_role("button",name="Open Iframe B").click()
 iframe_b = frame.frame_locator("iframe").first
 iframe_b.get_by_role("button",name="Open Iframe C").click()
 iframe_c = iframe_b.frame_locator("iframe").first
 iframe_c.get_by_role("button",name="Click button").click()
 expect(iframe_c.get_by_text("Iframe C Clicked!")).to_be_visible()


# =====================================================
# WINDOWS / POPUP / MODAL
# =====================================================

def test_win_001(base_page: Page):
 # Open new tab

 with base_page.expect_popup() as new_tab:
  base_page.locator("#btn-new-tab").click()
 child_page = new_tab.value
 child_page.wait_for_load_state()
 child_page.locator(".getStarted_Sjon").click()
 expect(child_page.get_by_role("heading", name="Installation")).to_be_visible(timeout=15000)


def test_popup_001(base_page: Page):
 # Popup window

 with base_page.expect_popup() as popup:
  base_page.get_by_role("button",name="Open Popup Window").click()
 popup_page = popup.value
 expect(popup_page.get_by_text("Popup Activated")).to_be_visible()


def test_modal_001(base_page: Page):
 # Open modal

 base_page.get_by_role("button",name="Open In-page Modal").click()
 expect(base_page.get_by_text("Secure Confirmation")).to_be_visible()


def test_modal_002(base_page: Page):
 # Confirm modal

 base_page.get_by_role("button", name="Open In-page Modal").click()
 base_page.locator("#modal-input").fill("Playwright")
 base_page.locator("#modal-confirm-btn").click()
 expect(base_page.locator("#modal-result")).to_have_text("✓ Verified: Playwright")


def test_modal_003(base_page: Page):
 # Cancel modal
 base_page.get_by_role("button", name="Open In-page Modal").click()
 base_page.locator("#modal-input").fill("Playwright")
 base_page.get_by_role("button", name="Cancel").click()
 expect(base_page.locator("#modal-overlay")).not_to_contain_text("Playwright")


# =====================================================
# ALERT / CONFIRM / PROMPT
# =====================================================

def test_alert_001(base_page: Page):

    def handle_dialog(dialog):
     assert "This is a browser alert!" in dialog.message
     dialog.accept()

    base_page.once("dialog", handle_dialog)
    base_page.locator("#btn-alert").click()


def test_alert_002(base_page: Page):
 # Accept alert

 def handle_alert(dialog):
  dialog.accept()

 base_page.on("dialog", handle_alert)
 base_page.get_by_role("button",name="Trigger Alert").click()


def test_confirm_001(base_page: Page):
 # Trigger confirm
  def handle_dialog(dialog):
     assert "Continue?" in dialog.message
     dialog.accept()

  base_page.on("dialog", handle_dialog)
  base_page.locator("#btn-confirm").click()
  



def test_confirm_002(base_page: Page):
 # Confirm OK

 def handle_confirm(dialog):
  dialog.accept()

 base_page.on("dialog", handle_confirm)
 base_page.locator("#btn-confirm").click()
 expect(base_page.locator("#confirm-result")).to_have_text("✓ Confirmed")


def test_confirm_003(base_page: Page):
 # Confirm cancel

 def handle_confirm(dialog):
  dialog.dismiss()
 base_page.on("dialog", handle_confirm)
 base_page.locator("#btn-confirm").click()
 expect(base_page.locator("#confirm-result")).to_have_text("✗ Cancelled")


def test_prompt_001(base_page: Page):
 # Prompt OK

 def handle_prompt(dialog):dialog.accept("Playwright")
 base_page.on("dialog", handle_prompt)
 base_page.get_by_role("button",name="Trigger Prompt").click()
 expect(base_page.locator("#prompt-result")).to_have_text("Name: Playwright")


def test_prompt_002(base_page: Page):
 # Prompt cancel

 def handle_prompt(dialog):dialog.dismiss()
 base_page.on("dialog", handle_prompt)
 base_page.get_by_role("button",name="Trigger Prompt").click()
 expect(base_page.locator("#prompt-result")).to_have_text("Dismissed")


# =====================================================
# SCREENSHOT
# =====================================================

def test_screenshot_001(base_page: Page):
 # Full page screenshot

 base_page.get_by_role("button",name="Normal State").click()
 expect(base_page.get_by_text("System Normal")).to_be_visible()
 base_page.screenshot(path="screenshots/fullpage.png",full_page=True)
 assert os.path.exists("screenshots/fullpage.png")


def test_screenshot_002(base_page: Page):
 # Element screenshot failed only
 base_page.get_by_role("button", name="Failure State").click()
 expect(base_page.locator("body")).to_contain_text("Failure")

# =====================================================
# VIDEO 
# =====================================================
def test_video_001(base_page: Page):
 # Record video in ALL cases (PASS)
 base_page.get_by_role("button", name="▶ Play Sequence").click()
 expect(base_page.get_by_text("Sequence complete!")).to_be_visible(timeout=15000)


def test_video_002(base_page: Page):
 #Video ONLY on failure (PASS case → NO video saved)
 base_page.get_by_role("button", name="▶ Play Sequence").click()
 expect(base_page.get_by_text("Sequence complete!")).to_be_visible(timeout=10000)


# =====================================================
# TRACING 
# =====================================================
def test_trace_001(base_page: Page):
 #Trace in ALL cases (PASS)
 base_page.locator("#trace-name").fill("Tracing")
 base_page.locator("#trace-email").fill("Submission")
 base_page.get_by_role("button", name="Submit Form").click()
 expect(base_page.get_by_text("✓ Submitted: tracing")).to_be_visible(timeout=15000)


def test_trace_002(base_page: Page):
 #Trace ONLY on failure (PASS case → NO trace saved)
 base_page.get_by_role("button", name="Submit Form").click()
 expect(base_page.get_by_text("Both fields are required")).to_be_visible(timeout=5000)


# =====================================================
# HOOK TESTS 
# =====================================================
def test_hook_001(base_page: Page):
 # BEFORE EACH
 base_page.locator("#hk-username").fill("admin")
 base_page.locator("#hk-password").fill("password123")
 base_page.get_by_role("button", name="Login").click()
 base_page.locator("#hk-record-name").fill("Test Record")
 base_page.locator("#hk-btn-create").click()
 expect(base_page.locator("#hk-create-msg")).to_contain_text("created")

def test_hook_002(base_page: Page):
 # AFTER EACH
 base_page.locator("#hk-username").fill("admin")
 base_page.locator("#hk-password").fill("password123")
 base_page.get_by_role("button", name="Login").click()

 base_page.locator("#hk-record-name").fill("Test Record")
 base_page.locator("#hk-btn-create").click()
 base_page.locator("#hk-btn-delete-1").click()
 expect(base_page.locator("#hk-delete-msg")).to_contain_text("deleted")

@pytest.fixture(scope="session", autouse=True)
def hooks_session():
 print("[beforeAll] Setup môi trường test")
 print("Artifacts sẽ được lưu tại: ./artifacts")
 yield
 print("[afterAll] Kết thúc test session - dọn dẹp môi trường")


