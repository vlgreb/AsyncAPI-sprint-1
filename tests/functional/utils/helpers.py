from tests.functional.settings import TestSettings
from tests.functional.utils.models import ResponseFromApi


async def get_data(api_session, query: str, query_params: dict | None, settings: TestSettings):

    url = f'{settings.api_prefix}{query}'

    async with api_session.get(url, params=query_params) as response:
        data = await response.json()
        validation = {
            "status": response.status,
            "length": len(data)
        }

    return ResponseFromApi(data=data, validation=validation)
