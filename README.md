## Facebook Unfollow Tool

This repository contains a small toolkit to **extract your Facebook “Following” list and batch unfollow many accounts** using your browser and a Python script.

- **`batch_unfollow.py`** – Python CLI tool that uses your Facebook cookie + JSON list of following accounts to:
  - Unfollow **one** account (single mode), or
  - Unfollow **many** accounts from a JSON file (batch mode, multi‑threaded).
- **`fb_following_extractor_popup.js`** – Browser script (run in DevTools console) that shows a popup on Facebook, auto‑scrolls the Following page, and **exports your following list to JSON** (including UID) for use with `batch_unfollow.py`.

You can keep these two files at the repository root or, for a cleaner GitHub layout, put them together in a folder, for example:

```text
facebook-unfollow-tool/
  tool/
    batch_unfollow.py
    fb_following_extractor_popup.js
  README.md
  requirements.txt
```

---

## 1. File: `batch_unfollow.py`

### English – What it does

`batch_unfollow.py` is a **terminal-based Facebook unfollow tool**:

- Shows a colored menu with two modes:
  - **Mode 1 – Unfollow a single user**: you paste a profile URL or UID, and it performs the unfollow via the GraphQL API.
  - **Mode 2 – Batch unfollow from JSON**: reads a JSON file (exported by the extractor) and unfollows many accounts with delay + multithreading.
- Asks for:
  - **Debug mode** (on/off): whether to print detailed logs (requests, tokens, responses).
  - **Clear console each step** (yes/no).
  - **Facebook cookie** (copied from browser devtools).
  - For batch mode: JSON file path, delay between requests, and number of threads.
- Automatically:
  - Parses the cookie, extracts `c_user`, `xs`, etc.
  - Fetches **tokens** (`fb_dtsg`, `lsd`) and your own **UID** and **name** from `www.facebook.com`.
  - Unfollows via the `CometUserUnfollowMutation` GraphQL endpoint.
  - Logs everything safely to UTF‑8 text files and a summary JSON.

### English – How to run

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the script:**

   ```bash
   python batch_unfollow.py
   ```

3. **Choose options in the menu:**

   - Answer whether to enable **debug mode** (`y`/`n`).
   - Answer whether to **clear the console** between steps (`y`/`n`).
   - Choose:
     - `1` – Unfollow a single user.
     - `2` – Batch unfollow from a JSON file.

4. **Paste your Facebook cookie** when asked.

   - Open Facebook in a browser → `F12` → **Application** tab → **Cookies** → `facebook.com`.
   - Copy the complete cookie string (including `c_user`, `xs`, `fr`, `datr`, `sb`, …).

5. **Single unfollow (mode 1):**

   - Enter a **profile URL** or **UID** when prompted.
   - The script will:
     - Fetch your tokens,
     - Call the GraphQL API,
     - Print success/failure and save a log file `unfollow_single_log_YYYY-MM-DD_HH-MM-SS.txt`.

6. **Batch unfollow (mode 2):**

   - When asked for the **JSON file**, either:
     - Paste a path to the JSON exported by `fb_following_extractor_popup.js`, or
     - Press **Enter** to auto-pick the newest `facebook_following_*.json` in the current folder.
   - Choose:
     - **Delay** (seconds between requests, default 2s).
     - **Number of threads** (1–10, default 5).
   - The tool will:
     - Show a colored progress and detailed logs (if debug enabled),
     - Save a full text log `unfollow_log_*.txt`,
     - Save a structured result JSON `unfollow_results_*.json` containing success/failed/skipped items.

> **Note:** Names may show as `Unknown` sometimes; this is intentional to avoid accidentally using internal telemetry keys like `latency_level` or `connection_quality`. Unfollow logic still works because it uses UID + tokens, not the name.

---

### Tiếng Việt – Công dụng

`batch_unfollow.py` là một **tool hủy theo dõi Facebook chạy trong terminal**:

- Hiển thị menu màu với 2 chế độ:
  - **Chế độ 1 – Hủy theo dõi 1 người**: bạn dán URL profile hoặc UID, tool gọi API GraphQL để hủy theo dõi.
  - **Chế độ 2 – Hủy theo dõi theo file JSON (batch)**: đọc file JSON (xuất từ script extractor) và hủy theo dõi nhiều người, có delay + đa luồng.
