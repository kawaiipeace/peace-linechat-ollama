# PEA Open AI Chatbot Stack (Local Implementation Edition)

## เครื่องมือที่ใช้ (Technology Stack)
- Frontend ChatUI by **Open WebUI**.
- Backend AI Model System by **OLLAMA**.
- Local Tunneling (Deploy to website) by **NGROK**.
- Reverse Proxy by **NGINX**.
- Integration with Social Network (**LINE**).

## สิ่งที่จำเป็นก่อนเริ่ม (Prerequisite)
- Docker Engine หรือ Software Container เช่น Rancher (แนะนำ) หรือ Docker Desktop (ถ้าใช้เน็ตเครือข่ายของ PEA ห้ามใช้ตัวนี้เด็ดขาด)
- Line Official Account (ที่เปิดการใช้งาน Messaging API)
- กรณีที่เครื่องมีการ์ดจอของ NVIDIA ให้ติดตั้งไดรเวอร์ของ NVIDIA เวอร์ชั่นล่าสุด

## วิธีการติดตั้งใช้งาน (Installation)
1. เปลี่ยนชื่อไฟล์ .env.example ให้เป็น .env และโดยที่ TOKEN
- CHANNEL_ACCESS_TOKEN หาได้จาก [ที่นี่](https://developers.line.biz/console)
- CHANNEL_SECRET หาได้จาก [ที่นี่](https://developers.line.biz/console)
- NGROK_AUTHTOKEN หาได้จาก [ที่นี่](https://dashboard.ngrok.com/get-started/your-authtoken)
2. 
2. Open the Terminal (or Powershell) and START all services
```bash
docker compose up -d --build
```
3. If you want to STOP all services, input this command.
```bash
docker compose down -v
```