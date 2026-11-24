"""Heuristics for describing headers before the dataset schema is verified."""

import re


def column_group(name: str) -> str:
    field = name.strip().casefold()
    if re.search(r"(?:^|[._ -])(?:label|class|target|attack_type)(?:$|[._ -])", field):
        return "label_candidate"
    prefix = field.partition(".")[0]
    if prefix == "frame":
        return "frame"
    if prefix in {"radiotap", "wlan_radio"}:
        return "physical"
    if prefix in {"wlan", "eap", "eapol"}:
        return "wlan"
    if prefix in {"ip", "ipv6", "arp", "icmp", "icmpv6"}:
        return "network"
    if prefix in {"tcp", "udp", "sctp"}:
        return "transport"
    if prefix in {"dns", "http", "http2", "tls", "ssh", "ssdp", "smb", "smb2", "dhcp"}:
        return "application"
    return "other"


def identifier_candidate(name: str) -> bool:
    field = name.strip().casefold()
    return bool(re.search(
        r"(?:^|[._ -])(?:id|identifier|addr|address|mac|ssid|bssid|sa|da|ta|ra)(?:$|[._ -])",
        field,
    ) or re.fullmatch(r"(?:ip|ipv6)(?:\.(?:src|dst))?", field))
