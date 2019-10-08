import os
import requests
import urllib.parse
import xml.etree.ElementTree as ET


usps_username = os.environ.get("USPS_USERID")
validate_url = 'http://production.shippingapis.com/ShippingApi.dll?API=Verify&XML='
validate_address = f'''
    <AddressValidateRequest USERID="{usps_username}">
        <Revision>1</Revision>
        <Address ID="0">
        <Address1>1915 Batson Ave.</Address1>
        <Address2>Apt. 19</Address2>
        <City/>
        <State>CA</State>
        <Zip5>91748</Zip5>
        <Zip4/>
        </Address>
    </AddressValidateRequest>'''

address_encoded = urllib.parse.quote(validate_address)
root = ET.fromstring(requests.get(validate_url+address_encoded).content)

print(root[0][13].text)
