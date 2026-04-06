import pytest
from playwright.sync_api import Page, expect

# 測試資料
BASE_URL = "https://www.saucedemo.com"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


# 輔助函式
def login(page: Page):
    """登入並等待進入商品列表頁"""
    page.goto(BASE_URL)
    page.fill("#user-name", VALID_USER)
    page.fill("#password", VALID_PASS)
    page.click("#login-button")
    page.wait_for_url(f"{BASE_URL}/inventory.html")


# 測試案例
class TestCart:

    # ── 功能測試：購物車核心功能 ───────────────────────────────────

    @pytest.mark.functional
    @pytest.mark.smoke
    def test_add_one_item_to_cart(self, page: Page):
        """🛒 加入一個商品 → 購物車圖示應顯示數量 1"""
        login(page)
        page.locator(".btn_inventory").first.click()
        cart_badge = page.locator(".shopping_cart_badge")
        expect(cart_badge).to_be_visible()
        expect(cart_badge).to_have_text("1")

    @pytest.mark.functional
    def test_cart_page_shows_one_item(self, page: Page):
        """🛒 加入一個商品後進入購物車頁 → 應有 1 筆商品"""
        login(page)
        page.locator(".btn_inventory").first.click()
        page.click(".shopping_cart_link")
        page.wait_for_url(f"{BASE_URL}/cart.html")
        expect(page.locator(".cart_item")).to_have_count(1)

    @pytest.mark.functional
    def test_add_button_changes_to_remove(self, page: Page):
        """🛒 加入商品後 → 按鈕文字應變為 Remove"""
        login(page)
        add_btn = page.locator(".btn_inventory").first
        add_btn.click()
        expect(add_btn).to_have_text("Remove")

    @pytest.mark.functional
    def test_add_multiple_items(self, page: Page):
        """🛒 加入兩個不同商品 → 購物車數量應為 2"""
        login(page)
        buttons = page.locator(".btn_inventory")
        buttons.nth(0).click()
        buttons.nth(1).click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("2")

    @pytest.mark.functional
    def test_remove_item_from_cart(self, page: Page):
        """🛒 加入商品後再移除 → 購物車徽章應消失"""
        login(page)
        add_btn = page.locator(".btn_inventory").first
        add_btn.click()
        # 按鈕已變成 Remove，再點一次移除
        add_btn.click()
        expect(page.locator(".shopping_cart_badge")).not_to_be_visible()

    # ── 回歸測試：確保購物車相關行為沒有被改壞 ───────────────────

    @pytest.mark.regression
    def test_cart_empty_on_fresh_login(self, page: Page):
        """回歸：剛登入時購物車應為空（無徽章數字）"""
        login(page)
        expect(page.locator(".shopping_cart_badge")).not_to_be_visible()

    @pytest.mark.regression
    def test_cart_item_has_name_and_price(self, page: Page):
        """回歸：購物車內商品應顯示名稱與價格"""
        login(page)
        page.locator(".btn_inventory").first.click()
        page.click(".shopping_cart_link")
        cart_item = page.locator(".cart_item").first
        expect(cart_item.locator(".inventory_item_name")).to_be_visible()
        expect(cart_item.locator(".inventory_item_price")).to_be_visible()

    @pytest.mark.regression
    def test_continue_shopping_returns_to_inventory(self, page: Page):
        """回歸：在購物車頁點「Continue Shopping」→ 應回到商品列表"""
        login(page)
        page.click(".shopping_cart_link")
        page.wait_for_url(f"{BASE_URL}/cart.html")
        page.click("[data-test='continue-shopping']")
        expect(page).to_have_url(f"{BASE_URL}/inventory.html")