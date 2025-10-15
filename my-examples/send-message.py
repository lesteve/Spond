import asyncio
import subprocess

import click

from spond import spond


# email used for Spond
username = "..."
# Spond password
password = "..."


async def spond_func(to, message):
    s = spond.Spond(username=username, password=password)
    groups = await s.get_groups()
    main_group = [g for g in groups if "Club" in g["name"]][0]
    print(f"{main_group['id']=}")
    # You need both user and group_uid otherwise
    # {'error': 'wrong usage, group_id and user_id needed or continue chat with chat_id'}
    # Similar to in Spond web UI where you need to select a group before
    # sending a message to one person ...
    result = await s.send_message(
        message,
        user=to,
        group_uid=main_group["id"],
    )
    print(f"{result=}")
    await s.clientsession.close()


# Need this kind of dance for asyncio + click. I guess click.command wants a "normal" function
@click.command()
@click.option(
    "--to", help="User to send message to, <first_name> <last_name>, e.g. John Doe"
)
@click.option("--message", help="Message to send")
def main(to, message):
    asyncio.run(spond_func(to, message))


if __name__ == "__main__":
    main()
