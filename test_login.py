import pytest
from playwright.async_api import async_playwright, expect

BASE_URL = "https://playwright-demo.eventos.work/web/portal/529/event/3988/users/login"

VALID_EMAIL = "kimtran@bravesoft.com.vn"        
VALID_PASSWORD = "brave0404"            

INVALID_EMAIL_1 = "abc@gmail"
INVALID_EMAIL_2 = "abc!@gmail.com"
INVALID_EMAIL_3 = "test.abc"
INVALID_EMAIL_4 = "@gmail.com"

UNREGISTERED_EMAIL = "not_exist@gmail.com"
WRONG_PASSWORD = "wrongpass"
SHORT_PASSWORD = "1234567"
LONG_PASSWORD = "a" * 33


# ====== COMMON FUNCTION ======
async def open_browser():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True, slow_mo=300)
    page = await browser.new_page()
    await page.goto(BASE_URL)
    return p, browser, page
    

# ====== TEST CASES ======

@pytest.mark.asyncio
async def test_01_ui_display():
    """画面表示確認"""
    p, browser, page = await open_browser()
    await expect(page.locator("input[type='email']")).to_be_visible()
    await expect(page.locator("input[type='password']")).to_be_visible()
    await browser.close()
    await p.stop()



@pytest.mark.asyncio
async def test_02_email_invalid_format():
    """メール形式不正チェック"""
    p, browser, page = await open_browser()

    email = page.locator("input[type='email']")

    # abc@gmail
    await email.fill(INVALID_EMAIL_1)
    await page.click("text=ログイン")
    await expect(page.locator("text=メールアドレスが正しくありません")).to_be_visible()

    # abc!@gmail.com
    await email.fill(INVALID_EMAIL_2)
    await page.click("text=ログイン")
    await expect(page.locator("text=メールアドレスが正しくありません")).to_be_visible()

    # test.abc
    await email.fill(INVALID_EMAIL_3)
    await page.click("text=ログイン")
    await expect(page.locator("text=メールアドレスが正しくありません")).to_be_visible()

    # @gmail.com
    await email.fill(INVALID_EMAIL_4)
    await page.click("text=ログイン")
    await expect(page.locator("text=メールアドレスが正しくありません")).to_be_visible()


    # 全角文字入力
    await email.fill("あいう１２３@gmail.com")
    await page.click("text=ログイン")
    await expect(page.locator("text=メールアドレスが正しくありません")).to_be_visible()
    await browser.close()
    await p.stop()

   

@pytest.mark.asyncio
async def test_03_email_empty():
    """メール未入力"""
    p, browser, page = await open_browser()

    await page.fill("input[type='email']", "")
    await page.click("text=ログイン")
    await expect(page.locator("text=メールアドレスを入力してください")).to_be_visible()
    await browser.close()
    await p.stop()

   


@pytest.mark.asyncio
async def test_04_password_visibility_toggle():
    """パスワード表示・非表示の挙動確認"""
    p, browser, page = await open_browser()

    password_input = page.locator("input[type='password']")
    test_password = "Password123"
    toggle_icon = page.locator("button[aria-label='append icon']")
    await toggle_icon.wait_for()
    
   
    # 初期状態：マスク（非アクティブ）
    input_type = await password_input.get_attribute("type")
    assert input_type == "password"

    #  文字入力と入力できること
    await password_input.fill(test_password)
    value = await password_input.input_value()
    assert value == test_password

    # マスク表示（*****）
    input_type = await password_input.get_attribute("type")
    assert input_type == "password"

    # 目アイコン押下とマスク解除（表示状態）
    await toggle_icon.click()
    input_type = await password_input.get_attribute("type")
    assert input_type == "text"

    # もう一度押下と再びマスク表示
    await toggle_icon.click()
    input_type = await password_input.get_attribute("type")
    assert input_type == "password"
    await browser.close()
    await p.stop()

    


@pytest.mark.asyncio
async def test_05_password_short():
    """パスワード桁数不足"""
    p, browser, page = await open_browser()

    await page.fill("input[type='email']", VALID_EMAIL)
    await page.fill("input[type='password']", SHORT_PASSWORD)
    await page.click("text=ログイン")

    await expect(page.locator("text=パスワードは8文字以上32文字以下で指定してください")).to_be_visible()
    await browser.close()
    await p.stop()

  

   
@pytest.mark.asyncio
async def test_06_password_long():
    """パスワード桁数長い"""
    p, browser, page = await open_browser()
    
    await page.fill("input[type='email']", VALID_EMAIL)
    await page.fill("input[type='password']", LONG_PASSWORD)
    await page.click("text=ログイン")

    await expect(page.locator("text=パスワードは8文字以上32文字以下で指定してください")).to_be_visible()
    await browser.close()
    await p.stop()




@pytest.mark.asyncio
async def test_07_login_wrong_password():
    """正しいメール + 間違ったパスワード"""
    p, browser, page = await open_browser()

    await page.fill("input[type='email']", VALID_EMAIL)
    await page.fill("input[type='password']", WRONG_PASSWORD)
    await page.click("text=ログイン")
   
    await expect(page.locator("text=ログインできませんでした")).to_be_visible()
    await browser.close()
    await p.stop()




@pytest.mark.asyncio
async def test_08_login_unregistered_email():
    """未登録メール + 正しいパスワード"""
    p, browser, page = await open_browser()

    await page.fill("input[type='email']", UNREGISTERED_EMAIL)
    await page.fill("input[type='password']", VALID_PASSWORD)
    await page.click("text=ログイン")

    await expect(page.locator("text=ログインできませんでした")).to_be_visible()
    await browser.close()
    await p.stop()


@pytest.mark.asyncio
async def test_09_login_success():
    """正常ログイン"""
    p, browser, page = await open_browser()

    await page.fill("input[type='email']", VALID_EMAIL)
    await page.fill("input[type='password']", VALID_PASSWORD)
    await page.click("text=ログイン")
    await expect(page).not_to_have_url(BASE_URL)
    await browser.close()
    await p.stop()

   
@pytest.mark.asyncio
async def test_10_register_button_visible():
    """新規登録ボタン表示確認"""
    p, browser, page = await open_browser()

    register_button = page.locator("text=新規登録")

    # ボタンが表示されること
    await expect(register_button).to_be_visible()
    await browser.close()
    await p.stop()
   

@pytest.mark.asyncio
async def test_11_register_navigation():
    """新規登録ボタン表示確認"""
    p, browser, page = await open_browser()

    register_button = page.locator("text=新規登録")

    # 新規登録画面遷移確認
    await register_button.click()
    await expect(page).not_to_have_url(BASE_URL)
    await browser.close()
    await p.stop()

