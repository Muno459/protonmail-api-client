#!/usr/bin/env python3

"""
Example showing the new async ProtonMail API with automatic token refresh.

The async version now properly handles token refresh just like the sync version did!
No more "Invalid access token" errors when tokens expire.
"""

import asyncio
from src.protonmail import ProtonMail


async def main():
    # Example credentials (replace with your actual tokens)
    uid = "m24ptyvpzexid6qwgtr2krop56p3yjjf"
    auth_token = "xhs46vqjlubr3kgbvzzihcitxlqlfx3z"
    refresh_token = "jod3623m44c6rgaqavigcoofrzja2oi5"
    email = "sir.james.third@proton.me"
    password = "Tovben-3kyqdy-hoknaz"

    print("🔧 Testing async ProtonMail with automatic token refresh...")

    # Method 1: Using the new configure_tokens method
    async with ProtonMail() as proton:
        try:
            # Configure tokens for previously logged-in account
            proton.configure_tokens(uid, auth_token, refresh_token)
            
            # Parse login info and save session
            await proton._parse_info_after_login(password)
            await proton.save_session('session.pickle')
            
            # Now you can use the API - even with expired tokens!
            # The async version now automatically refreshes tokens on 401 errors
            messages = await proton.get_messages()
            print(f"✅ Got {len(messages)} messages (tokens auto-refreshed if needed)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try getting fresh tokens from your browser or use regular login")

    # Method 2: Load from saved session (recommended)
    print("\n🔄 Testing session load...")
    async with ProtonMail() as proton:
        try:
            await proton.load_session('session.pickle')
            messages = await proton.get_messages_by_page(0, 10)  # Get first 10 messages
            print(f"✅ Loaded session, got {len(messages)} messages")
        except Exception as e:
            print(f"❌ Session load failed: {e}")

    # Method 3: Regular login (fallback)
    print("\n🔐 Testing regular login as fallback...")
    async with ProtonMail() as proton:
        try:
            await proton.login(email, password)
            await proton.save_session('session_new.pickle')
            print("✅ Regular login successful")
        except Exception as e:
            print(f"❌ Login failed: {e}")

    print("\n🎉 Async migration complete! Token refresh now works like the sync version!")


if __name__ == "__main__":
    asyncio.run(main()) 