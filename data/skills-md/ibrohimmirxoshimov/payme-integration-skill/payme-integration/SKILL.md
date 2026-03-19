---
name: payme-integration
description: >
  Payme Business payment gateway integration for Uzbekistan. Use this skill whenever the user mentions
  Payme, Paycom, paycom.uz, payment integration for Uzbekistan, Uzcard/HUMO card payments, Merchant API,
  Subscribe API, Payme checkout, receipts.create, cards.create, CheckPerformTransaction, CreateTransaction,
  PerformTransaction, CancelTransaction, or any payment processing for Uzbek market. Also trigger when
  user asks about integrating card payments in Uzbekistan, building payment forms, handling transactions
  with JSON-RPC 2.0 for payments, or implementing a billing server for Payme. Covers both Merchant API
  (server-to-server, Payme sends requests to merchant) and Subscribe API (merchant sends requests to Payme,
  card tokenization, one-click payments, invoices). Includes payment initialization (checkout forms),
  sandbox testing, fiscalization, hold payments, mobile SDK integration, and error handling.
---

# Payme Business Integration Skill

O'zbekiston bozori uchun Payme Business to'lov tizimi integratsiyasi bo'yicha to'liq qo'llanma.

## Tizim haqida umumiy ma'lumot

Payme Business — Uzcard va HUMO bank kartalari orqali onlayn to'lovlarni qabul qilish tizimi. Pul mablag'lari Payme Business kassalari orqali biznes hisob raqamiga tushadi. Faqat yuridik shaxslar (IP, ChP, OOO, AO, GUP, SP, NOU) ishlashi mumkin.

### 3 turdagi kassa
1. **Billing bilan to'lov qabul qilish kassasi** — Merchant API sozlash talab qilinadi
2. **Billingsiz to'lov qabul qilish kassasi** — Merchant API sozlash talab qilinadi
3. **Joyida to'lov qabul qilish kassasi** — darhol ishlashni boshlash mumkin

### 2 ta asosiy protokol

| Xususiyat | Merchant API | Subscribe API |
|-----------|-------------|---------------|
| So'rovni kim yuboradi | Payme → Merchant | Merchant → Payme |
| Javobni kim qaytaradi | Merchant → Payme | Payme → Merchant |
| Qachon ishlatiladi | Standart Payme to'lov formasi | O'zining to'lov formasi, "bir klik" to'lov, avtoto'lov, invoice |
| Protokol | JSON-RPC 2.0 over HTTPS POST | JSON-RPC 2.0 over HTTPS POST |

**Integratsiya tartibi:**
1. Merchant API va/yoki Subscribe API ni sozlash
2. Sandbox (pesochnitsa)da test qilish
3. To'lovni boshlash (checkout) usulini qo'shish
4. Ishchi serverga ko'chirish

---

## MERCHANT API

### Protokol talablari
- JSON-RPC 2.0, HTTP 1.1 POST, HTTPS (TLS v1/v1.1/v1.2)
- Javoblar doim **HTTP 200** status bilan qaytarilishi shart (boshqa statuslar -32400 xato deb qabul qilinadi)
- Faqat nomlangan parametrlar (named parameters)

### Avtorizatsiya
Payme Business `Authorization` headerida Basic auth yuboradi:
```
Authorization: Basic base64(login:password)
```
- `login` — Payme texnik mutaxassisidan so'rash kerak
- `password` — veb-kassa yaratilgandan keyin beriladigan kalit

### Payme IP manzillari (whitelist uchun)
```
185.234.113.1 — 185.234.113.15
```

### So'rov formati
```json
{
    "method": "PerformTransaction",
    "params": {
        "id": "53327b3fc92af52c0b72b695",
        "time": 1399114284039,
        "amount": 500000,
        "account": { "phone": "903595731" }
    },
    "id": 2032
}
```

### Javob formati

**Muvaffaqiyatli:**
```json
{
    "result": { ... },
    "id": 2032
}
```

**Xatolik:**
```json
{
    "error": {
        "code": -31050,
        "message": {
            "ru": "Номер телефона не найден",
            "uz": "Raqam ro'yhatda yo'q",
            "en": "Phone number not found"
        },
        "data": "phone"
    },
    "id": 2032
}
```

### Merchant API Metodlari

Batafsil ma'lumot: `references/merchant-api-methods.md` faylini o'qing.

**Metodlar ro'yxati:**
1. **CheckPerformTransaction** — tranzaksiya yaratish mumkinligini tekshirish
2. **CreateTransaction** — tranzaksiya yaratish
3. **PerformTransaction** — tranzaksiyani o'tkazish (pul yechish)
4. **CancelTransaction** — tranzaksiyani bekor qilish
5. **CheckTransaction** — tranzaksiya holatini tekshirish
6. **GetStatement** — ma'lum davr uchun tranzaksiyalar ro'yxati
7. **SetFiscalData** — fiskalizatsiya ma'lumotlarini qabul qilish (ixtiyoriy)