- Tool sẽ:
  - Hỏi **debug mode** (bật/tắt log chi tiết).
  - Hỏi có **clear màn hình** giữa các bước hay không.
  - Hỏi **cookie Facebook** (copy từ DevTools).
  - Với batch: hỏi đường dẫn **file JSON**, **delay**, **số luồng**.
- Tự động:
  - Parse cookie, lấy `c_user`, `xs`, v.v.
  - Lấy **tokens** (`fb_dtsg`, `lsd`) và **UID + tên** của bạn từ `www.facebook.com`.
  - Gọi API GraphQL `CometUserUnfollowMutation` để hủy theo dõi.
  - Ghi log đầy đủ, an toàn Unicode, vào file `.txt` và `.json`.

### Tiếng Việt – Cách chạy

1. **Cài thư viện Python:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Chạy script:**

   ```bash
   python batch_unfollow.py
   ```

3. **Chọn tùy chọn trong menu:**

   - Trả lời có bật **debug mode** hay không (`y`/`n`).
   - Trả lời có muốn **clear màn hình** giữa các bước hay không (`y`/`n`).
   - Chọn:
     - `1` – Hủy theo dõi 1 người.
     - `2` – Hủy theo dõi theo file JSON (batch).

4. **Dán cookie Facebook** khi được hỏi.

   - Vào Facebook → nhấn `F12` → tab **Application** → **Cookies** → `facebook.com`.
   - Copy toàn bộ chuỗi cookie (bao gồm `c_user`, `xs`, `fr`, `datr`, `sb`, …).

5. **Hủy theo dõi 1 người (chế độ 1):**

   - Nhập **URL profile** hoặc **UID**.
   - Tool sẽ:
     - Lấy token,
     - Gửi request GraphQL,
     - In kết quả **thành công / thất bại** và lưu log `unfollow_single_log_YYYY-MM-DD_HH-MM-SS.txt`.

6. **Hủy theo dõi theo file (chế độ 2 – batch):**

   - Khi hỏi **đường dẫn file JSON**:
     - Dán đường dẫn tới file JSON được xuất từ `fb_following_extractor_popup.js`, hoặc
     - Nhấn **Enter** để tool tự chọn file mới nhất dạng `facebook_following_*.json` trong thư mục hiện tại.
   - Chọn:
     - **Delay** (số giây giữa các request, mặc định 2 giây).
     - **Số luồng** (1–10, mặc định 5).
   - Tool sẽ:
     - Hiển thị tiến trình có màu, log chi tiết nếu bật debug,
     - Lưu log text `unfollow_log_*.txt`,
     - Lưu file kết quả JSON `unfollow_results_*.json` với danh sách success / failed / skipped.

> **Lưu ý:** Đôi khi tên sẽ hiện `Unknown` – đây là chủ ý để tránh lụm nhầm mấy key kỹ thuật như `latency_level`, `connection_quality`. Logic hủy theo dõi vẫn chạy bình thường vì dùng UID + token, không phụ thuộc tên.

---

## 2. File: `fb_following_extractor_popup.js`

### English – What it does

`fb_following_extractor_popup.js` is a **browser-side extractor** that:

- Injects a modern popup UI into the **Facebook Following** page.
- Auto-scrolls the page to **load all following entries**.
- Extracts for each account:
  - `name`
  - `profileUrl`
  - `username` (if any)
  - `uid` (if directly visible)
  - `avatar` URL
  - `description` (small text description if found)
- Shows a live table with avatars, names, usernames, UIDs, links.
- Allows:
  - **“Get UID”**: tries to resolve missing UIDs using multiple fetches and patterns.
  - **“Export Data”**: downloads a JSON file `facebook_following_YYYY-MM-DD_HH-mm-SS.json` and also copies the JSON to clipboard when possible.

This JSON is the input for `batch_unfollow.py` in batch mode.

### English – How to use in browser

1. **Open your Following list**:
   - Go to your Facebook profile.
   - Open the “Following” / “People you follow” page (the list of people you are following).

