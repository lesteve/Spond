import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from spond import spond


username = "..."
password = "..."


async def my_query(self, group_id, n_posts=5):
    """

    self is the Spond object
    """
    # https://api.spond.com/core/v1/posts?type=PLAIN&includeComments=true&includeReadStatus=true&includeSeenCount=true&max=5&groupId=<groupId>
    url = f"{self.api_url}posts?type=PLAIN&includeComments=true&includeReadStatus=true&max={n_posts}&groupId={group_id}"
    async with self.clientsession.get(url, headers=self.auth_headers) as r:
        return await r.json()


async def display_post(s, post):
    sender = await s.get_person(post["ownerId"])
    sender_name = f"{sender['firstName']} {sender['lastName']}"
    date_utc = datetime.fromisoformat(post['timestamp'])
    date = date_utc.astimezone(ZoneInfo("Europe/Paris"))
    date_str = date.isoformat()

    print("-" * 80)
    print(f"{sender_name=}")
    print(f"{date_str=}")
    print(post["title"])
    print(post["body"])
    print(f'{post["unread"]=}')
    print("-" * 80)


async def main():
    s = spond.Spond(username=username, password=password)
    groups = await s.get_groups()
    main_group = [g for g in groups if "Club" in g["name"]][0]

    posts = await my_query(s, main_group["id"])

    for p in posts:
        await display_post(s, p)

asyncio.run(main())
