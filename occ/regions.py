REGIONS = [
    {"name":"Tsavo Conservation Area","country":"Kenya","lat":-2.90,"lng":38.40,"ecosystem":"Semi-arid savanna"},
    {"name":"Laikipia Plateau","country":"Kenya","lat":0.20,"lng":36.90,"ecosystem":"Highland savanna / rangeland"},
    {"name":"KAZA TFCA (core)","country":"Multi","lat":-18.00,"lng":24.50,"ecosystem":"Miombo / floodplain / savanna"},
    {"name":"Samburu–Laikipia (STE)","country":"Kenya","lat":0.60,"lng":37.53,"ecosystem":"Arid bushland"},
    {"name":"Maasai Mara","country":"Kenya","lat":-1.50,"lng":35.10,"ecosystem":"Savanna grassland"},
    {"name":"Amboseli","country":"Kenya","lat":-2.65,"lng":37.26,"ecosystem":"Savanna / swamp"},
    {"name":"Serengeti","country":"Tanzania","lat":-2.33,"lng":34.83,"ecosystem":"Savanna grassland"},
    {"name":"Ruaha","country":"Tanzania","lat":-7.70,"lng":34.65,"ecosystem":"Miombo / savanna"},
    {"name":"Nyerere (Selous)","country":"Tanzania","lat":-8.50,"lng":37.50,"ecosystem":"Miombo woodland"},
    {"name":"Queen Elizabeth","country":"Uganda","lat":-0.20,"lng":30.00,"ecosystem":"Savanna / wetland"},
    {"name":"Murchison Falls","country":"Uganda","lat":2.20,"lng":31.80,"ecosystem":"Savanna"},
    {"name":"Kidepo Valley","country":"Uganda","lat":3.90,"lng":33.75,"ecosystem":"Semi-arid savanna"},
    {"name":"South Luangwa","country":"Zambia","lat":-13.10,"lng":31.60,"ecosystem":"Miombo / valley"},
    {"name":"Okavango Delta","country":"Botswana","lat":-19.30,"lng":22.90,"ecosystem":"Floodplain / delta"},
    {"name":"Chobe","country":"Botswana","lat":-18.65,"lng":24.50,"ecosystem":"Riverine / savanna"},
    {"name":"Hwange","country":"Zimbabwe","lat":-18.80,"lng":26.50,"ecosystem":"Kalahari sand / savanna"},
    {"name":"Etosha","country":"Namibia","lat":-18.85,"lng":16.33,"ecosystem":"Saline pan / savanna"},
    {"name":"Kruger","country":"South Africa","lat":-24.00,"lng":31.50,"ecosystem":"Savanna bushveld"},
    {"name":"Virunga","country":"DR Congo","lat":-0.50,"lng":29.30,"ecosystem":"Montane / savanna"},
]
def region_names(): return [r["name"] for r in REGIONS]
def get_region(n):
    for r in REGIONS:
        if r["name"]==n: return r
    return None
