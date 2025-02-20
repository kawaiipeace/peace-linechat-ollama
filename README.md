# PEA Open AI Chatbot Stack (Local Implementation Edition)

> PEA Open AI Chatbot Stack สร้างขึ้นโดยทีม PEA-AI ภายใต้ MIT License สามารถนำไปพัฒนาและต่อยอดได้อย่างไร้ขีดจำกัด

## เครื่องมือที่ใช้ (Technology Stack)
- Frontend ChatUI by **Open WebUI**.
- Backend AI Model System by **OLLAMA**.
- Local Tunneling (Deploy to website) by **NGROK**.
- Reverse Proxy by **NGINX**.
- Integration with Social Network (**LINE**).

## สิ่งที่จำเป็นก่อนเริ่ม (Prerequisite)
- Docker Engine หรือ Software Container เช่น [Rancher](https://rancherdesktop.io/) (แนะนำ) หรือ Docker Desktop (ถ้าใช้เน็ตเครือข่ายของ PEA ห้ามใช้ตัวนี้เด็ดขาด) [เหตุผลห้ามใช้](https://docs.docker.com/subscription/desktop-license/)
- บัญชี Line Official Account (ที่เปิดการใช้งาน Messaging API) [วิธีการสมัคร](https://www.admeadme.co/blog/line/how-to-create-a-line-official-account/
)
- บัญชี NGROK [สมัครที่นี่](https://dashboard.ngrok.com/signup)
- กรณีที่เครื่องมีการ์ดจอของ NVIDIA ให้ติดตั้งไดรเวอร์ของ NVIDIA [เวอร์ชั่นล่าสุด](https://www.nvidia.com/en-us/drivers/)

## วิธีการติดตั้งและเริ่มใช้งาน (Installation)
1. เปลี่ยนชื่อไฟล์ .env.example ให้เป็น .env และเพิ่ม Key Token ดังนี้
- CHANNEL_ACCESS_TOKEN หาได้จาก [ที่นี่](https://developers.line.biz/console) ในแท็บ Basic settings
- CHANNEL_SECRET หาได้จาก [ที่นี่](https://developers.line.biz/console) ในแท็บ Messaging API
- NGROK_AUTHTOKEN หาได้จาก [ที่นี่](https://dashboard.ngrok.com/get-started/your-authtoken)

2. เปิดโปรแกรม Powershell (หรือ Terminal) และให้ทำการรัน Services ทั้งหมดโดยใช้คำสั่ง
```bash
docker compose up -d --build
```
*หรือหากคอมพิวเตอร์มีการ์ดจอ NVIDIA ให้ใช้คำสั่ง*
```bash
docker compose -f docker-compose-gpu.yaml up -d --build
```

3. ทดสอบโดยการเปิดลิงก์บน Web Browser
```bash
localhost
localhost:11434 หรือ localhost/ollama/
localhost:8000 หรือ localhost/line-chat/
```

4. ให้ทำการติดตั้ง AI Model จาก [ลิงก์นี้](http://localhost:8080/admin/settings) ในแท็บ Model สำหรับ AI Model ที่แนะนำให้ติดตั้งมีดังนี้
```bash
llama3.2
deepseek-r1
mistral
```

5. ระหว่างรอติดตั้งจากข้อ 4 ให้ทำการคัดลอก URL Endpoints ของ NGROK หาได้จาก [ที่นี่](https://dashboard.ngrok.com/endpoints?sortBy=updatedAt&orderBy=desc)

6. ให้ติ๊ก Use webhook และทำการเพิ่ม Webhook URL จาก [ลิงก์นี้](https://developers.line.biz/console) ในแท็บ Messaging API โดยเพิ่ม **[URL ที่ได้จาก NGROK]/line-chat/webhook** เสร็จแล้วให้ลองกด Verify หากขึ้น Success แปลว่าสำเร็จ

7. ให้ทดสอบโดยการสนทนากับ AI Bot ผ่าน WebUI ก่อน จากนั้นลองสนทนาผ่าน Line OA

## การหยุดใช้งาน (Stop Services)
เปิดโปรแกรม Powershell (หรือ Terminal) และให้ทำการรัน Services ทั้งหมดโดยใช้คำสั่ง
```bash
docker compose down -v
```