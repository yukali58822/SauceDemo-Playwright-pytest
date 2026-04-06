import pytest
from playwright.sync_api import Page, expect

# 測試資料
BASE_URL = "https://www.saucedemo.com"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


# 輔助函式
def go_to_login(page: Page):
    """開啟登入頁面"""
    page.goto(BASE_URL)


def do_login(page: Page, username: str, password: str):
    """填寫帳密並按登入"""
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


# 測試案例
class TestLogin:

    @pytest.mark.functional
    @pytest.mark.smoke
    def test_login_success(self, page: Page):
        """正確帳密 → 應成功進入商品列表頁"""
        go_to_login(page)
        do_login(page, VALID_USER, VALID_PASS)
        expect(page).to_have_url(f"{BASE_URL}/inventory.html")
        expect(page.locator(".title")).to_have_text("products") # 檢查整個元素的文字 完全等於 "Products"

    @pytest.mark.functional
    def test_login_wrong_password(self, page: Page):
        """密碼錯誤 → 應顯示錯誤訊息"""
        go_to_login(page)
        do_login(page, VALID_USER, "wrong_password")
        error_msg = page.locator("[data-test='error']") # 透過 CSS selector 去定位具有 data-test="error" 的元素
        expect(error_msg).to_be_visible() # 確認錯誤訊息「有出現在畫面上」
        expect(error_msg).to_contain_text("Username and password do not match") # 確認錯誤訊息包含文字內容，但不一定完全相等

    @pytest.mark.functional
    def test_login_empty_fields(self, page: Page):
        """空白帳密 → 應顯示必填錯誤訊息"""
        go_to_login(page)
        do_login(page, "", "")
        error_msg = page.locator("[data-test='error']")
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text("Username is required")

    @pytest.mark.functional
    def test_login_empty_password_only(self, page: Page):
        """只填帳號、不填密碼 → 應顯示密碼必填錯誤"""
        go_to_login(page)
        do_login(page, VALID_USER, "")
        error_msg = page.locator("[data-test='error']")
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text("Password is required")

    @pytest.mark.functional
    def test_login_locked_user(self, page: Page):
        """鎖定帳號登入 → 應顯示帳號被鎖定的錯誤訊息"""
        go_to_login(page)
        do_login(page, "locked_out_user", VALID_PASS)
        error_msg = page.locator("[data-test='error']")
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text("Sorry, this user has been locked out")

    # ── 回歸測試：確保登入後的基本狀態沒有被改壞 ─────────────────

    @pytest.mark.regression
    def test_login_page_has_required_elements(self, page: Page):
        """回歸：登入頁面的 UI 元素都存在（帳號欄、密碼欄、按鈕）"""
        go_to_login(page)
        expect(page.locator("#user-name")).to_be_visible()
        expect(page.locator("#password")).to_be_visible()
        expect(page.locator("#login-button")).to_be_visible()

    @pytest.mark.regression
    def test_logout_returns_to_login(self, page: Page):
        """回歸：登入後執行登出 → 應回到登入頁"""
        go_to_login(page)
        do_login(page, VALID_USER, VALID_PASS)
        # 開選單 → 點登出
        page.click("#react-burger-menu-btn")
        page.click("#logout_sidebar_link")
        expect(page).to_have_url(BASE_URL + "/")
        expect(page.locator("#login-button")).to_be_visible()

    @pytest.mark.regression
    def test_cannot_access_inventory_without_login(self, page: Page):
        """回歸：未登入直接訪問商品頁 → 應被導回登入頁"""
        page.goto(f"{BASE_URL}/inventory.html")
        expect(page).to_have_url(BASE_URL + "/")
        expect(page.locator("[data-test='error']")).to_contain_text(
            "You can only access"
        )