"""
Real-life product catalog and user persona metadata for RecoOps platform.
Maps item_id (0..499) to realistic commercial products with brands, specs, prices, and ratings.
"""

CATEGORIES = [
    {"name": "Audio & Sound", "color": "#06b6d4", "icon": "🎧"},
    {"name": "Computing & Displays", "color": "#8b5cf6", "icon": "💻"},
    {"name": "Keyboards & Peripherals", "color": "#10b981", "icon": "⌨️"},
    {"name": "Creator & Studio", "color": "#f59e0b", "icon": "🎙️"},
    {"name": "Smart Home & Power", "color": "#ec4899", "icon": "⚡"},
    {"name": "Workspace & Lifestyle", "color": "#6366f1", "icon": "☕"}
]

REAL_PRODUCTS_SEED = [
    # Audio & Sound (0-9)
    {"title": "Sony WH-1000XM5 Noise Canceling Wireless Headphones", "category": "Audio & Sound", "price": 398.00, "rating": 4.8, "reviews": 3410, "badge": "Best Seller"},
    {"title": "Bose QuietComfort Ultra Earbuds with Spatial Audio", "category": "Audio & Sound", "price": 299.00, "rating": 4.7, "reviews": 1820, "badge": "Top Pick"},
    {"title": "Apple AirPods Max with Smart Case - Space Gray", "category": "Audio & Sound", "price": 549.00, "rating": 4.6, "reviews": 5190, "badge": "Premium"},
    {"title": "Sennheiser HD 660S2 Open-Back Dynamic Audiophile Headphones", "category": "Audio & Sound", "price": 499.95, "rating": 4.9, "reviews": 940, "badge": "Audiophile"},
    {"title": "Audio-Technica ATH-M50x Professional Studio Monitor Headphones", "category": "Audio & Sound", "price": 149.00, "rating": 4.8, "reviews": 12840, "badge": "Classic"},
    {"title": "Shure AONIC 50 Gen 2 Premium Wireless Studio Headphones", "category": "Audio & Sound", "price": 349.00, "rating": 4.7, "reviews": 630, "badge": "Studio Pro"},
    {"title": "Sonos Era 300 Smart Speaker with Dolby Atmos", "category": "Audio & Sound", "price": 449.00, "rating": 4.8, "reviews": 1150, "badge": "New"},
    {"title": "Focal Bathys Hi-Fi Active Noise-Canceling Headphones", "category": "Audio & Sound", "price": 699.00, "rating": 4.9, "reviews": 410, "badge": "Hi-Fi Elite"},
    {"title": "Nothing Ear (2) True Wireless Hi-Res Earbuds", "category": "Audio & Sound", "price": 149.00, "rating": 4.5, "reviews": 2100, "badge": "Design Award"},
    {"title": "Marshall Stanmore III Bluetooth Home Speaker", "category": "Audio & Sound", "price": 379.99, "rating": 4.8, "reviews": 3200, "badge": "Trending"},

    # Computing & Displays (10-19)
    {"title": "Apple MacBook Pro 16\" M3 Max (36GB RAM, 1TB SSD)", "category": "Computing & Displays", "price": 3499.00, "rating": 4.9, "reviews": 840, "badge": "Pro Workstation"},
    {"title": "Dell UltraSharp 32\" 4K UHD USB-C Hub Monitor (U3223QE)", "category": "Computing & Displays", "price": 729.99, "rating": 4.8, "reviews": 1640, "badge": "Top Pick"},
    {"title": "LG 34\" UltraWide Curved Nano IPS Thunderbolt Display", "category": "Computing & Displays", "price": 899.00, "rating": 4.7, "reviews": 1280, "badge": "UltraWide"},
    {"title": "CalDigit TS4 Thunderbolt 4 18-Port Universal Docking Station", "category": "Computing & Displays", "price": 399.95, "rating": 4.9, "reviews": 2400, "badge": "Best Seller"},
    {"title": "ASUS ProArt Display 27\" 4K HDR Color-Accurate Monitor", "category": "Computing & Displays", "price": 469.00, "rating": 4.7, "reviews": 890, "badge": "Creator Choice"},
    {"title": "Samsung Odyssey OLED G9 49\" Curved Gaming Monitor 240Hz", "category": "Computing & Displays", "price": 1299.99, "rating": 4.8, "reviews": 1420, "badge": "Ultrawide Elite"},
    {"title": "Apple Mac Studio M2 Max (32GB RAM, 512GB SSD)", "category": "Computing & Displays", "price": 1999.00, "rating": 4.9, "reviews": 750, "badge": "Performance"},
    {"title": "Lenovo ThinkPad X1 Carbon Gen 11 Ultrabook Intel Core i7", "category": "Computing & Displays", "price": 1649.00, "rating": 4.7, "reviews": 980, "badge": "Business Class"},
    {"title": "BenQ ScreenBar Halo Wireless Controller LED Monitor Light Bar", "category": "Computing & Displays", "price": 179.00, "rating": 4.8, "reviews": 4310, "badge": "Essential"},
    {"title": "Anker 778 Thunderbolt 4 Docking Station 12-in-1", "category": "Computing & Displays", "price": 279.99, "rating": 4.6, "reviews": 820, "badge": "Compact"},

    # Keyboards & Peripherals (20-29)
    {"title": "Keychron Q1 Pro Wireless Custom Mechanical Keyboard (Gateron Brown)", "category": "Keyboards & Peripherals", "price": 199.00, "rating": 4.9, "reviews": 3120, "badge": "Mechanical"},
    {"title": "Logitech MX Master 3S Advanced Wireless Ergonomic Mouse", "category": "Keyboards & Peripherals", "price": 99.99, "rating": 4.9, "reviews": 19400, "badge": "Best Seller"},
    {"title": "NuPhy Air75 V2 Low-Profile Wireless Mechanical Keyboard", "category": "Keyboards & Peripherals", "price": 139.95, "rating": 4.8, "reviews": 2840, "badge": "Travel Ready"},
    {"title": "Apple Magic Trackpad - Black Multi-Touch Surface", "category": "Keyboards & Peripherals", "price": 149.00, "rating": 4.7, "reviews": 4120, "badge": "Ergonomic"},
    {"title": "Logitech MX Keys S Advanced Illuminated Wireless Keyboard", "category": "Keyboards & Peripherals", "price": 109.99, "rating": 4.8, "reviews": 14200, "badge": "Office Pro"},
    {"title": "HHKB Professional Hybrid Type-S Silent Topre Switch Keyboard", "category": "Keyboards & Peripherals", "price": 329.00, "rating": 4.9, "reviews": 1280, "badge": "Legendary"},
    {"title": "Razer DeathAdder V3 Pro Ultra-Lightweight Wireless Gaming Mouse", "category": "Keyboards & Peripherals", "price": 149.99, "rating": 4.8, "reviews": 5600, "badge": "Speed King"},
    {"title": "Wooting 60HE Hall Effect Analog Mechanical Gaming Keyboard", "category": "Keyboards & Peripherals", "price": 174.99, "rating": 5.0, "reviews": 2900, "badge": "Hall Effect"},
    {"title": "Grovemade Wool Felt Desk Mat - Dark Extra Large", "category": "Keyboards & Peripherals", "price": 80.00, "rating": 4.8, "reviews": 3200, "badge": "Aesthetic"},
    {"title": "DeltaHub Carpio 2.0 Ergonomic Gliding Wrist Rest for Mouse", "category": "Keyboards & Peripherals", "price": 39.90, "rating": 4.6, "reviews": 4810, "badge": "Ergonomics"},

    # Creator & Studio (30-39)
    {"title": "Elgato Stream Deck MK.2 Studio Controller (15 LCD Keys)", "category": "Creator & Studio", "price": 149.99, "rating": 4.9, "reviews": 16400, "badge": "Best Seller"},
    {"title": "Shure SM7B Cardioid Dynamic Vocal Recording Microphone", "category": "Creator & Studio", "price": 399.00, "rating": 4.9, "reviews": 18200, "badge": "Broadcast Standard"},
    {"title": "Sony Alpha 7 IV Full-Frame Mirrorless Camera (Body Only)", "category": "Creator & Studio", "price": 2498.00, "rating": 4.8, "reviews": 2100, "badge": "Pro Video"},
    {"title": "Rode Rodecaster Pro II All-in-One Audio Production Studio", "category": "Creator & Studio", "price": 699.00, "rating": 4.9, "reviews": 1540, "badge": "Podcasting"},
    {"title": "Elgato Key Light Air Professional Studio Desktop LED Panel", "category": "Creator & Studio", "price": 129.99, "rating": 4.7, "reviews": 6800, "badge": "Lighting"},
    {"title": "Hollyland Lark Max Wireless Lavalier Microphone System", "category": "Creator & Studio", "price": 249.00, "rating": 4.8, "reviews": 2940, "badge": "Wireless"},
    {"title": "DJI Mic 2 Wireless Microphone with Intelligent Noise Cancelling", "category": "Creator & Studio", "price": 349.00, "rating": 4.8, "reviews": 1450, "badge": "New Release"},
    {"title": "Elgato Wave:3 Premium USB Condenser Microphone", "category": "Creator & Studio", "price": 149.99, "rating": 4.7, "reviews": 9200, "badge": "USB Plug & Play"},
    {"title": "Blackmagic Design ATEM Mini Pro HDMI Live Streaming Switcher", "category": "Creator & Studio", "price": 295.00, "rating": 4.8, "reviews": 3900, "badge": "Multi-Cam"},
    {"title": "Peak Design Everyday Backpack 30L V2 - Charcoal", "category": "Creator & Studio", "price": 299.95, "rating": 4.8, "reviews": 3100, "badge": "Travel Ready"},

    # Smart Home & Power (40-49)
    {"title": "Anker 737 Power Bank (PowerCore 24K) 140W Portable Charger", "category": "Smart Home & Power", "price": 149.99, "rating": 4.8, "reviews": 11200, "badge": "Fast Charge"},
    {"title": "Philips Hue Play Gradient PC Lightstrip 32-34\" Multi-Color", "category": "Smart Home & Power", "price": 179.99, "rating": 4.7, "reviews": 2900, "badge": "Ambient Light"},
    {"title": "Amazon Kindle Paperwhite Signature Edition 32GB Wireless Charging", "category": "Smart Home & Power", "price": 189.99, "rating": 4.8, "reviews": 24500, "badge": "Reader Choice"},
    {"title": "Apple HomePod mini Smart Speaker with Siri - Space Gray", "category": "Smart Home & Power", "price": 99.00, "rating": 4.7, "reviews": 8400, "badge": "Smart Sound"},
    {"title": "Nanoleaf Shapes Hexagons Smarter Kit (9 Light Panels)", "category": "Smart Home & Power", "price": 199.99, "rating": 4.6, "reviews": 4200, "badge": "Smart Wall"},
    {"title": "Anker Prime 240W 4-Port GaN Desktop Charger with USB-C", "category": "Smart Home & Power", "price": 199.99, "rating": 4.8, "reviews": 1800, "badge": "GaN Tech"},
    {"title": "Belkin 3-in-1 Wireless Charging Stand with MagSafe 15W", "category": "Smart Home & Power", "price": 149.99, "rating": 4.7, "reviews": 6500, "badge": "Desk Clean"},
    {"title": "Eve Energy Smart Plug & Power Meter with Thread & Matter", "category": "Smart Home & Power", "price": 39.95, "rating": 4.6, "reviews": 2300, "badge": "Matter Support"},
    {"title": "Govee RGBIC LED Floor Lamp with Music Sync Alexa Voice Control", "category": "Smart Home & Power", "price": 99.99, "rating": 4.7, "reviews": 7800, "badge": "Atmosphere"},
    {"title": "UGREEN Nexode 300W GaN Fast Charger 5-Port", "category": "Smart Home & Power", "price": 269.99, "rating": 4.8, "reviews": 950, "badge": "Mega Power"},

    # Workspace & Lifestyle (50-59)
    {"title": "Fellow Ode Gen 2 Brew Burr Coffee Grinder - Matte Black", "category": "Workspace & Lifestyle", "price": 345.00, "rating": 4.9, "reviews": 3100, "badge": "Barista Grade"},
    {"title": "Ember Temperature Control Smart Mug 2 (14 oz)", "category": "Workspace & Lifestyle", "price": 149.95, "rating": 4.6, "reviews": 8200, "badge": "Smart Warmer"},
    {"title": "Herman Miller Aeron Ergonomic Office Chair with PostureFit SL", "category": "Workspace & Lifestyle", "price": 1695.00, "rating": 4.9, "reviews": 4500, "badge": "Iconic Ergonomics"},
    {"title": "Fellow Stagg EKG Electric Gooseneck Pour-Over Kettle", "category": "Workspace & Lifestyle", "price": 195.00, "rating": 4.8, "reviews": 6400, "badge": "Precision Pour"},
    {"title": "AeroPress Clear Coffee Maker Shatterproof Tritan Espresso Maker", "category": "Workspace & Lifestyle", "price": 49.95, "rating": 4.9, "reviews": 14300, "badge": "Essential"},
    {"title": "Grovemade Solid Walnut Wood Monitor Stand Riser", "category": "Workspace & Lifestyle", "price": 140.00, "rating": 4.8, "reviews": 1800, "badge": "Crafted Wood"},
    {"title": "Uplift V2 Commercial Standing Desk 60x30 Bamboo Top", "category": "Workspace & Lifestyle", "price": 799.00, "rating": 4.9, "reviews": 9200, "badge": "Standing Desk"},
    {"title": "Kinto Travel Tumbler 500ml Stainless Steel Vacuum Insulated", "category": "Workspace & Lifestyle", "price": 38.00, "rating": 4.8, "reviews": 2900, "badge": "Minimalist"},
    {"title": "Bellroy Tech Kit Compact Cable & Accessory Travel Organizer", "category": "Workspace & Lifestyle", "price": 59.00, "rating": 4.7, "reviews": 3600, "badge": "EDC Gear"},
    {"title": "YETI Rambler 20 oz Travel Mug with Stronghold Lid", "category": "Workspace & Lifestyle", "price": 38.00, "rating": 4.8, "reviews": 16500, "badge": "Rugged"}
]

