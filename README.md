<div align="center">

# ⚡️ **aioprotonmail** ⚡️

### 🚀 **Blazing Fast** • 🔐 **Secure** • 🛠️ **Developer Friendly** • 🌊 **Fully Async**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Async](https://img.shields.io/badge/Async-aiohttp-green.svg)](https://aiohttp.readthedocs.io)
[![ProtonMail](https://img.shields.io/badge/ProtonMail-API-purple.svg)](https://proton.me)  
[![Speed](https://img.shields.io/badge/Speed-⚡️Lightning-yellow.svg)](#)
[![Encryption](https://img.shields.io/badge/Encryption-🔒E2E-red.svg)](#)
[![Status](https://img.shields.io/badge/Status-🔥Production%20Ready-orange.svg)](#)

---

### **🎯 What's New in Async Version:**
- ⚡️ **Lightning Fast**: Full async/await support with aiohttp
- 🔄 **Auto Token Refresh**: Never worry about expired tokens again  
- 🎨 **Backward Compatible**: Same API as sync version, just add `await`
- 🛠️ **Easy Migration**: Simple `async with` context manager
- 🔧 **One-Line Config**: Use `configure_tokens()` for instant setup

</div>

---

## 🎭 **What This Beast Can Do**

This unofficial ProtonMail API client lets you:
- 📧 **Send & receive** encrypted messages  
- 📎 **Download & upload** attachments
- 🎨 **Render HTML** emails with embedded images
- 🔍 **Search & filter** your mailbox
- 🏷️ **Manage labels** and conversations
- 💾 **Save sessions** for seamless re-authentication
- 🎯 **Event polling** for real-time updates

> ⚠️ **Migration Notice**: This forked library is now **fully async**! All network operations require `async with` and `await`. If you're upgrading from the sync version, check the migration guide below.

## Installation
``` 
pip install git+https://github.com/Muno459/aioprotonmail.git
```

## Basic Usage

### Login and Read Messages
```python
import asyncio
from protonmail import ProtonMail

username = "YouAddress@proton.me"
password = "YourPassword123"

async def main():
    async with ProtonMail() as proton:
        await proton.login(username, password)
        # Get a list of all messages
        messages = await proton.get_messages()
        # Read the latest message
        message = await proton.read_message(messages[0])
        print(message.sender.address)  # sender address
        print(message.subject)  # subject
        print(message.body)
        # <html><body><div>it's my image: <img src="cid:1234@proton.me">....

        # Render the template, images downloading, converting to BASE64 and insert into html
        await proton.render(message)
        # This is a ready-made html page, with all the pictures, you can save it right away
        with open('message.html', 'w', encoding='utf-8') as f:
            f.write(message.body)
        print(message.body)
        # <html><body><div>it's my image: <img src="data:image/png;base64, iVBORw0K..">....

        # Download file from message
        first_file = message.attachments[0]
        await proton.download_files([first_file])
        with open(f'{first_file.name}', 'wb') as f:
            f.write(first_file.content)

asyncio.run(main())
```

### Send Messages
```python
import asyncio
from protonmail import ProtonMail

async def main():
    async with ProtonMail() as proton:
        await proton.login(username, password)
        
        # Create attachments
        with open('image.png', 'rb') as f:
            img = f.read()
        with open('resume.pdf', 'rb') as f:
            pdf = f.read()

        img_attachment = proton.create_attachment(content=img, name='image.png')
        pdf_attachment = proton.create_attachment(content=pdf, name='resume.pdf')

        html = f"""
        <html>
            <body>
                <h2>Hi, I'm a python developer, here's my photo:</h2>
                <img {img_attachment.get_embedded_attrs()} height="150" width="300">
                <br/>
                Look at my resume, it is attached to the letter.
            </body>
        </html>
        """

        new_message = proton.create_message(
            recipients=["to1@proton.me", "to2@gmail.com", "Name of recipient <to3@outlook.com>"],
            cc=["cc1@proton.me", "cc2@gmail.com", "Name of recipient <cc3@outlook.com>"],
            bcc=["bcc1@proton.me", "bcc2@gmail.com", "Name of recipient <bcc3@outlook.com>"],
            subject="My first message",
            body=html,  # html or just text
            attachments=[img_attachment, pdf_attachment],
            external_id="some-message-id-header-if-you-want-to-specify",
            in_reply_to="message-id-of-the-mail-to-reply-to",
        )

        sent_message = await proton.send_message(new_message)

        # Wait for new message
        new_message = await proton.wait_for_new_message(interval=1, timeout=60, rise_timeout=False, read_message=True)
        if 'spam' in new_message.body:
            # Delete spam
            await proton.delete_messages([new_message])

        # Save session, you do not have to re-enter your login, password, pgp key, passphrase
        # WARNING: the file contains sensitive data, do not share it with anyone,
        # otherwise someone will gain access to your mail.
        await proton.save_session('session.pickle')

asyncio.run(main())
```

### Session Management
```python
import asyncio
from protonmail import ProtonMail

async def main():
    async with ProtonMail() as proton:
        # Load session
        await proton.load_session('session.pickle', auto_save=True)
        # Autosave is needed to save tokens if they are updated
        # (the access token is only valid for 24 hours and will be updated automatically)

        # Getting a list of all sessions in which you are authorized
        sessions = await proton.get_all_sessions()
        print(sessions)

        # Revoke all sessions except the current one
        await proton.revoke_all_sessions()

asyncio.run(main())
```

### 🆕 Quick Token-Based Authentication

If you have previously extracted authentication tokens, you can use them directly without full login:

```python
import asyncio
from protonmail import ProtonMail

async def main():
    # Your saved tokens
    uid = "your_uid_here"
    auth_token = "your_auth_token"
    refresh_token = "your_refresh_token"
    password = "YourPassword123"

    async with ProtonMail() as proton:
        # Configure tokens for previously logged-in account
        proton.configure_tokens(uid, auth_token, refresh_token)
        
        # Parse login info and save session
        await proton._parse_info_after_login(password)
        await proton.save_session('session.pickle')
        
        # Now you can use the API
        messages = await proton.get_messages()
        print(f"Got {len(messages)} messages")

asyncio.run(main())
```

### Event Polling
Event polling. Polling ends in 3 cases:
1. Callback returns not `None`.
2. The callback raises the `SystemExit` exception.
3. Timeout ends.

For example, wait indefinitely until 2 messages arrive:
```python
import asyncio
from protonmail import ProtonMail

async def callback(response: dict, new_messages: list):
    messages = response.get('Messages', [])
    new_messages.extend(messages)
    if len(new_messages) >= 2:
        raise SystemExit

async def main():
    async with ProtonMail() as proton:
        await proton.login(username, password)
        new_messages = []
        await proton.event_polling(callback, new_messages)
        print(new_messages)

asyncio.run(main())
```

## CAPTCHA

### Solve CAPTCHA
Instructions to solve CAPTCHA:
1. At the moment automatic CAPTCHA solving is already implemented (used by default), it uses `cv2` and `NumPy`. Sometimes `CantSolveImageCaptcha` exception may occur, it means you encountered a complex image, just try to log in again.
2. You can use manual CAPTCHA solving:
   1. Login with `proton.login(username, password, captcha_config=CaptchaConfig(type=CaptchaConfig.CaptchaType.MANUAL))`
   2. You will see a url in the console, copy it.
   3. Open a new browser tab in incognito mode.
   4. Open the "DevTools" panel (press `F12`)
   5. Go to the "Network" tab.
   6. Enable network logging (press `CTRL + E`)
   7. Follow the copied url (from point 2.2)
   8. Solve the CAPTCHA.
   9. Find the `init` request in the "Network" tab and open it.
   10. In the "Preview" tab of the request, copy the token value.
   11. Paste the token into the python console.

![CAPTCHA token interception](assets/captcha-token-interception.png)

### Avoid CAPTCHA
Instructions to avoid CAPTCHA:
1. There maybe a DDoS attack, just wait 1-2 days.
2. Stop logging into your account too often, use the `save_session` and `load_session` methods.
3. Change your IP address (for example, reboot your router, use VPN, Share mobile Internet).
4. If CAPTCHA also appears in your browser:
   1. Open a browser tab in incognito mode.
   2. Log into your account.
   3. Solve the CAPTCHA.
   4. Wait for your mail to load.
   5. Close the tab.
   6. Repeat this about 10 times, then your account (only this one) can be allowlisted, and authorization (including `protonmail-api-client`) will be without CAPTCHA.

### Extract Tokens from Browser (Manual Session Restore)

5. Use `cookies` from the browser:
   1. Open a browser tab in incognito mode.
   2. Open the login page (https://account.proton.me/mail).
   3. Open the "DevTools" panel (press `F12`).
   4. Go to the "network" tab.
   5. Enable recording network log (press `CTRL + E`).
   6. Log in to your account (check "Keep me signed in").
   7. Find the `auth` request in the "Network" tab and open it.
   8. In the "Headers" tab of the request, scroll down to the `Set-Cookie` items in the "Response Headers" list.
   9. Copy the key and value from the cookies: `REFRESH-*`, `AUTH-*`.
   10. Extract the UID (the part after `AUTH-`).
   11. Close the incognito tab (Do not click the "log out" button, otherwise cookies will be invalidated).

![cookies interception](assets/cookies-interception.png)

**Method 1: Using `configure_tokens()` (Recommended):**
```python
import asyncio
from protonmail import ProtonMail

async def main():
    # Extract these from browser DevTools
    uid = "lgfbju2dxc1234567890mrf3tqmqfhv6q"  # Part after AUTH-
    auth_token = "qr4uci1234567890anafsku8dd34vkwq"   # Value of AUTH-{uid} cookie
    refresh_token = "ceo5gp1234567890fghuinsxxtgmpvdduxg"  # Extract from REFRESH-{uid} cookie JSON
    password = 'YourPassword123'

    async with ProtonMail() as proton:
        # One-line configuration
        proton.configure_tokens(uid, auth_token, refresh_token)
        await proton._parse_info_after_login(password)
        await proton.save_session('session.pickle')

asyncio.run(main())
```

**Method 2: Manual Cookie/Header Setting (Advanced):**
```python
import asyncio
from protonmail import ProtonMail

async def main():
    async with ProtonMail() as proton:
        # Set manually (backward compatible)
        proton.session.headers['x-pm-uid'] = 'lgfbju2dxc1234567890mrf3tqmqfhv6q'
        proton.session.cookies['AUTH-lgfbju2dxc1234567890mrf3tqmqfhv6q'] = 'qr4uci1234567890anafsku8dd34vkwq'
        proton.session.cookies['REFRESH-lgfbju2dxc1234567890mrf3tqmqfhv6q'] = '%7B%22ResponseType%22%3A%22token%22%2C%22ClientID%22%3A%22WebAccount%22%2C%22GrantType%22%3A%22refresh_token%22%2C%22RefreshToken%22%3A%22ceo5gp1234567890fghuinsxxtgmpvdduxg%22%2C%22UID%22%3A%22lgfbju2dxc1234567890mrf3tqmqfhv6q%22%7D'
        
        password = 'YourPassword123'
        await proton._parse_info_after_login(password)
        await proton.save_session('session.pickle')

asyncio.run(main())
```

## Migration from Synchronous Version

If you're migrating from a previous synchronous version:

1. **Add `async`/`await`**: All network methods are now async
2. **Use context manager**: Wrap with `async with ProtonMail() as proton:`
3. **Update function calls**: Add `await` before method calls
4. **Use `asyncio.run()`**: Wrap your main function call

**Before:**
```python
proton = ProtonMail()
proton.login(username, password)
messages = proton.get_messages()
```

**After:**
```python
async def main():
    async with ProtonMail() as proton:
        await proton.login(username, password)
        messages = await proton.get_messages()

asyncio.run(main())
```
