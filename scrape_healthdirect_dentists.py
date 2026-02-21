#!/usr/bin/env python3
"""Scrape dental practices (Dentists service type) from Healthdirect Service Finder API.

Outputs:
- healthdirect_dentists_master.csv
- healthdirect_dentists_QLD.csv
- healthdirect_dentists_NSW.csv
- healthdirect_dentists_VIC.csv

Notes:
- Uses publicly accessible Healthdirect endpoints under /australian-health-services/api.
- Coverage is based on a curated set of suburb/postcode anchors per state, de-duplicated by healthcareService id.
"""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

API_BASE = "https://www.healthdirect.gov.au/australian-health-services/api"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

DENTISTS_IDREF = "nhsd:/reference/taxonomies/snomed-servicetype/310144008"  # Dentists

# Curated anchor suburbs (query strings) per state.
ANCHORS: Dict[str, List[str]] = {
    "QLD": [
        "Brisbane City",
        "Southport",
        "Surfers Paradise",
        "Maroochydore",
        "Caloundra",
        "Ipswich",
        "Logan Central",
        "Cairns",
        "Townsville",
        "Toowoomba",
        "Mackay",
        "Rockhampton",
        "Bundaberg",
        "Gladstone",
    ],
    "NSW": [
        "Sydney",
        "Parramatta",
        "Penrith",
        "Newcastle",
        "Wollongong",
        "Gosford",
        "Coffs Harbour",
        "Port Macquarie",
        "Tamworth",
        "Dubbo",
        "Bathurst",
        "Albury",
        "Wagga Wagga",
        "Lismore",
    ],
    "VIC": [
        "Melbourne",
        "Geelong",
        "Ballarat",
        "Bendigo",
        "Shepparton",
        "Mildura",
        "Warrnambool",
        "Traralgon",
        "Frankston",
        "Dandenong",
    ],
}


@dataclass
class Suburb:
    id: str
    label: str
    code: str
    state_label: str
    state_idref: str
    centroid_lat: str
    centroid_lon: str

    @classmethod
    def from_api(cls, d: Dict[str, Any]) -> "Suburb":
        return cls(
            id=d.get("id") or "",
            label=d.get("label") or "",
            code=d.get("code") or "",
            state_label=((d.get("state") or {}).get("label") or ""),
            state_idref=((d.get("state") or {}).get("idRef") or ""),
            centroid_lat=((d.get("centroid") or {}).get("latitude") or ""),
            centroid_lon=((d.get("centroid") or {}).get("longitude") or ""),
        )

    def to_query_obj(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "code": self.code,
            "centroid": {"latitude": self.centroid_lat, "longitude": self.centroid_lon},
            "state": {"idRef": self.state_idref, "label": self.state_label},
        }


def http_get_json(url: str, timeout: int = 30) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "ignore")
    return json.loads(raw)


def resolve_suburb(query: str, state: str) -> Optional[Suburb]:
    url = API_BASE + "/location?q=" + urllib.parse.quote(query)
    try:
        obj = http_get_json(url)
    except Exception:
        return None

    suburbs = (obj.get("data") or {}).get("suburbs") or []
    # Try to pick a suburb in the desired state, preferring exact label match tokens if possible.
    # Many queries include postcode; centroid/state filtering is the main constraint.
    candidates = [Suburb.from_api(s) for s in suburbs if ((s.get("state") or {}).get("label") == state)]
    if not candidates:
        return None

    # Prefer those whose label appears in query.
    q_low = query.lower()
    def score(s: Suburb) -> Tuple[int, int]:
        # higher is better
        label_hit = 1 if s.label.lower() in q_low else 0
        code_hit = 1 if s.code and s.code in query else 0
        return (label_hit + code_hit, -len(s.label))

    candidates.sort(key=score, reverse=True)
    return candidates[0]


def encode_q(q_obj: Dict[str, Any]) -> str:
    # IMPORTANT: encode all characters (safe='') because idRef contains forward slashes.
    q_str = json.dumps(q_obj, separators=(",", ":"))
    return urllib.parse.quote(q_str, safe="")


def search_services(suburb: Suburb, radius_km: int, offset: int, limit: int, lang: str = "en") -> Dict[str, Any]:
    q = {
        "suburb": suburb.to_query_obj(),
        "serviceTypeCodes": [DENTISTS_IDREF],
        "offset": offset,
        "limit": limit,
        "radius": radius_km,
    }
    url = API_BASE + "/healthcare-service?q=" + encode_q(q) + "&lang=" + urllib.parse.quote(lang)
    return http_get_json(url, timeout=40)