# Generate procedural real-world products for the full 500 items catalog
BRANDS_BY_CAT = {
    "Audio & Sound": ["Sony", "Bose", "Sennheiser", "Audio-Technica", "Shure", "Sonos", "JBL", "Focal", "Beyerdynamic", "Anker Soundcore"],
    "Computing & Displays": ["Apple", "Dell", "LG", "ASUS", "Samsung", "CalDigit", "BenQ", "Lenovo", "HP", "ViewSonic"],
    "Keyboards & Peripherals": ["Keychron", "Logitech", "NuPhy", "HHKB", "Razer", "SteelSeries", "Corsair", "Wooting", "Glorious", "Ducky"],
    "Creator & Studio": ["Elgato", "Shure", "Sony", "Rode", "DJI", "Blackmagic", "Hollyland", "Focusrite", "Audio-Technica", "Peak Design"],
    "Smart Home & Power": ["Anker", "Philips Hue", "Amazon", "Apple", "Nanoleaf", "Belkin", "Eve", "Govee", "UGREEN", "TP-Link"],
    "Workspace & Lifestyle": ["Fellow", "Ember", "Herman Miller", "Grovemade", "Uplift", "Kinto", "Bellroy", "YETI", "Hydro Flask", "Steelcase"]
}

ITEM_TYPES_BY_CAT = {
    "Audio & Sound": ["Wireless ANC Headphones", "True Wireless Earbuds", "Studio Reference Monitors", "Bluetooth Speaker", "DAC Headphone Amp", "In-Ear Monitors"],
    "Computing & Displays": ["4K HDR Display", "Thunderbolt 4 Dock", "Curved Ultrawide Monitor", "Pro Laptop Hub", "ScreenBar Light", "USB-C Travel Adapter"],
    "Keyboards & Peripherals": ["Wireless Custom Keyboard", "Ergonomic Performance Mouse", "Low-Profile Mechanical Keyboard", "Multi-Touch Trackpad", "Wool Desk Mat", "Wrist Rest"],
    "Creator & Studio": ["Dynamic Broadcast Mic", "Live Production Switcher", "USB Studio Mic", "LED Key Light Panel", "Wireless Lavalier System", "Studio Boom Arm"],
    "Smart Home & Power": ["140W GaN Power Bank", "Gradient Ambient Lightstrip", "Fast GaN Desktop Charger", "Smart Energy Plug", "Magnetic Wireless Stand", "Smart Speaker"],
    "Workspace & Lifestyle": ["Precision Coffee Grinder", "Smart Temperature Mug", "Ergonomic Office Chair", "Electric Gooseneck Kettle", "Solid Wood Stand", "Cable Organizer"]
}

