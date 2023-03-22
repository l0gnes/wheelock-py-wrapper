from typing import Optional, List, Dict
from asyncio import AbstractEventLoop, get_event_loop
from objects.periods import PERIODS
from objects.Menu import Menu
from datetime import date
import aiohttp

from utils import format_date

class WheelockAPI(object):

    # Constants required to be known
    WHEELOCK_LOCATION_ID : str = "63b7353d92d6b47d412fff24"

    loop : AbstractEventLoop
    period_cache : Dict[date, List[Dict[PERIODS, str]]]



    def __init__(
        self,
        loop : Optional[AbstractEventLoop] = None
    ) -> None:
        
        self.loop = loop if loop else get_event_loop()
        self.period_cache = {}



    async def period_cache_check(
        self,
        d : date
    ):
        
        if d in self.period_cache.keys():
            return

        async with aiohttp.ClientSession() as session:

            async with session.get(
                "https://api.dineoncampus.ca/v1/location/%s/periods?platform=0&date=%s" 
                % (self.WHEELOCK_LOCATION_ID, format_date(d))
            ) as resp:
                json_data = await resp.json()
        
        period_data = json_data["periods"]
        
        completed = []

        for p in period_data:

            for m in [b for b in PERIODS.__members__.values() if b not in completed]:

                if p["name"] == m.value:
                    
                    completed.append(m)

                    if d not in self.period_cache:
                        self.period_cache[d] = {}

                    self.period_cache[d][m] = p['id']



    async def get_period_id(
        self,
        period : PERIODS,
        d : date,
    ):
        await self.period_cache_check(d)
        return self.period_cache[d][period]



    async def get_menu(
        self,
        period : PERIODS,
        d : date
    ) -> Menu:
        pid = await self.get_period_id(period, d)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.dineoncampus.ca/v1/location/%s/periods/%s?platform=0&date=%s" 
                % (self.WHEELOCK_LOCATION_ID, pid, format_date(d))
            ) as resp:
                json_data = await resp.json()

        menu_data = json_data['menu']
        return Menu.parseFromJSON(menu_data)