def get_service_detail(service_id: str, lang: str = "en") -> Dict[str, Any]:
    url = API_BASE + f"/healthcare-service/{urllib.parse.quote(service_id)}?lang={urllib.parse.quote(lang)}"
    return http_get_json(url, timeout=40)


def extract_contacts(contacts: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {"Phone": [], "Email": [], "Website": []}
    if not contacts:
        return out

    # Sort by priority descending (higher first). If missing, treat as 0.
    contacts_sorted = sorted(contacts, key=lambda c: (c.get("priority") if isinstance(c.get("priority"), int) else 0), reverse=True)
    for c in contacts_sorted:
        vt = (c.get("valueType") or {}).get("label")
        val = (c.get("value") or "").strip()
        if not vt or not val:
            continue
        if vt in out:
            if val not in out[vt]:
                out[vt].append(val)
    return out


def safe_get(d: Dict[str, Any], path: List[str]) -> Optional[Any]:
    cur: Any = d
    for p in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
    return cur


def normalise_state(label: str) -> str:
    return (label or "").strip().upper()


def main() -> None:
    rows: List[Dict[str, str]] = []
    seen_service_ids: Set[str] = set()

    # Heuristic radii: metro anchors get smaller radius to reduce spillover; regionals larger.
    default_radius_by_state = {"QLD": 30, "NSW": 30, "VIC": 30}

    for state, queries in ANCHORS.items():
        for query in queries:
            suburb = resolve_suburb(query, state)
            if not suburb:
                continue

            radius = default_radius_by_state[state]
            # Some anchors are explicitly regional; bump radius slightly.
            if suburb.code and suburb.code not in ("2000", "3000", "4000"):
                radius = 35

            offset = 0
            limit = 50

            while True:
                try:
                    res = search_services(suburb=suburb, radius_km=radius, offset=offset, limit=limit)
                except Exception:
                    break

                services = res.get("data") or []
                if not services:
                    break

                for s in services:
                    service_id = s.get("id")
                    if not service_id or service_id in seen_service_ids:
                        continue

                    # Filter by actual service state (avoid cross-border spillover).
                    svc_state = normalise_state(safe_get(s, ["location", "physicalLocation", "state", "label"]) or "")
                    if svc_state and svc_state != state:
                        continue

                    seen_service_ids.add(service_id)

                    # Pull richer contacts (email often only appears in detail).
                    detail = None
                    try:
                        detail = get_service_detail(service_id)
                    except Exception:
                        detail = None

                    svc = (detail or {}).get("data", {}).get("healthcareService") if detail else None
                    if not isinstance(svc, dict):
                        svc = s  # fallback

                    org_name = (safe_get(svc, ["organisation", "name"]) or safe_get(s, ["organisation", "name"]) or "").strip()
                    if not org_name:
                        org_name = "(Unknown)"

                    pl = safe_get(svc, ["location", "physicalLocation"]) or safe_get(s, ["location", "physicalLocation"]) or {}
                    city = (safe_get(pl, ["suburb", "label"]) or "").strip().title()
                    postcode = (safe_get(pl, ["postcode"]) or "").strip()
                    svc_state = normalise_state(safe_get(pl, ["state", "label"]) or state)

                    contacts = extract_contacts((svc.get("contacts") or []) if isinstance(svc, dict) else [])
                    phone = "; ".join(contacts.get("Phone") or [])
                    email = "; ".join(contacts.get("Email") or [])
                    website = "; ".join(contacts.get("Website") or [])

                    rows.append(
                        {
                            "State": svc_state,
                            "Practice Name": org_name,
                            "Principal Dentist / Owner": "",  # not consistently available in this dataset
                            "City": city,
                            "Postcode": postcode,
                            "Phone": phone,
                            "Email": email,
                            "Website": website,
                            "Source": "Healthdirect Service Finder",
                            "Healthdirect Service ID": service_id,
                        }
                    )

                offset += len(services)
                count = res.get("count")
                if isinstance(count, int) and offset >= count:
                    break
                if len(services) < limit:
                    break

                time.sleep(0.2)

            time.sleep(0.2)

    # Write CSVs
    def write_csv(path: str, items: List[Dict[str, str]]) -> None:
        if not items:
            return
        fieldnames = list(items[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(items)

    master_path = "healthdirect_dentists_master.csv"
    write_csv(master_path, rows)

    for st in ["QLD", "NSW", "VIC"]:
        subset = [r for r in rows if r.get("State") == st]
        write_csv(f"healthdirect_dentists_{st}.csv", subset)

    print(f"Total rows: {len(rows)}")
    print(f"Unique services: {len(seen_service_ids)}")


if __name__ == "__main__":
    main()
