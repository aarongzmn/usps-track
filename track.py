import pandas as pd
import requests
from xml.etree import ElementTree
from tqdm import tqdm
import urllib.parse
import os


def no(track):
    usps_username = os.environ.get("USPS_USERID")
    request_url = "http://production.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML="
    request_xml = urllib.parse.quote(
        f"""<TrackFieldRequest USERID="{usps_username}">
                    <ClientIp>111.0.0.1</ClientIp>
                    <TrackID ID="{track}" />
                    </TrackFieldRequest>"""
    )
    usps = request_url + request_xml
    r = ElementTree.fromstring(requests.get(usps).content)
    return r


# read in USPS USERID from os environment variable
usps_username = os.environ.get("USPS_USERID")

# read in list of tracking numbers to be processed
data = pd.read_csv("sample_mix.csv")

df = pd.DataFrame(data=data)

status_list = []
date_list = []
code_list = []


for track in tqdm(df["TrackingNumber"]):
    r = no(track)

    event = r.findall("TrackInfo/TrackSummary/Event")
    for e in event:
        event = e.text
    status_list.append(event)

    eventdate = r.findall("TrackInfo/TrackSummary/EventDate")
    for e in eventdate:
        eventdate = e.text
    date_list.append(eventdate)

    code = r.findall("TrackInfo/TrackSummary/DeliveryAttributeCode")
    for e in code:
        code = e.text
    code_list.append(code)

df["Status"] = status_list
df["Status Date"] = date_list
df["Delivery Attribute Code"] = code_list

df.to_csv("results.csv")
