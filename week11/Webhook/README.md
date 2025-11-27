# Demo Webhook cho hệ thống thông báo cơ bản
Mục tiêu: Khi một **sự kiện xảy ra**, Webhook **tự gửi thông báo tới server** và server **hiển thị hoặc gửi thông báo** cho người dùng.

---

## **1. Luồng demo**

```
[Event Trigger] → [Webhook gửi POST] → [Server nhận] → [Xử lý & thông báo]
```

**Chi tiết:**

1.  **Event Trigger**: Ví dụ người dùng tạo đơn hàng mới, gửi message mới, hoặc gửi thử bằng Postman.
2.  **Webhook**: URL của server nhận sự kiện.
3.  **Server nhận webhook**: Xử lý dữ liệu, hiển thị console hoặc gửi thông báo (email / chat / popup).
4.  **Thông báo**: Người dùng biết có sự kiện mới.

---

## **2. Demo bằng Node.js (Express)**

**Bước 1: Tạo server webhook**

```javascript
// server.js
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

// parse JSON body
app.use(bodyParser.json());

// endpoint webhook nhận sự kiện
app.post('/webhook', (req, res) => {
    const event = req.body.event;
    const message = req.body.message;

    console.log('--- Webhook received ---');
    console.log(`Event: ${event}`);
    console.log(`Message: ${message}`);

    // Thông báo cơ bản: console log
    console.log(`🔔 Thông báo: ${message}`);

    res.status(200).send('Webhook received');
});

app.listen(PORT, () => {
    console.log(`Webhook server listening at http://localhost:${PORT}/webhook`);
});
```

---

**Bước 2: Chạy server**

```bash
node server.js
```

---

**Bước 3: Gửi thử sự kiện**

*   Sử dụng **Postman** hoặc **curl**:

```bash
curl -X POST http://localhost:3000/webhook \
-H "Content-Type: application/json" \
-d '{"event": "new_order", "message": "Có đơn hàng mới #1234"}'
```

*   Server sẽ hiển thị:

```
--- Webhook received ---
Event: new_order
Message: Có đơn hàng mới #1234
🔔 Thông báo: Có đơn hàng mới #1234
```

---

## **3. Demo bằng Python Flask**

```python
# webhook.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('event')
    message = data.get('message')

    print('--- Webhook received ---')
    print(f'Event: {event}')
    print(f'Message: {message}')
    print(f'🔔 Thông báo: {message}')

    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

*   Chạy: `python webhook.py`
*   Gửi POST giống Node.js demo.