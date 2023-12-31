# Linebot-IOT
โครงงานนี้ คือโครงพัฒนาระบบ IOT ด้วย LINE Bot และ LINE LIFF ซึ่งช่วยให้ผู้ใช้งานสามารถติดตามสภาพแวดล้อมที่วัดได้จากอุปกรณ์ IOT ของตัวเองได้อย่างง่ายดายและชัดเจนผ่านเว็บไซต์ที่ใช้งานด้วย LINE LIFF และผ่าน LINE Bot

This is an IOT development project with LINE Bot and LINE LIFF.

## How to use
1. สร้าง .env โดยมีตัวแปรดังนี้
   MONGO_INITDB_ROOT_USERNAME=
   MONGO_INITDB_ROOT_PASSWORD=
   MONGO_HOST=mongodb:27017/
   LINE_CHANNEL_SECRET=
   LINE_ACCESS_TOKEN=
   LINE_ADMIN_ID=
   NGROK_TOKEN= //optional
2. ใช้ LINE Official Account ของตัวเอง ให้ใช้ webhook จาก forward port ของ VScode
3. ต้องมี LINE Login channel เป็นของตัวเอง และใช้ webhook เหมือนข้อ 2 ที่ใข้ port เลข 6000
4. รัน demo โดยใช้คำสั่งดังนี้

      `docker compose up -d`
      `npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch`

   โดยใช้คำสั่งในโฟลเดอร์ liff
5. หากต้องการเปลี่ยน url ของ frontend สามารถเปลี่ยได้ที่

      `@app.get("/url/path/")`

   ที่อยู่ในไฟล์ liff/app.py
6. หากต้องการเปลี่ยน backend api link ให้เปลี่ยนที่

      `@app.post("/apt/url/path")`

   ที่อยู่ในไฟล์ iot/app.py แต่ต้องเปลี่ยน

      `request.post("http://iot:8000/api/url/path")`

   ใน liff/app.py เพื่อให้สามารถดึงค่าจากฐานข้อมูล mongodb ได้
7. LINE bot สามารถใช้ webhook จาก forward port ของ VScode ไม่จำเป็นต้องใช้ของ ngrok เสมอไป

## Linebot EnviroNotify
Bot Basic ID: @005wkjpj

<img src="markdown-imgs\qr-code-line-bot.png" alt="Image" width="150" height="150">

---
### สมาชิก (Member)
1. ปุญญ์ฐิสา แตงมั่ง (Punthisa Taengmang) 6110613236
   - LINE Bot
   - Test cases
2. มุนินทร์ วุฒิพงษ์วรกิจ (Munin Wutthipongworakit) 6310682601
   - LINE LIFF
   - Frontend
3. รัญชนา ศุภเสวต (Runchana Supasavate) 6310682650
   - LINE Bot 
4. ณัฐนนท์ บุญเขตต์ (Nattanol Boonyakhet) 6310682726
   - Backend (API)
   - Backend (MQTT)
5. ธัญญวัฒน์ ธนัครสมบัติ (Thunyavat Thanakornsombat) 6310682825
   - Espressif ESP32
   - Fullstack
