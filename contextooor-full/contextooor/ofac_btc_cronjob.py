import requests
import xml.etree.ElementTree as ET
import polars as pl

DEMO_SANCTIONED_ADDRESSES=["18qTfJCWzT4WW34eRZVV5u2Wf5iCCUsipd","14HivzpNZkTVyLvzuEgaK8xRvLJux1W3TL","1P1GMmXTNW9Nv11MkbJLGrDmsUPhjeeNVr","18xVYvcSi41RXSxWR95M5rHLfg1wA1g2qo","1Kh8cDRYmXpVMHkLiNG4pJRBeXZibUo2Kp"]

def feature_type_text(asset):
    """returns text we expect in a <FeatureType></FeatureType> tag for a given asset"""
    return "Digital Currency Address - " + asset

def get_address_id(root, asset):
    """returns the feature id of the given asset"""
    feature_type = root.find(
        "sdn:ReferenceValueSets/sdn:FeatureTypeValues/*[.='{}']".format(feature_type_text(asset)), {'sdn': 'http://www.un.org/sanctions/1.0'})
    if feature_type == None:
        raise LookupError("No FeatureType with the name {} found".format(
            feature_type_text(asset)))
    address_id = feature_type.attrib["ID"]
    return address_id

def get_sanctioned_addresses(root, address_id):
    """returns a list of sanctioned addresses for the given address_id"""
    addresses = list()
    for feature in root.findall("sdn:DistinctParties//*[@FeatureTypeID='{}']".format(address_id), {'sdn': 'http://www.un.org/sanctions/1.0'}):
        for version_detail in feature.findall(".//sdn:VersionDetail", {'sdn': 'http://www.un.org/sanctions/1.0'}):
            addresses.append(version_detail.text)
    return addresses

def get_sanction_list(update=False):
    url = 'https://www.treasury.gov/ofac/downloads/sanctions/1.0/sdn_advanced.xml'
    response = requests.get(url)
    with open('sdn_advanced.xml', 'wb') as file:
        file.write(response.content)
    tree = ET.parse("./sdn_advanced.xml")
    root = tree.getroot()
    address_id = get_address_id(root, "XBT")
    addresses = get_sanctioned_addresses(root, address_id)
    addresses = list(dict.fromkeys(addresses).keys())
    addresses.extend(DEMO_SANCTIONED_ADDRESSES)
    df=pl.DataFrame({"addresses":addresses})
    df.write_parquet('btc_sanctioned_addresses.parquet')

get_sanction_list()