import asyncio
import httpx

with open('cookie.txt', encoding='utf-8') as f:
    cookie = f.read()

client = httpx.AsyncClient(
    cookies={'.ROBLOSECURITY': cookie}
)

MESSAGES = 'https://privatemessages.roblox.com/v1/messages'


async def fetch_csrf():
    req = await client.post('https://auth.roblox.com/v1/xbox/disconnect')
    return req.headers['x-csrf-token']


async def clear_page(page_number):
    req = await client.get(f'{MESSAGES}?pageNumber={page_number}&pageSize=20&messageTab=Inbox')
    res = req.json()

    msg_ids = [i['id'] for i in res['collection']]
    await client.post(
        'https://privatemessages.roblox.com/v1/messages/archive',
        data={"messageIds": msg_ids},
        headers={'x-csrf-token': await fetch_csrf()})


async def main():
    req = await client.get(f'{MESSAGES}?pageNumber=1&pageSize=20&messageTab=Inbox')
    res = req.json()
    pages = res.get('totalPages', None)
    if not pages:
        return

    await asyncio.gather(
        *(clear_page(i) for i in range(pages))
    )

asyncio.run(main())
