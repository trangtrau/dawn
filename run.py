import asyncio
import json
from loguru import logger

# credits to dwisyafriadi/dawn
async def send_keepalive_request(appid, bearer_token, username, extension_id, number_of_tabs):
    url = f"https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive?appid={appid}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": f"chrome-extension://{extension_id}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
    }
    payload = {
        "username": username,
        "extensionid": extension_id,
        "numberoftabs": number_of_tabs,
        "_v": "1.0.9"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=payload) as response:
                response_data = await response.json()
                logger.info(f"Response: {response_data}")
                return response_data
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return None

async def execute_account(account, extension_id, number_of_tabs):
    response = await send_keepalive_request(
        account["AppID"], account["Token"], account["Email"], extension_id, number_of_tabs
    )
    if response:
        logger.info(f"Keep alive successful for {account['Email']}")
        return True
    else:
        logger.error(f"Keep alive failed for {account['Email']}")
        return False

async def main():
    with open("config.json", "r") as config_file:
        accounts = json.load(config_file)
    extension_id = "fpdkjdnhkakefebpekbdhillbhonfjjp"
    number_of_tabs = 0
    while True:
        for account in accounts:
            success = await execute_account(account, extension_id, number_of_tabs)
            if not success:
                logger.info(f"Moving to the next account after failure: {account['Email']}")
        logger.info("All accounts processed. Restarting after 180 seconds.")
        await asyncio.sleep(180)

if __name__ == '__main__':
    asyncio.run(main())
