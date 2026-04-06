SimpleWebTest

使用 Playwright + pytest 對 SauceDemo
 進行自動化 UI 測試專案。

主要目標：

驗證登入功能與購物車功能的正確性
支援功能測試、回歸測試、冒煙測試

專案結構
SimpleWebTest/
├── tests/
│   ├── test_login.py     # 登入功能測試
│   └── test_cart.py      # 購物車功能測試
├── requirements.txt       # Python 套件清單
├── pytest.ini             # pytest 設定（如 marker 定義）
└── README.md
測試範圍

| 檔案              | 測試案例                                          | 說明                                  | 標記(Marker)        |
| --------------- | --------------------------------------------- | ----------------------------------- | ----------------- |
| `test_login.py` | `test_login_success`                          | 正確帳密登入成功                            | functional, smoke |
|                 | `test_login_wrong_password`                   | 錯誤密碼顯示錯誤訊息                          | functional        |
|                 | `test_login_empty_fields`                     | 空白欄位顯示必填提示                          | functional        |
|                 | `test_login_empty_password_only`              | 只填帳號不填密碼顯示提示                        | functional        |
|                 | `test_login_locked_user`                      | 鎖定帳號登入顯示錯誤訊息                        | functional        |
|                 | `test_login_page_has_required_elements`       | 登入頁面 UI 元素存在                        | regression        |
|                 | `test_logout_returns_to_login`                | 登入後登出 → 回到登入頁                       | regression        |
|                 | `test_cannot_access_inventory_without_login`  | 未登入訪問商品頁 → 導回登入頁                    | regression        |
| `test_cart.py`  | `test_add_one_item_to_cart`                   | 加入商品後購物車數量為 1                       | functional, smoke |
|                 | `test_cart_page_shows_one_item`               | 購物車頁面顯示 1 筆商品                       | functional        |
|                 | `test_add_button_changes_to_remove`           | 按鈕文字變為 Remove                       | functional        |
|                 | `test_add_multiple_items`                     | 加入多個商品 → 購物車數量正確                    | functional        |
|                 | `test_remove_item_from_cart`                  | 移除商品 → 購物車徽章消失                      | functional        |
|                 | `test_cart_empty_on_fresh_login`              | 回歸：新登入購物車為空                         | regression        |
|                 | `test_cart_item_has_name_and_price`           | 回歸：購物車商品顯示名稱與價格                     | regression        |
|                 | `test_continue_shopping_returns_to_inventory` | 回歸：購物車頁點「Continue Shopping」 → 回商品列表 | regression        |


安裝與執行
1. 安裝套件
pip install -r requirements.txt
playwright install chromium

2. 執行測試
# 執行全部測試 
pytest

# 無頭模式
pytest --headless

# 只跑登入測試
pytest tests/test_login.py

# 放慢速度方便觀察（毫秒）
pytest --slowmo=500

# 只跑功能測試
pytest -m functional

# 只跑回歸測試
pytest -m regression

# 只跑冒煙測試（最快，核心流程）
pytest -m smoke

3. 標記說明（Markers）
functional → 功能測試：驗證新功能是否符合需求
regression → 回歸測試：改動後確認原功能仍正常
smoke → 冒煙測試：核心流程測試，快速檢查系統是否可用