2. **Open DevTools Console**:

   - Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Opt+I` (macOS).
   - Go to the **Console** tab.

3. **Paste the entire `fb_following_extractor_popup.js` code** into the Console and press Enter.

4. A popup titled **“📋 Facebook Following Extractor”** will appear:

   - Click **“🔄 Lấy Data”** to:
     - Auto-scroll the page,
     - Collect all visible following items that look like real user profiles.
   - After data is loaded:
     - Table shows index, avatar, name, username, UID, and link.
     - The header shows stats: total, with UID, without UID, etc.

5. **(Optional) Resolve missing UIDs**:

   - If some items have username but no UID, click **“🆔 Lấy UID”**.
   - The script will:
     - Use up to 5 concurrent “workers” with retries to fetch profile pages,
     - Try many regex patterns to find a numeric UID,
     - Update the table with newly found UIDs.

6. **Export data to JSON**:

   - Click **“💾 Xuất Data”**.
   - The script will:
     - Trigger a download of `facebook_following_YYYY-MM-DD_HH-mm-SS.json`,
     - Try to copy the same JSON to your clipboard,
     - Log the JSON to the browser console.
   - This JSON file should be copied to the same folder as `batch_unfollow.py` and used as input for batch unfollow.

---

### Tiếng Việt – Công dụng

`fb_following_extractor_popup.js` là **script chạy trong trình duyệt** để:

- Chèn một popup đẹp vào trang **Following** của Facebook.
- Tự động scroll để **load hết danh sách những người bạn đang theo dõi**.
- Trích xuất cho mỗi người:
  - `name` – tên hiển thị.
  - `profileUrl` – link profile.
  - `username` – nếu có.
  - `uid` – nếu lấy được trực tiếp.
  - `avatar` – link ảnh đại diện.
  - `description` – mô tả ngắn nếu tìm được.
- Hiển thị bảng với avatar, tên, username, UID, link.
- Cho phép:
  - **“🆔 Lấy UID”** – cố gắng lấy UID cho những người chỉ có username.
  - **“💾 Xuất Data”** – xuất file JSON `facebook_following_YYYY-MM-DD_HH-mm-SS.json` và copy JSON vào clipboard (nếu trình duyệt cho phép).

File JSON này là **input cho `batch_unfollow.py`** (chế độ batch).

### Tiếng Việt – Cách dùng trong trình duyệt

1. **Mở trang Following**:

   - Vào Facebook, mở trang **“Đang theo dõi” / “Following”** trong profile của bạn (danh sách những người bạn đang theo dõi).

2. **Mở DevTools Console**:

   - Nhấn `F12` hoặc `Ctrl+Shift+I` (Windows) / `Cmd+Opt+I` (macOS).
   - Chuyển sang tab **Console**.

3. **Dán toàn bộ nội dung file `fb_following_extractor_popup.js`** vào Console rồi Enter.

4. Popup **“📋 Facebook Following Extractor”** sẽ xuất hiện:

   - Nhấn **“🔄 Lấy Data”**:
     - Script sẽ tự scroll xuống để load hết danh sách.
     - Lọc ra các item có vẻ là **profile người dùng thật** (bỏ map, places, pages…).
   - Sau khi xong:
     - Bảng sẽ hiện STT, avatar, tên, username, UID, link.
     - Phần trên hiển thị thống kê: tổng, bao nhiêu có UID, bao nhiêu chưa có UID, v.v.

5. **(Tuỳ chọn) Lấy UID cho các dòng chưa có UID**:

   - Nếu có người chỉ có username mà chưa có UID, nhấn **“🆔 Lấy UID”**.
   - Script sẽ:
     - Dùng tối đa 5 luồng song song + retry để fetch profile,
     - Dùng nhiều pattern regex khác nhau để tìm UID dạng số,
     - Cập nhật bảng với UID mới lấy được.

6. **Xuất dữ liệu ra JSON**:

   - Nhấn **“💾 Xuất Data”**.
   - Script sẽ:
     - Tải file `facebook_following_YYYY-MM-DD_HH-mm-SS.json` về máy,
     - Thử copy JSON vào clipboard,
     - In JSON ra console của trình duyệt.
   - Hãy copy file JSON này vào cùng thư mục với `batch_unfollow.py` để dùng cho chế độ batch.

---

## 3. Recommended folder layout for GitHub

For a clean GitHub repo, you can arrange files like this:

```text
facebook-unfollow-tool/
  tool/
    batch_unfollow.py
    fb_following_extractor_popup.js
  requirements.txt
  README.md
```

The current repository already contains `batch_unfollow.py`, `fb_following_extractor_popup.js`, `requirements.txt`, and this `README.md`.  
You can simply create a `tool/` folder and move the two main files there before pushing to GitHub if you want them grouped.