### Tranzaksiya holatlari (State)
| Kod | Tavsif |
|-----|--------|
| 1 | Tranzaksiya yaratildi, tasdiqlash kutilmoqda |
| 2 | Tranzaksiya muvaffaqiyatli yakunlandi |
| -1 | Tranzaksiya bekor qilindi (state 1 dan) |
| -2 | Tranzaksiya yakunlangandan keyin bekor qilindi (state 2 dan) |

### Bekor qilish sabablari (Reason)
| Kod | Tavsif |
|-----|--------|
| 1 | Qabul qiluvchi topilmadi yoki faol emas |
| 2 | Debet operatsiyasida xatolik |
| 3 | Tranzaksiya bajarishda xatolik |
| 4 | Timeout bo'yicha bekor qilish (12 soat = 43,200,000 ms) |
| 5 | Pul qaytarish |
| 10 | Noma'lum xatolik |

### Ma'lumot turlari
- **ID** — 24 belgili string (Payme unikal identifikator)
- **Timestamp** — 13 raqamli integer (1970-01-01 UTC dan millisekund)
- **Amount** — musbat integer, tiyinda (1 so'm = 100 tiyin)
- **Account** — JSON obyekt, merchant biznes-logikasiga bog'liq

---

## SUBSCRIBE API

### Endpoint URL
- **Test:** `https://checkout.test.paycom.uz/api`
- **Production:** `https://checkout.paycom.uz/api`

### Avtorizatsiya headeri
| Qayer | Format |
|-------|--------|
| Frontend | `X-Auth: {kassa_id}` |
| Backend | `X-Auth: {kassa_id}:{password}` |

### Karta bilan ishlash metodlari

**Frontend (client-side):**
- `cards.create` — karta tokenini yaratish
- `cards.get_verify_code` — SMS verifikatsiya kodi so'rash
- `cards.verify` — SMS kod bilan kartani tasdiqlash

**Backend (server-side):**
- `cards.check` — karta tokeni tekshirish
- `cards.remove` — karta tokenini o'chirish

### Chek bilan ishlash metodlari (Backend)
- `receipts.create` — to'lov chekini yaratish
- `receipts.pay` — chekni to'lash
- `receipts.send` — invoice (hisob-faktura) yuborish
- `receipts.cancel` — to'langan chekni bekor qilish navbatiga qo'yish
- `receipts.check` — chek statusini tekshirish
- `receipts.get` — chek haqida to'liq ma'lumot
- `receipts.get_all` — ma'lum davr uchun barcha cheklar

Batafsil ma'lumot: `references/subscribe-api-methods.md` faylini o'qing.

### Xavfsizlik talablari
- Karta input formasi elementlarida `name` atributi bo'lmasligi kerak
- `<form>` tegida `action` atributi bo'lmasligi kerak
- Forma Payme logotipi, oferta havolasi va xavfsizlik haqida yozuv o'z ichiga olishi kerak
- **Shifrllanmagan karta ma'lumotlarini saqlash QATTIYAN TAQIQLANADI!**
- Faqat token saqlanadi

### Hold (Xoldirovaniye) to'lovlar
Hold to'lov uchun `receipts.create` va `receipts.pay` da `"hold": true` flagi qo'shiladi.

```json
// receipts.create bilan hold
{
    "method": "receipts.create",
    "params": {
        "account": { "order_id": 106 },
        "amount": 2500,
        "hold": true
    }
}

// receipts.pay bilan hold
{
    "method": "receipts.pay",
    "params": {
        "id": "{{receipt_id}}",
        "token": "{{card_token}}",
        "hold": true
    }
}
```
Hold holati: state = 5

### Test kartalari
| Raqam | Expire | Izoh |
|-------|--------|------|
| 8600 0609 2109 0842 | 03/99 | SMS xabar yo'q |
| 3333 3364 1580 4657 | 03/99 | Muddati o'tgan |
| 4444 4459 8745 9073 | 03/99 | Bloklangan |
| 8600 1434 1777 0323 | 03/99 | Tizim xatosi |
| 8600 1343 0184 9596 | 03/99 | 10 sek kechikish simulyatsiyasi |
| 8600 4954 7331 6478 | 03/99 | Normal |
| 8600 0691 9540 6311 | 03/99 | Normal |

**Barcha test kartalari uchun SMS kod: `666666`**

---

## TO'LOVNI BOSHLASH (CHECKOUT)

### POST usuli
```html
<form method="POST" action="https://checkout.paycom.uz">
    <input type="hidden" name="merchant" value="{Merchant ID}"/>
    <input type="hidden" name="amount" value="{summa tiyinda}"/>
    <input type="hidden" name="account[order_id]" value="{buyurtma_id}"/>
    <input type="hidden" name="lang" value="uz"/>
    <input type="hidden" name="callback" value="{qaytish URL}"/>
    <input type="hidden" name="callback_timeout" value="{millisekund}"/>
    <input type="hidden" name="description" value="{tavsif}"/>
    <input type="hidden" name="detail" value="{BASE64 JSON detalizatsiya}"/>
    <button type="submit">Payme orqali to'lash</button>
</form>
```

**Test URL:** `https://test.paycom.uz`
**Production URL:** `https://checkout.paycom.uz`

### GET usuli
Format: `{checkout_url}/base64(params)`, parametrlar `;` bilan ajratiladi.

| Parametr | Tavsif |
|----------|--------|
| m | Merchant ID yoki alias |
| ac | Account obyekti |
| a | Summa (tiyinda) |
| l | Til (ru/uz/en) |
| c | Qaytish URL |
| ct | Qaytish kutish vaqti (ms) |
| cr | Valyuta kodi (ISO) |

**Misol:**
```
https://checkout.paycom.uz/bT01ODdmNzJjNzJjYWMwZDE2MmM3MjJhZTI7YWMub3JkZXJfaWQ9MTk3O2E9NTAw
```
Bu: `base64("m=587f72c72cac0d162c722ae2;ac.order_id=197;a=500")`

---

## XATOLAR JADVALI

### Umumiy xatolar
| Kod | Tavsif |
|-----|--------|
| -32300 | POST bo'lmagan so'rov metodi |
| -32700 | JSON parsing xatosi |
| -32600 | RPC-so'rovda majburiy maydonlar yo'q |
| -32601 | Metod topilmadi |
| -32504 | Ruxsatlar yetarli emas |
| -32400 | Tizim (ichki) xatosi |

### Merchant xatolari
| Kod | Tavsif |
|-----|--------|
| -31001 | Noto'g'ri summa |
| -31003 | Tranzaksiya topilmadi |
| -31007 | Bekor qilib bo'lmaydi — tovar/xizmat to'liq taqdim etilgan |
| -31008 | Operatsiyani bajarib bo'lmaydi (holat ruxsat bermaydi) |
| -31050 — -31099 | Account noto'g'ri kiritilgan (login/telefon topilmadi va h.k.) |

---

## FISKALIZATSIYA

### CheckPerformTransaction da detail obyekti
```json
{
    "result": {
        "allow": true,
        "detail": {
            "receipt_type": 0,
            "shipping": {
                "title": "Yetkazib berish",
                "price": 500000
            },
            "items": [
                {
                    "discount": 10000,
                    "title": "Pomidor",
                    "price": 505000,
                    "count": 2,
                    "code": "00702001001000001",
                    "units": 241092,
                    "vat_percent": 15,
                    "package_code": "123456"
                }
            ]
        }
    }
}
```

### Items massivi parametrlari
| Maydon | Tur | Tavsif | Majburiy |
|--------|-----|--------|----------|
| title | String | Mahsulot nomi | Ha |
| price | Number | Narx (tiyinda) | Ha |
| count | Number | Miqdor | Ha |
| code | String | IKPU kodi | Ha |
| vat_percent | Number | QQS foizi | Ha |
| package_code | String | Qadoqlash kodi | Ha |
| discount | Number | Chegirma (tiyinda) | Yo'q |
| units | Number | O'lchov birligi kodi | Yo'q |

### SetFiscalData metodi
Payme chek muvaffaqiyatli to'langandan keyin fiskalizatsiya ma'lumotlarini yuboradi:
```json
{
    "method": "SetFiscalData",
    "params": {
        "id": "61396aaed8b87a4c215ae556",
        "type": "PERFORM",
        "fiscal_data": {
            "receipt_id": 121,
            "status_code": 0,
            "message": "accepted",
            "terminal_id": "EP000000000025",
            "fiscal_sign": "800031554082",
            "qr_code_url": "fiscal receipt url",
            "date": "20220706221021"
        }
    }
}
```

---

## SANDBOX (PESOCHNITSA) — TEST MUHITI

### Test kabineti
- **URL:** https://merchant.test.paycom.uz
- **Login:** telefon raqamingiz
- **Parol:** qwerty
- **SMS kod:** 666666

### Test jarayoni — 2 stsenariy:
1. **Tasdiqlanmagan tranzaksiya yaratish va bekor qilish**
   - Noto'g'ri avtorizatsiya testi → -32504
   - Noto'g'ri summa testi → -31001
   - Mavjud bo'lmagan hisob testi → -31050...-31099
   - CheckPerformTransaction → allow: true
   - CreateTransaction → muvaffaqiyat
   - Takroriy CreateTransaction → muvaffaqiyat (idempotent)
   - Yangi tranzaksiya yaratish (hisob "kutilmoqda") → -31008
   - CancelTransaction → muvaffaqiyat

2. **Tranzaksiya yaratish, tasdiqlash va bekor qilish**
   - Yuqoridagi barcha qadamlar + PerformTransaction + CancelTransaction

### Muhim qoidalar:
- CreateTransaction, PerformTransaction, CancelTransaction **2 marta** yuboriladi (idempotent bo'lishi kerak)
- Takroriy so'rovlarga javob birinchi javob bilan bir xil bo'lishi shart

---

## MOBIL INTEGRATSIYA

- **Android SDK:** https://github.com/PaycomUZ/AndroidSDK
- SDK da karta bilan ishlash UI va client-side Subscribe API metodlari tayyor
- Server tomonda receipts.* va cards.check/remove metodlarini amalga oshirish kerak

## SERVER NAMUNALARI
- **PHP:** https://github.com/PaycomUZ/paycom-integration-php-template
- **Java (Kotlin):** https://github.com/PaycomUZ/paycom-integration-java-template

---

## CHEK HOLATLARI

| Kod | Tavsif |
|-----|--------|
| 0 | Chek yaratildi, to'lov kutilmoqda |
| 1 | Birinchi tekshiruv bosqichi |
| 2 | Kartadan pul yechish |
| 3 | Merchant billingda tranzaksiya yopish |
| 4 | Chek to'landi |
| 5 | Chek xoldirovka qilindi (hold) |
| 6 | Xoldirovaniye jarayonida |
| 20 | Qo'lda boshqarish uchun pauza |
| 21 | Bekor qilish navbatida |
| 30 | Billing yopish navbatida |
| 50 | Chek bekor qilindi |

---

## NODE.JS/TYPESCRIPT UCHUN IMPLEMENTATION GUIDE

Batafsil ma'lumot: `references/node-implementation.md` faylini o'qing.

### Umumiy arxitektura (Node.js)

Merchant API serverini yaratishda quyidagi tuzilmaga amal qiling:

```
src/
├── payme/
│   ├── PaymeController.ts    — HTTP endpoint, auth tekshirish, method routing
│   ├── PaymeService.ts       — Biznes logika (CheckPerform, Create, Perform, Cancel, Check, GetStatement)
│   ├── PaymeError.ts         — Xatolar klassi (code, message, data)
│   ├── types.ts              — PaymeRequest, PaymeResponse, Transaction interfeyslari
│   └── constants.ts          — Xato kodlari, Payme IP lar, timeout qiymatlari
├── models/
│   └── PaymeTransaction.ts   — DB model (id, payme_id, state, amount, account, timestamps)
└── routes/
    └── payme.ts              — Express/Fastify route
```

### Muhim tekshiruvlar
1. **Auth:** `Authorization` headeridan login:password ajratib, KEY bilan solishtirish
2. **IP whitelist:** 185.234.113.1-15 dan kelgan so'rovlarnigina qabul qilish
3. **HTTP method:** Faqat POST, boshqasiga -32300
4. **JSON parsing:** Xato bo'lsa -32700
5. **Majburiy maydonlar:** method, params, id mavjudligini tekshirish, yo'q bo'lsa -32600
6. **Method routing:** method nomiga qarab tegishli handler chaqirish, topilmasa -32601

### Summani tiyinga aylantirish
```
1 so'm = 100 tiyin
500 so'm = 50000 tiyin (amount: 50000)
```

---

## TEZKOR REFERENS

### Muhim URL lar
| Muhit | URL |
|-------|-----|
| Docs | https://developer.help.paycom.uz |
| Test checkout | https://test.paycom.uz |
| Prod checkout | https://checkout.paycom.uz |
| Subscribe test | https://checkout.test.paycom.uz/api |
| Subscribe prod | https://checkout.paycom.uz/api |
| Merchant kabinet | https://merchant.paycom.uz |
| Test kabinet | https://merchant.test.paycom.uz |

### Talablar eslatmasi
- "Powered by Payme" logotipi qo'shish (Subscribe API foydalanuvchilari uchun)
- Payme oferta havolasi: https://cdn.payme.uz/terms/main.html
- Karta ma'lumotlarini **hech qachon** ochiq saqlash mumkin emas — faqat token!
