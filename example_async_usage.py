#!/usr/bin/env python3

"""
Example showing the new async ProtonMail API with built-in token configuration.

The async migration is now complete and includes a configure_tokens() method
to easily restore access to previously logged-in accounts.
"""

import asyncio
from src.protonmail import ProtonMail


async def main():
    # Example credentials (replace with your actual tokens)
    uid = "rbmlchsyeyyo4qxonadfwopvy22qy2p4"
    auth_token = "xxxmrxse4fyayy6kgi26yj4cwa5is5ez"
    refresh_token = "rbmlchsyeyyo4qxonadfwopvy22qy2p4"
    email = "sir.james.third@proton.me"
    password = "Tovben-3kyqdy-hoknaz"

    # Method 1: Using the new configure_tokens method (recommended)
    async with ProtonMail() as proton:
        # Configure tokens for previously logged-in account
        proton.configure_tokens(uid, auth_token, refresh_token)
        
        # Parse login info and save session
        await proton._parse_info_after_login(password)
        await proton.save_session('session.pickle')
        
        # Now you can use the API
        messages = await proton.get_messages()
        print(f"✅ Got {len(messages)} messages")

    # Method 2: Manual approach (still works)
    async with ProtonMail() as proton:
        # Set headers and cookies manually (backward compatible)
        proton.session.headers['x-pm-uid'] = uid
        proton.session.cookies[f'AUTH-{uid}'] = auth_token
        proton.session.cookies[f'REFRESH-{uid}'] = 'your_url_encoded_refresh_payload'

        await proton._parse_info_after_login(password)
        await proton.save_session('session.pickle')
        print("✅ Session configured manually!")

    # Method 3: Load from saved session
    async with ProtonMail() as proton:
        await proton.load_session('session.pickle')
        messages = await proton.get_messages() 
        print(f"✅ Loaded session, got {len(messages)} messages")

    print("✅ All methods work! Use configure_tokens() for the easiest setup.")


if __name__ == "__main__":
    asyncio.run(main()) 