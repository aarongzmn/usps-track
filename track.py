import csv
import pandas as pd
import aiohttp
import asyncio
import time
from xml.etree import ElementTree
import urllib.parse
import os
from tqdm import tqdm


# open tracking list from csv file and create list of items
my_list = []
with open("sample_mix.csv", newline="") as inputfile:
    next(inputfile)
    for row in csv.reader(inputfile):
        my_list.append(row[0])


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


# set limit of asyncrohous request here
n = 10  # rename to "batch" later on

# set minimum seconds between batch request here
throttle = 1


usps_username = os.environ.get("USPS_USERID")
usps_link = "http://production.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML="
usps_data = """<TrackFieldRequest USERID="{usps_username}">
                <ClientIp>111.0.0.1</ClientIp>
                <TrackID ID="{track}" />
                </TrackFieldRequest>""".replace(
    "{usps_username}", usps_username
)

list_track = []
list_status = []
list_date = []

lists = list(divide_chunks(my_list, n))

for list in tqdm(lists):
    start = time.perf_counter()  # start timer

    async def main():
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*(_get_response(session, trackno) for trackno in list))

    async def _get_response(session, trackno):
        async with session.get(
            usps_link + urllib.parse.quote(usps_data.replace("{track}", trackno))
        ) as resp:
            r = await resp.text()
            r = ElementTree.fromstring(r)

            list_track.append(trackno)

            event = r.findall("TrackInfo/TrackSummary/Event")
            for e in event:
                event = e.text
            list_status.append(event)

            eventdate = r.findall("TrackInfo/TrackSummary/EventDate")
            for e in eventdate:
                eventdate = e.text
            list_date.append(eventdate)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    elapsed = time.perf_counter() - start  # stop timer
    if elapsed > throttle:  # set minimum amount of seconds per request batch here
        pass
    else:
        time.sleep(
            throttle - elapsed
        )  # used to make sure there is always at least 1 second per n number of requests


df = pd.DataFrame(list_track)
df["status"] = list_status
df["date"] = list_date


# stop timer and print time
times = []
elapsed = time.perf_counter() - start
times.append(f"executed in {elapsed:0.2f} seconds.")
print(times)

df.to_csv("sample_list_response.csv")
