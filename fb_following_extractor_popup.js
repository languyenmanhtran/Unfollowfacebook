// Facebook Following Extractor Popup
// Author: LNMT x KST
// GitHub: https://github.com/languyenmanhtran
// Code JavaScript - Copy và paste vào F12 Console trên trang Facebook Following
// Tạo menu popup nhỏ để trích xuất và hiển thị dữ liệu


(function() {
    // Kiểm tra xem đã có popup chưa
    if (document.getElementById('fbExtractorPopup')) {
        document.getElementById('fbExtractorPopup').remove();
    }

    // Tạo popup container
    const popup = document.createElement('div');
    popup.id = 'fbExtractorPopup';
    popup.innerHTML = `
        <style>
            #fbExtractorPopup {
                position: fixed;
                top: 20px;
                right: 20px;
                width: 400px;
                max-height: 90vh;
                height: auto;
                min-height: 300px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                z-index: 999999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }
            
            #fbExtractorPopup .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            #fbExtractorPopup .header h3 {
                margin: 0;
                font-size: 16px;
                font-weight: 600;
            }
            
            #fbExtractorPopup .close-btn {
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
            }
            
            #fbExtractorPopup .close-btn:hover {
                background: rgba(255,255,255,0.3);
            }
            
            #fbExtractorPopup .controls {
                padding: 15px;
                background: #f8f9fa;
                border-bottom: 1px solid #e9ecef;
                display: flex;
                gap: 10px;
            }
            
            #fbExtractorPopup .btn {
                flex: 1;
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }
            
            #fbExtractorPopup .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            #fbExtractorPopup .btn-primary:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            }
            
            #fbExtractorPopup .btn-secondary {
                background: #6c757d;
                color: white;
            }
            
            #fbExtractorPopup .btn-secondary:hover {
                background: #5a6268;
            }
            
            #fbExtractorPopup .btn-info {
                background: #17a2b8;
                color: white;
            }
            
            #fbExtractorPopup .btn-info:hover {
                background: #138496;
            }
            
            #fbExtractorPopup .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            #fbExtractorPopup .content {
                flex: 1;
                overflow-y: auto;
                overflow-x: hidden;
                padding: 15px;
                max-height: calc(90vh - 180px);
                min-height: 200px;
            }
            
            #fbExtractorPopup .content::-webkit-scrollbar {
                width: 8px;
            }
            
            #fbExtractorPopup .content::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 10px;
            }
            
            #fbExtractorPopup .content::-webkit-scrollbar-thumb {
                background: #888;
                border-radius: 10px;
            }
            
            #fbExtractorPopup .content::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
            
            #fbExtractorPopup .stats {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                flex-wrap: wrap;
            }
            
            #fbExtractorPopup .stat-item {
                flex: 1;
                min-width: 80px;
                text-align: center;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 8px;
            }
            
            #fbExtractorPopup .stat-number {
                font-size: 20px;
                font-weight: bold;
                color: #667eea;
            }
            
            #fbExtractorPopup .stat-label {
                font-size: 11px;
                color: #6c757d;
                margin-top: 5px;
            }
            
            #fbExtractorPopup .table-container {
                overflow-x: auto;
                overflow-y: visible;
                max-height: none;
            }
            
            #fbExtractorPopup .table-container::-webkit-scrollbar {
                height: 6px;
            }
            
            #fbExtractorPopup .table-container::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 10px;
            }
            
            #fbExtractorPopup .table-container::-webkit-scrollbar-thumb {
                background: #888;
                border-radius: 10px;
            }
            
            #fbExtractorPopup .table-container::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
            
            #fbExtractorPopup table {
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
            }
            
            #fbExtractorPopup th {
                background: #f8f9fa;
                padding: 8px;
                text-align: left;
                font-weight: 600;
                font-size: 11px;
                color: #495057;
                border-bottom: 2px solid #dee2e6;
            }
            
            #fbExtractorPopup td {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
            
            #fbExtractorPopup tr:hover {
                background: #f8f9fa;
            }
            
            #fbExtractorPopup .avatar {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                object-fit: cover;
            }
            
            #fbExtractorPopup .avatar-placeholder {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: #e9ecef;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
            }
            
            #fbExtractorPopup .name {
                font-weight: 600;
                color: #212529;
                font-size: 12px;
            }
            
            #fbExtractorPopup .username {
                color: #667eea;
                font-size: 11px;
                font-weight: 500;
            }
            
            #fbExtractorPopup .uid {
                color: #6c757d;
                font-size: 10px;
                font-family: monospace;
            }
            
            #fbExtractorPopup .link {
                color: #667eea;
                text-decoration: none;
                font-size: 11px;
            }
            
            #fbExtractorPopup .link:hover {
                text-decoration: underline;
            }
            
            #fbExtractorPopup .description {
                color: #6c757d;
                font-size: 11px;
                font-style: italic;
                max-width: 200px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            
            #fbExtractorPopup .badge {
                display: inline-block;
                padding: 2px 6px;
                border-radius: 10px;
                font-size: 9px;
                font-weight: 600;
            }
            
            #fbExtractorPopup .badge-uid {
                background: #e3f2fd;
                color: #1976d2;
            }
            
            #fbExtractorPopup .badge-username {
                background: #f3e5f5;
                color: #7b1fa2;
            }
            
            #fbExtractorPopup .empty-state {
                text-align: center;
                padding: 40px 20px;
                color: #6c757d;
            }
            
            #fbExtractorPopup .empty-state-icon {
                font-size: 48px;
                margin-bottom: 10px;
            }
            
            #fbExtractorPopup .alert {
                padding: 10px 15px;
                margin-bottom: 15px;
                border-radius: 8px;
                font-size: 12px;
            }
            
            #fbExtractorPopup .alert-info {
                background: #d1ecf1;
                color: #0c5460;
                border-left: 4px solid #0c5460;
            }
            
            #fbExtractorPopup .alert-success {
                background: #d4edda;
                color: #155724;
                border-left: 4px solid #155724;
            }
            
            #fbExtractorPopup .alert-warning {
                background: #fff3cd;
                color: #856404;
                border-left: 4px solid #856404;
            }
            
            #fbExtractorPopup table tbody tr {
                opacity: 0;
                transform: translateY(15px);
                animation: fadeInUp 0.5s ease-out forwards;
            }
            
            @keyframes fadeInUp {
                0% {
                    opacity: 0;
                    transform: translateY(15px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            #fbExtractorPopup .loading-scroll {
                text-align: center;
                padding: 20px;
                color: #667eea;
            }
            
            #fbExtractorPopup .loading-scroll .spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(102, 126, 234, 0.3);
                border-radius: 50%;
                border-top-color: #667eea;
                animation: spin 1s ease-in-out infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
        <div class="header">
            <h3>📋 Facebook Following Extractor</h3>
            <button class="close-btn" id="closeBtn">×</button>
        </div>
        <div class="controls">
            <button class="btn btn-primary" id="extractBtn">🔄 Lấy Data</button>
            <button class="btn btn-info" id="getUidBtn" disabled>🆔 Lấy UID</button>
            <button class="btn btn-secondary" id="exportBtn" disabled>💾 Xuất Data</button>
        </div>
        <div class="content" id="popupContent">
            <div class="empty-state">
                <div class="empty-state-icon">👆</div>
                <div>Nhấn nút "Lấy Data" để bắt đầu</div>
            </div>
        </div>
    `;
    
    document.body.appendChild(popup);
    
    // Thêm event listeners (tránh CSP violation)
    const closeBtn = popup.querySelector('#closeBtn');
    const extractBtn = popup.querySelector('#extractBtn');
    const exportBtn = popup.querySelector('#exportBtn');
    
    closeBtn.addEventListener('click', function() {
        popup.remove();
    });
    
    let extractedData = [];
    
    // Hàm tự động scroll để load tất cả danh sách
    async function autoScrollToLoadAll() {
        return new Promise((resolve) => {
            const content = popup.querySelector('#popupContent');
            content.innerHTML = `
                <div class="loading-scroll">
                    <div class="spinner"></div>
                    <div style="margin-top: 10px; font-size: 13px;">Đang scroll để load tất cả danh sách...</div>
                </div>
            `;
            
            let lastHeight = 0;
            let scrollAttempts = 0;
            const maxAttempts = 50; // Tối đa 50 lần scroll
            let noChangeCount = 0;
            
            const scrollInterval = setInterval(() => {
                // Scroll xuống cuối trang
                window.scrollTo(0, document.body.scrollHeight);
                
                // Đợi một chút để content load
                setTimeout(() => {
                    const currentHeight = document.body.scrollHeight;
                    
                    if (currentHeight === lastHeight) {
                        noChangeCount++;
                        // Nếu không thay đổi 3 lần liên tiếp thì dừng
                        if (noChangeCount >= 3) {
                            clearInterval(scrollInterval);
                            resolve();
                            return;
                        }
                    } else {
                        noChangeCount = 0;
                        lastHeight = currentHeight;
                    }
                    
                    scrollAttempts++;
                    if (scrollAttempts >= maxAttempts) {
                        clearInterval(scrollInterval);
                        resolve();
                    }
                }, 500); // Đợi 500ms mỗi lần scroll
            }, 800); // Scroll mỗi 800ms
        });
    }
    
    // Hàm trích xuất dữ liệu
    async function extractData() {
        const content = popup.querySelector('#popupContent');
        const extractBtnEl = popup.querySelector('#extractBtn');
        const exportBtnEl = popup.querySelector('#exportBtn');
        
        extractBtnEl.disabled = true;
        extractBtnEl.textContent = '⏳ Đang scroll...';
        
        try {
            // Bước 1: Auto scroll để load tất cả
            await autoScrollToLoadAll();
            
            extractBtnEl.textContent = '⏳ Đang lấy data...';
            
            // Bước 2: Tìm tất cả các container chứa thông tin user
            const containers = document.querySelectorAll('div.x6s0dn4.x1obq294.x5a5i1n.xde0f50');
            
            const results = [];
            const seenUrls = new Set(); // Để tránh trùng lặp
            
            containers.forEach((container, index) => {
                try {
                    // Lấy link profile
                    const profileLink = container.querySelector('a[href*="facebook.com"]');
                    const profileUrl = profileLink ? profileLink.getAttribute('href') : null;
                    
                    // Bỏ qua nếu không có URL
                    if (!profileUrl) return;
                    
                    // LOẠI BỎ các link không phải profile user:
                    // - Link đến /map (check-in)
                    // - Link đến /places_recent (địa điểm)
                    // - Link đến /pages/ (trang)
                    // - Link đến các tab khác như /photos, /videos, etc.
                    const urlLower = profileUrl.toLowerCase();
                    if (urlLower.includes('/map') || 
                        urlLower.includes('/places_recent') ||
                        urlLower.includes('/places') ||
                        urlLower.includes('/pages/') ||
                        urlLower.includes('/page/') ||
                        urlLower.match(/\/pages\/[^\/]+/) ||
                        urlLower.match(/\/[^\/]+\/(photos|videos|about|friends|groups|map|places|events|reviews)/)) {
                        return; // Bỏ qua địa điểm/check-in/trang
                    }
                    
                    // Kiểm tra xem có phải là profile user không
                    // Profile user: facebook.com/username hoặc facebook.com/profile.php?id=UID
                    // Loại bỏ: facebook.com/username/map, facebook.com/username/photos, etc.
                    const urlPath = profileUrl.split('facebook.com/')[1]?.split('?')[0] || '';
                    const pathParts = urlPath.split('/').filter(p => p);
                    
                    // Nếu có nhiều hơn 1 phần trong path (ví dụ: username/map) thì bỏ qua
                    if (pathParts.length > 1) {
                        // Trừ trường hợp profile.php?id=...
                        if (!urlPath.startsWith('profile.php')) {
                            return; // Không phải profile user đơn giản
                        }
                    }
                    
                    // Kiểm tra phần đầu của path
                    if (pathParts.length > 0) {
                        const firstPart = pathParts[0].toLowerCase();
                        if (firstPart === 'pages' || firstPart === 'page' || firstPart === 'map' || firstPart === 'places') {
                            return; // Không phải user
                        }
                    }
                    
                    // Bỏ qua nếu đã có trong kết quả
                    if (seenUrls.has(profileUrl)) return;
                    seenUrls.add(profileUrl);
                    
                    // Lấy tên
                    const nameElement = container.querySelector('span[dir="auto"]');
                    const name = nameElement ? nameElement.textContent.trim() : null;
                    
                    // Kiểm tra thêm: nếu tên rỗng hoặc không hợp lệ thì bỏ qua
                    if (!name || name.length < 2) return;
                    
                    // Lấy avatar
                    const avatarImg = container.querySelector('img[alt=""]');
                    const avatar = avatarImg ? avatarImg.getAttribute('src') : null;
                    
                    // Lấy mô tả
                    const descriptionElements = container.querySelectorAll('div[dir="auto"]');
                    let description = null;
                    descriptionElements.forEach(el => {
                        const text = el.textContent.trim();
                        if (text && text !== name && !text.includes('More options') && !text.includes('Lựa chọn')) {
                            // Loại bỏ các mô tả của địa điểm như "Đã ghé thăm vào..."
                            if (!text.includes('Đã ghé thăm') && !text.includes('Việt Nam') && !text.match(/^\d+\s+(tháng|ngày)/)) {
                                description = text;
                            }
                        }
                    });
                    
                    // Trích xuất UID từ URL
                    let uid = null;
                    let username = null;
                    if (profileUrl.includes('profile.php?id=')) {
                        uid = profileUrl.match(/id=(\d+)/)?.[1];
                    } else {
                        const urlParts = profileUrl.split('facebook.com/')[1]?.split('/')[0]?.split('?')[0];
                        // Chỉ lấy username nếu không phải là các từ khóa đặc biệt
                        if (urlParts && !urlParts.includes('pages') && !urlParts.includes('map')) {
                            username = urlParts;
                        }
                    }
                    
                    // Chỉ thêm nếu có đủ thông tin cơ bản
                    if (name && profileUrl && (uid || username)) {
                        results.push({
                            index: results.length + 1,
                            name: name,
                            profileUrl: profileUrl,
                            username: username,
                            uid: uid,
                            avatar: avatar,
                            description: description
                        });
                    }
                } catch (e) {
                    console.error(`Lỗi item ${index}:`, e);
                }
            });
            
            if (results.length === 0) {
                content.innerHTML = `
                    <div class="alert alert-warning">
                        ❌ Không tìm thấy dữ liệu. Hãy đảm bảo bạn đang ở trang Following và đã scroll để load tất cả.
                    </div>
                `;
                extractBtnEl.disabled = false;
                extractBtnEl.textContent = '🔄 Lấy Data';
                return;
            }
            
            extractedData = results;
            exportBtnEl.disabled = false;
            
            // Enable nút Lấy UID nếu có item không có UID
            const getUidBtnEl = popup.querySelector('#getUidBtn');
            const itemsWithoutUid = results.filter(item => !item.uid && item.username);
            if (itemsWithoutUid.length > 0) {
                getUidBtnEl.disabled = false;
                getUidBtnEl.textContent = `🆔 Lấy UID (${itemsWithoutUid.length})`;
            } else {
                getUidBtnEl.disabled = true;
                getUidBtnEl.textContent = '🆔 Lấy UID';
            }
            
            // Hiển thị kết quả
            displayResults(results);
            
            extractBtnEl.disabled = false;
            extractBtnEl.textContent = '🔄 Lấy Data';
            
            console.log('✅ Đã trích xuất:', results.length, 'người dùng');
            console.log(JSON.stringify(results, null, 2));
            
        } catch (error) {
            content.innerHTML = `
                <div class="alert alert-warning">
                    ❌ Lỗi: ${error.message}
                </div>
            `;
            const extractBtnEl = popup.querySelector('#extractBtn');
            extractBtnEl.disabled = false;
            extractBtnEl.textContent = '🔄 Lấy Data';
        }
    }
    
    // Hàm hiển thị kết quả
    function displayResults(data) {
        const content = popup.querySelector('#popupContent');
        
        const total = data.length;
        const withUid = data.filter(item => item.uid).length;
        const withoutUid = data.filter(item => !item.uid && item.username).length;
        const withUsername = data.filter(item => item.username).length;
        const withDescription = data.filter(item => item.description).length;
        
        let alertClass = 'alert-success';
        let alertMessage = `✅ Đã lấy ${total} người dùng thành công!`;
        if (withoutUid > 0) {
            alertClass = 'alert-info';
            alertMessage = `✅ Đã lấy ${total} người dùng! ${withoutUid} người chưa có UID. Nhấn nút "Lấy UID" để tự động lấy.`;
        }
        
        let html = `
            <div class="alert ${alertClass}">
                ${alertMessage}
            </div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">${total}</div>
                    <div class="stat-label">Tổng</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${withUid}</div>
                    <div class="stat-label">Có UID</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" style="color: ${withoutUid > 0 ? '#dc3545' : '#28a745'};">${withoutUid}</div>
                    <div class="stat-label">Chưa có UID</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${withUsername}</div>
                    <div class="stat-label">Username</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${withDescription}</div>
                    <div class="stat-label">Mô tả</div>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 35px;">#</th>
                            <th style="width: 40px;">AVT</th>
                            <th>Tên</th>
                            <th>User</th>
                            <th>UID</th>
                            <th>Link</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        data.forEach((item, idx) => {
            const avatarId = `avatar-${idx}`;
            const placeholderId = `placeholder-${idx}`;
            const delay = idx * 50; // Delay 50ms cho mỗi row
            html += `
                <tr style="animation-delay: ${delay}ms;">
                    <td style="text-align: center; color: #6c757d; font-weight: 600; font-size: 11px;">
                        ${idx + 1}
                    </td>
                    <td>
                        ${item.avatar 
                            ? `<img src="${item.avatar}" alt="${item.name}" class="avatar" id="${avatarId}" data-placeholder="${placeholderId}">
                               <div class="avatar-placeholder" id="${placeholderId}" style="display: none;">👤</div>`
                            : '<div class="avatar-placeholder">👤</div>'
                        }
                    </td>
                    <td>
                        <div class="name">${item.name || 'N/A'}</div>
                        ${item.description ? `<div class="description" title="${item.description}">${item.description}</div>` : ''}
                    </td>
                    <td>
                        ${item.username 
                            ? `<span class="username badge badge-username">@${item.username}</span>`
                            : '-'
                        }
                    </td>
                    <td>
                        ${item.uid 
                            ? `<span class="uid badge badge-uid">${item.uid}</span>`
                            : '-'
                        }
                    </td>
                    <td>
                        ${item.profileUrl 
                            ? `<a href="${item.profileUrl}" target="_blank" class="link">🔗</a>`
                            : '-'
                        }
                    </td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        content.innerHTML = html;
        
        // Thêm error handlers cho avatar images
        data.forEach((item, idx) => {
            if (item.avatar) {
                const img = content.querySelector(`#avatar-${idx}`);
                const placeholder = content.querySelector(`#placeholder-${idx}`);
                if (img && placeholder) {
                    img.addEventListener('error', function() {
                        this.style.display = 'none';
                        placeholder.style.display = 'flex';
                    });
                }
            }
        });
    }
    
    // Hàm lấy UID từ username
    async function getUidFromUsername(username) {
        if (!username) return null;
        
        try {
            // Thử nhiều URL
            const urls = [
                `https://www.facebook.com/${username}`,
                `https://web.facebook.com/${username}`,
                `https://m.facebook.com/${username}`
            ];
            
            for (const url of urls) {
                try {
                    const response = await fetch(url, {
                        method: 'GET',
                        credentials: 'include',
                        mode: 'same-origin', // Chỉ fetch từ cùng origin
                        headers: {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
                        }
                    });
                    
                    if (response.ok) {
                        const html = await response.text();
                        
                        // Nhiều patterns để tìm UID
                        const patterns = [
                            /"profile_owner"\s*:\s*\{[^}]*"id"\s*:\s*"(\d+)"/,
                            /"profile_owner":\{"id":"(\d+)"/,
                            /profile_owner.*?"id"\s*:\s*"(\d+)"/,
                            /"userID"\s*:\s*"(\d+)"/,
                            /"USER_ID"\s*:\s*"(\d+)"/,
                            /"actorID"\s*:\s*"(\d+)"/,
                            /"viewerID"\s*:\s*"(\d+)"/,
                            /"actor_id"\s*:\s*"(\d+)"/,
                            /\/profile\.php\?id=(\d+)/,
                            /\/profile\/(\d+)\//,
                            /"entity_id"\s*:\s*"(\d+)"/,
                            /"profile_id"\s*:\s*"(\d+)"/,
                            /profile_id:"(\d+)"/,
                            /"id"\s*:\s*"(\d+)"[^}]*"__typename"\s*:\s*"User"/,
                            /"__typename"\s*:\s*"User"[^}]*"id"\s*:\s*"(\d+)"/,
                            /<meta[^>]*property=["']fb:\/\/profile\/(\d+)["']/,
                            /profileID["']?\s*[:=]\s*["']?(\d+)/,
                            /userID["']?\s*[:=]\s*["']?(\d+)/,
                            /actorID["']?\s*[:=]\s*["']?(\d+)/,
                            /facebook\.com\/profile\.php\?id=(\d+)/,
                            /facebook\.com\/profile\/(\d+)/,
                        ];
                        
                        for (const pattern of patterns) {
                            const match = html.match(pattern);
                            if (match && match[1]) {
                                const uid = match[1];
                                // Validate UID (thường từ 6-19 chữ số)
                                if (uid.length >= 6 && uid.length <= 19 && /^\d+$/.test(uid)) {
                                    return uid;
                                }
                            }
                        }
                        
                        // Tìm trong script tags
                        const scriptMatches = html.match(/<script[^>]*>(.*?)<\/script>/gs);
                        if (scriptMatches) {
                            for (const script of scriptMatches) {
                                for (const pattern of patterns) {
                                    const match = script.match(pattern);
                                    if (match && match[1]) {
                                        const uid = match[1];
                                        if (uid.length >= 6 && uid.length <= 19 && /^\d+$/.test(uid)) {
                                            return uid;
                                        }
                                    }
                                }
                            }
                        }
                    }
                } catch (e) {
                    console.warn(`Lỗi khi fetch ${url}:`, e);
                    continue;
                }
            }
            
            // Thử cách khác: Sử dụng GraphQL API nếu có thể
            try {
                // Lấy fb_dtsg và lsd từ page hiện tại
                const pageHtml = document.documentElement.outerHTML;
                const fbDtsgMatch = pageHtml.match(/name="fb_dtsg"\s+value="([^"]+)"/) || 
                                   pageHtml.match(/"DTSGInitialData"[^}]*"token"\s*:\s*"([^"]+)"/);
                const lsdMatch = pageHtml.match(/name="lsd"\s+value="([^"]+)"/) || 
                               pageHtml.match(/"LSD"[^}]*"token"\s*:\s*"([^"]+)"/);
                
                if (fbDtsgMatch && lsdMatch) {
                    const fbDtsg = fbDtsgMatch[1];
                    const lsd = lsdMatch[1];
                    
                    // Thử query GraphQL
                    const graphqlUrl = 'https://www.facebook.com/api/graphql/';
                    const graphqlPayload = new URLSearchParams({
                        'av': document.cookie.match(/c_user=(\d+)/)?.[1] || '',
                        '__user': document.cookie.match(/c_user=(\d+)/)?.[1] || '',
                        '__a': '1',
                        '__req': '1',
                        'fb_dtsg': fbDtsg,
                        'lsd': lsd,
                        'variables': JSON.stringify({ scale: 1, useDefaultActor: false, id: username }),
                        'doc_id': '25738636172436531'
                    });
                    
                    const graphqlResponse = await fetch(graphqlUrl, {
                        method: 'POST',
                        credentials: 'include',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'x-fb-lsd': lsd,
                        },
                        body: graphqlPayload
                    });
                    
                    if (graphqlResponse.ok) {
                        let responseText = await graphqlResponse.text();
                        if (responseText.startsWith('for (;;);')) {
                            responseText = responseText.substring(9);
                        }
                        
                        try {
                            const jsonData = JSON.parse(responseText);
                            if (jsonData.data && jsonData.data.viewer) {
                                const actor = jsonData.data.viewer.actor;
                                if (actor && actor.id) {
                                    const uid = String(actor.id);
                                    if (uid.length >= 6 && uid.length <= 19 && /^\d+$/.test(uid)) {
                                        return uid;
                                    }
                                }
                            }
                        } catch (e) {
                            // Parse JSON failed, try regex
                            const uidMatch = responseText.match(/"id"\s*:\s*"(\d+)"/);
                            if (uidMatch && uidMatch[1]) {
                                const uid = uidMatch[1];
                                if (uid.length >= 6 && uid.length <= 19 && /^\d+$/.test(uid)) {
                                    return uid;
                                }
                            }
                        }
                    }
                }
            } catch (e) {
                console.warn('Lỗi khi dùng GraphQL API:', e);
            }
            
            return null;
        } catch (error) {
            console.error(`Lỗi khi lấy UID từ username ${username}:`, error);
            return null;
        }
    }
    
    // Hàm lấy UID cho tất cả items không có UID
    async function getAllUids() {
        const getUidBtnEl = popup.querySelector('#getUidBtn');
        const content = popup.querySelector('#popupContent');
        
        if (extractedData.length === 0) {
            alert('Chưa có dữ liệu! Hãy lấy data trước.');
            return;
        }
        
        const itemsWithoutUid = extractedData.filter(item => !item.uid && item.username);
        if (itemsWithoutUid.length === 0) {
            alert('Tất cả items đã có UID!');
            return;
        }
        
        getUidBtnEl.disabled = true;
        getUidBtnEl.textContent = '⏳ Đang lấy UID (5 luồng)...';
        
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
        const CONCURRENCY = 5;
        const MAX_RETRIES = 3;

        // Hiển thị progress
        let progressHtml = `
            <div class="alert alert-info">
                🔍 Đang lấy UID cho ${itemsWithoutUid.length} người dùng (5 luồng, retry tối đa 3 lần)...
            </div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number" id="progressCurrent">0</div>
                    <div class="stat-label">Đã xử lý</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="progressTotal">${itemsWithoutUid.length}</div>
                    <div class="stat-label">Tổng số</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="progressSuccess">0</div>
                    <div class="stat-label">Thành công</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="progressFailed" style="color:#dc3545;">0</div>
                    <div class="stat-label">Thất bại</div>
                </div>
            </div>
            <div style="margin-top: 15px;">
                <div style="background: #e9ecef; border-radius: 10px; height: 20px; overflow: hidden;">
                    <div id="progressBar" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; width: 0%; transition: width 0.3s;"></div>
                </div>
            </div>
            <div style="margin-top: 15px; padding: 10px; background: #f8f9fa; border-radius: 8px; font-size: 12px;">
                <div style="font-weight: 600; margin-bottom: 5px;">Đang xử lý:</div>
                <div id="currentItem" style="color: #667eea; font-weight: 500;">-</div>
            </div>
            <div style="margin-top: 12px; padding: 10px; background: #fff; border-radius: 8px; border: 1px solid #e9ecef; font-size: 12px;">
                <div style="font-weight: 600; margin-bottom: 6px; color:#dc3545;">Danh sách thất bại (tối đa 10):</div>
                <div id="failedList" style="color:#6c757d; font-size: 11px; line-height: 1.4;">(chưa có)</div>
            </div>
        `;
        content.innerHTML = progressHtml;
        
        let successCount = 0;
        let processedCount = 0;
        let failedCount = 0;
        const failedItems = [];

        const updateProgressUI = () => {
            const progressCurrent = content.querySelector('#progressCurrent');
            const progressSuccess = content.querySelector('#progressSuccess');
            const progressFailed = content.querySelector('#progressFailed');
            const progressBar = content.querySelector('#progressBar');
            const failedList = content.querySelector('#failedList');
            if (progressCurrent) progressCurrent.textContent = processedCount;
            if (progressSuccess) progressSuccess.textContent = successCount;
            if (progressFailed) progressFailed.textContent = failedCount;
            if (progressBar) {
                const percent = (processedCount / itemsWithoutUid.length) * 100;
                progressBar.style.width = percent + '%';
            }
            if (failedList) {
                if (failedItems.length === 0) {
                    failedList.textContent = '(chưa có)';
                } else {
                    failedList.innerHTML = failedItems
                        .slice(-10)
                        .map(it => `- ${it.name} (@${it.username})`)
                        .join('<br>');
                }
            }
        };

        // Queue (shared) cho các worker
        const queue = itemsWithoutUid.slice(); // copy

        const processOneItem = async (item) => {
            const currentItem = content.querySelector('#currentItem');
            if (currentItem) currentItem.textContent = `${item.name} (@${item.username})`;

            let uid = null;
            for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
                try {
                    uid = await getUidFromUsername(item.username);
                    if (uid) break;
                } catch (e) {
                    // ignore, will retry
                }
                // backoff nhỏ, coi như "luồng đó dừng lại" để thử lại
                const backoffMs = 600 * attempt + Math.floor(Math.random() * 250);
                await sleep(backoffMs);
            }

            processedCount++;
            if (uid) {
                item.uid = uid;
                successCount++;
                console.log(`✅ Lấy được UID cho ${item.name} (${item.username}): ${uid}`);
            } else {
                failedCount++;
                failedItems.push({ name: item.name, username: item.username });
                console.warn(`❌ Thất bại (sau ${MAX_RETRIES} lần) UID cho ${item.name} (${item.username})`);
            }

            updateProgressUI();

            // delay nhỏ sau mỗi item để giảm rate-limit (mỗi worker tự delay)
            await sleep(300 + Math.floor(Math.random() * 250));
        };

        const worker = async (workerId) => {
            while (queue.length > 0) {
                const item = queue.shift();
                if (!item) return;
                await processOneItem(item);
            }
        };
        
        // Chạy worker pool
        updateProgressUI();
        const workers = Array.from({ length: CONCURRENCY }, (_, i) => worker(i + 1));
        await Promise.all(workers);
        
        // Cập nhật lại extractedData
        extractedData = [...extractedData];
        
        // Hiển thị kết quả
        displayResults(extractedData);
        
        // Cập nhật nút
        const remaining = extractedData.filter(item => !item.uid && item.username).length;
        if (remaining > 0) {
            getUidBtnEl.disabled = false;
            getUidBtnEl.textContent = `🆔 Lấy UID (${remaining})`;
        } else {
            getUidBtnEl.disabled = true;
            getUidBtnEl.textContent = '🆔 Lấy UID';
        }
        
        // Thông báo kết quả
        const alertDiv = document.createElement('div');
        alertDiv.className = failedCount > 0 ? 'alert alert-warning' : 'alert alert-success';
        alertDiv.style.marginTop = '15px';
        alertDiv.textContent = `✅ Thành công: ${successCount}/${itemsWithoutUid.length} | ❌ Thất bại: ${failedCount}`;
        content.insertBefore(alertDiv, content.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
    
    // Hàm xuất dữ liệu
    function exportData() {
        if (extractedData.length === 0) {
            alert('Chưa có dữ liệu để xuất!');
            return;
        }
        
        const jsonString = JSON.stringify(extractedData, null, 2);
        const now = new Date();
        const pad = (n) => String(n).padStart(2, '0');
        const filename = `facebook_following_${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}_${pad(now.getHours())}-${pad(now.getMinutes())}-${pad(now.getSeconds())}.json`;

        // 1) LƯU FILE (tải về máy)
        try {
            const blob = new Blob([jsonString], { type: 'application/json;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        } catch (e) {
            console.warn('Không thể tải file:', e);
        }
        
        // 2) Copy vào clipboard (nếu được)
        if (navigator.clipboard) {
            navigator.clipboard.writeText(jsonString).then(() => {
                alert(`✅ Đã lưu file: ${filename}\n✅ Đã copy ${extractedData.length} người dùng vào clipboard!`);
            }).catch(() => {
                // Fallback: hiển thị trong prompt
                alert(`✅ Đã lưu file: ${filename}\n⚠️ Không copy được clipboard, bạn copy thủ công trong prompt.`);
                prompt('Copy JSON này:', jsonString);
            });
        } else {
            alert(`✅ Đã lưu file: ${filename}\n⚠️ Trình duyệt không hỗ trợ clipboard, bạn copy thủ công trong prompt.`);
            prompt('Copy JSON này:', jsonString);
        }
        
        // Log ra console
        console.log('='.repeat(80));
        console.log('DỮ LIỆU JSON:');
        console.log('='.repeat(80));
        console.log(jsonString);
    }
    
    // Thêm event listeners cho các nút
    const getUidBtn = popup.querySelector('#getUidBtn');
    extractBtn.addEventListener('click', extractData);
    getUidBtn.addEventListener('click', getAllUids);
    exportBtn.addEventListener('click', exportData);
    
    console.log('✅ Facebook Following Extractor đã sẵn sàng!');
    console.log('💡 Nhấn nút "Lấy Data" trong popup để bắt đầu.');
})();