# Cache catalog
CATALOG = {}

def _init_catalog():
    global CATALOG
    for i in range(500):
        if i < len(REAL_PRODUCTS_SEED):
            item = dict(REAL_PRODUCTS_SEED[i])
            item["item_id"] = i
            item["name"] = item["title"]
            CATALOG[i] = item
        else:
            cat_dict = CATEGORIES[i % len(CATEGORIES)]
            cat_name = cat_dict["name"]
            brand = BRANDS_BY_CAT[cat_name][(i * 3) % len(BRANDS_BY_CAT[cat_name])]
            itype = ITEM_TYPES_BY_CAT[cat_name][(i * 7) % len(ITEM_TYPES_BY_CAT[cat_name])]
            version = f"Gen {(i % 5) + 1}" if i % 2 == 0 else f"Pro {i % 10}"
            price = round(29.99 + ((i * 17) % 850), 2)
            rating = round(4.3 + (((i * 7) % 7) * 0.1), 1)
            reviews = 300 + ((i * 137) % 9500)
            badges = ["Trending", "Staff Pick", "Best Seller", "New", "Top Rated"]
            badge = badges[i % len(badges)]

            CATALOG[i] = {
                "item_id": i,
                "title": f"{brand} {itype} ({version})",
                "name": f"{brand} {itype} ({version})",
                "category": cat_name,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "badge": badge
            }

