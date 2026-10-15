PARKS = [
 {"name":"Tsavo Conservation Area","country":"Kenya","lat":-2.90,"lng":38.40,"area_km2":22000,"species":["Elephant","Buffalo","Lion","Giraffe","Zebra","Oryx"]},
 {"name":"Laikipia Plateau","country":"Kenya","lat":0.20,"lng":36.90,"area_km2":9500,"species":["Elephant","Grevy's zebra","Reticulated giraffe","Lion","Wild dog"]},
 {"name":"KAZA TFCA","country":"Multi","lat":-18.00,"lng":24.50,"area_km2":520000,"species":["Elephant","Buffalo","Hippo","Lion","Sable","Wild dog"]},
 {"name":"Samburu NR","country":"Kenya","lat":0.60,"lng":37.53,"area_km2":165,"species":["Elephant","Grevy's zebra","Reticulated giraffe","Gerenuk","Beisa oryx"]},
 {"name":"Maasai Mara NR","country":"Kenya","lat":-1.50,"lng":35.10,"area_km2":1510,"species":["Wildebeest","Zebra","Lion","Elephant","Cheetah","Hippo"]},
 {"name":"Amboseli NP","country":"Kenya","lat":-2.65,"lng":37.26,"area_km2":392,"species":["Elephant","Buffalo","Zebra","Wildebeest","Hippo"]},
 {"name":"Serengeti NP","country":"Tanzania","lat":-2.33,"lng":34.83,"area_km2":14750,"species":["Wildebeest","Zebra","Lion","Elephant","Buffalo","Cheetah"]},
 {"name":"Ruaha NP","country":"Tanzania","lat":-7.70,"lng":34.65,"area_km2":20226,"species":["Elephant","Buffalo","Lion","Greater kudu","Wild dog"]},
 {"name":"Nyerere NP (Selous)","country":"Tanzania","lat":-8.50,"lng":37.50,"area_km2":30893,"species":["Elephant","Buffalo","Hippo","Wild dog","Sable"]},
 {"name":"Queen Elizabeth NP","country":"Uganda","lat":-0.20,"lng":30.00,"area_km2":1978,"species":["Elephant","Buffalo","Hippo","Lion","Uganda kob"]},
 {"name":"Murchison Falls NP","country":"Uganda","lat":2.20,"lng":31.80,"area_km2":3840,"species":["Elephant","Giraffe","Buffalo","Hippo","Uganda kob"]},
 {"name":"Kidepo Valley NP","country":"Uganda","lat":3.90,"lng":33.75,"area_km2":1442,"species":["Elephant","Buffalo","Giraffe","Lion","Zebra"]},
 {"name":"South Luangwa NP","country":"Zambia","lat":-13.10,"lng":31.60,"area_km2":9050,"species":["Elephant","Hippo","Buffalo","Leopard","Thornicroft's giraffe"]},
 {"name":"Okavango Delta","country":"Botswana","lat":-19.30,"lng":22.90,"area_km2":15000,"species":["Elephant","Buffalo","Hippo","Lechwe","Wild dog"]},
 {"name":"Chobe NP","country":"Botswana","lat":-18.65,"lng":24.50,"area_km2":11700,"species":["Elephant","Buffalo","Hippo","Sable","Lion"]},
 {"name":"Hwange NP","country":"Zimbabwe","lat":-18.80,"lng":26.50,"area_km2":14650,"species":["Elephant","Buffalo","Giraffe","Lion","Sable"]},
 {"name":"Etosha NP","country":"Namibia","lat":-18.85,"lng":16.33,"area_km2":22270,"species":["Elephant","Springbok","Oryx","Zebra","Black rhino","Lion"]},
 {"name":"Kruger NP","country":"South Africa","lat":-24.00,"lng":31.50,"area_km2":19485,"species":["Elephant","Buffalo","Lion","Rhino","Leopard","Impala"]},
 {"name":"Virunga NP","country":"DR Congo","lat":-0.50,"lng":29.30,"area_km2":7800,"species":["Elephant","Hippo","Buffalo","Mountain gorilla","Okapi"]},
]
def park_names(): return [p["name"] for p in PARKS]
def get_park(n):
    for p in PARKS:
        if p["name"]==n: return p
    return None
