from stobox_dependencies.clients import public_page_client
from stobox_dependencies.schemes.public_page import PublicPageInfo


async def get_public_page_info(domain: str) -> PublicPageInfo:
    public_page_info = await public_page_client.get_public_page_info(domain)
    return public_page_info