_init_catalog()

def get_item_metadata(item_id: int) -> dict:
    item_id = int(item_id)
    if item_id in CATALOG:
        item = CATALOG[item_id]
        if "name" not in item:
            item["name"] = item.get("title", f"Product #{item_id}")
        return item
    return {
        "item_id": item_id,
        "title": f"Workspace Tech Gear #{item_id}",
        "name": f"Workspace Tech Gear #{item_id}",
        "category": "Keyboards & Peripherals",
        "price": 99.99,
        "rating": 4.7,
        "reviews": 1200,
        "badge": "Popular"
    }

USER_PERSONAS = {
    0: {
        "name": "Alex Chen",
        "role": "Software Architect & Audiophile",
        "avatar": "👨‍💻",
        "segment": "High-Affinity Tech & Audio",
        "status_detail": "Warm Profile (18 views, 6 clicks, 2 purchases in Feast)",
        "affinity_tags": ["Audio", "Keyboards", "Displays"]
    },
    42: {
        "name": "Sarah Jenkins",
        "role": "Podcaster & Creative Director",
        "avatar": "🎙️",
        "segment": "Studio & Audio Creator",
        "status_detail": "Active Profile (12 views, 4 clicks, 1 purchase in Feast)",
        "affinity_tags": ["Creator", "Mics", "Lighting"]
    },
    89: {
        "name": "Marcus Vance",
        "role": "Smart Home & Automation Pro",
        "avatar": "⚡",
        "segment": "Smart Power & Office Gear",
        "status_detail": "Frequent Buyer (24 views, 9 clicks, 5 purchases in Feast)",
        "affinity_tags": ["Smart Home", "Power", "Workspace"]
    },
    999: {
        "name": "Elena Rostova",
        "role": "First-Time Guest Visitor",
        "avatar": "✨",
        "segment": "Cold-Start User (No prior interactions)",
        "status_detail": "Zero Interaction History (Triggering Popularity Fallback)",
        "affinity_tags": ["Trending", "Best Sellers"]
    }
}

def get_user_persona(user_id: int) -> dict:
    user_id = int(user_id)
    if user_id in USER_PERSONAS:
        return USER_PERSONAS[user_id]
    return {
        "name": f"User #{user_id}",
        "role": "Marketplace Customer",
        "avatar": "👤",
        "segment": "Standard Customer",
        "status_detail": "Active Customer Profile",
        "affinity_tags": ["Tech", "Peripherals"]
    }
