import http
import re
from playwright.sync_api import Page, expect
import pytest


@pytest.fixture
def logged_page(page: Page):
 page.goto("https://admin.odakyu.bravesoft.vn/login")
 page.locator('input[name="email"]').fill("kimtran@bravesoft.com.vn")
 page.locator('input[name="password"]').fill("brave0404")
 page.locator('button[type="submit"]').click()
 page.wait_for_load_state("networkidle")
 page.locator(".loading-overlay").first.wait_for(state="hidden", timeout=15000)
 page.wait_for_timeout(500)
 return page


def test_create_account_screen_01(logged_page: Page):
 #  画面タイトル
 logged_page.get_by_role("button",name="新規追加").click()
 expect(logged_page.get_by_text("新規アカウント追加")).to_be_visible()

def test_create_account_screen_02(logged_page: Page):
 #  URL
 logged_page.get_by_role("button",name="新規追加").click()
 expect(logged_page).to_have_url("https://admin.odakyu.bravesoft.vn/account-management")



def test_create_account_screen_03(logged_page: Page):
 #  アカウント名のタイトル
 logged_page.get_by_role("button",name="新規追加").click()
 expect(logged_page.locator(".label-title").filter(has_text=("アカウント名"))).to_have_text("アカウント名 * （255文字以内）")
 

def test_create_account_screen_04(logged_page: Page):
 #  アカウント名の入力
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.locator('input[name="userName"]').click()
 logged_page.locator('input[name="userName"]').fill("ngoctran")
 expect(logged_page.locator('input[name="userName"]')).to_have_value("ngoctran")

def test_create_account_screen_05(logged_page: Page):
 #  メールアドレスのタイトル
 logged_page.get_by_role("button",name="新規追加").click()
 expect(logged_page.locator(".label-title").filter(has_text=("メールアドレス"))).to_have_text("メールアドレス *")

def test_create_account_screen_06(logged_page: Page):
 #  メールアドレスの入力
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.locator('input[name="email"]').click()
 logged_page.locator('input[name="email"]').fill("ngoctran@bravesoft.com.vn")
 expect(logged_page.locator('input[name="email"]')).to_have_value("ngoctran@bravesoft.com.vn")

def test_create_account_screen_07(logged_page: Page):
 #  パスワードのタイトル
 logged_page.get_by_role("button",name="新規追加").click()
 expect(logged_page.locator(".label-title").filter(has_text="パスワード")).to_have_text("パスワード *（半角英数字 8文字以上32文字以内）")

def test_create_account_screen_08(logged_page: Page):
 #  パスワードのplaceholder
 logged_page.get_by_role("button",name="新規追加").click()
 expect(logged_page.get_by_placeholder("**********")).to_be_visible()

def test_create_account_screen_09(logged_page: Page):
 #  パスワードの入力
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.locator('input[name="password"]').click()
 logged_page.locator('input[name="password"]').fill("ngoctran@123")
 expect(logged_page.locator('input[name="password"]')).to_have_attribute('type',"password")

def test_create_account_screen_10(logged_page: Page):
  #  権限セレクトボックスの表示
 logged_page.get_by_role("button",name="新規追加").click()
 expect(logged_page.get_by_role("combobox").nth(0)).to_be_visible()
 expect(logged_page.get_by_role("combobox").nth(0)).to_have_attribute("aria-expanded","false")

def test_create_account_screen_11(logged_page: Page):
  #  マスター管理者を選択する
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.get_by_role("combobox").nth(1).click()
 logged_page.get_by_role("option", name="マスター管理者").click()
 expect(logged_page.locator('.multiselect-single-label').nth(1)).to_have_text("マスター管理者")

def test_create_account_screen_12(logged_page: Page):
  #  テナント管理者チケットを選択する
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.get_by_role("combobox").nth(1).click()
 logged_page.get_by_role("option", name="テナント管理者").click()
 expect(logged_page.locator('.multiselect-single-label').nth(1)).to_have_text("テナント管理者")

def test_create_account_screen_13(logged_page: Page):
  #  マスター管理者とテナント管理者チケットを同時選択できない
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.get_by_role("combobox").nth(1).click()
 logged_page.get_by_role("option", name="マスター管理者").click()
 expect(logged_page.locator('.multiselect-single-label').nth(1)).to_have_text("マスター管理者")
 
 logged_page.get_by_role("combobox").nth(1).click()
 logged_page.get_by_role("option", name="テナント管理者").click()
 expect(logged_page.locator('.multiselect-single-label').nth(1)).to_have_text("テナント管理者")

def test_create_account_screen_14(logged_page: Page):
  #  チケット組成時のポイント付与パラメータの変更権限の表示 
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.get_by_role("combobox").nth(1).click()
 logged_page.get_by_role("option", name="テナント管理者").click()
 expect(logged_page.get_by_text("有")).to_be_visible()
 expect(logged_page.get_by_text("無")).to_be_visible()
 
def test_create_account_screen_15(logged_page: Page):
  #  「有」を選択する
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.get_by_role("combobox").nth(1).click()
 logged_page.get_by_role("option", name="テナント管理者").click()
 logged_page.locator('#authority1').check()
 expect(logged_page.locator('#authority1')).to_be_checked()

def test_create_account_screen_16(logged_page: Page):
  #  「無」を選択する
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.get_by_role("combobox").nth(1).click()
 logged_page.get_by_role("option", name="テナント管理者").click()
 logged_page.locator('#authority2').check()
 expect(logged_page.locator('#authority2')).to_be_checked()

def test_create_account_screen_17(logged_page: Page):
  #  「有」と「無」を同時選択できない
 logged_page.get_by_role("button",name="新規追加").click()
 logged_page.get_by_role("combobox").nth(1).click()
 logged_page.get_by_role("option", name="テナント管理者").click()
 logged_page.locator('#authority1').check()
 expect(logged_page.locator('#authority1')).to_be_checked()

 logged_page.locator('#authority2').check()
 expect(logged_page.locator('#authority2')).to_be_checked()



