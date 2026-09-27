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

import re

IMAGE_COLLECTION = {
    "headphones_overear": [
        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?auto=format&fit=crop&w=600&q=80",
    ],
    "earbuds": [
        "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?auto=format&fit=crop&w=600&q=80",
    ],
    "speaker": [
        "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80",
    ],
    "laptop": [
        "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=600&q=80",
    ],
    "display": [
        "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1547082299-de196ea013d6?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1586210579191-33b45e38fa2c?auto=format&fit=crop&w=600&q=80",
    ],
    "dock_hub": [
        "https://images.unsplash.com/photo-1544652478-6653e09f18a2?auto=format&fit=crop&w=600&q=80",
    ],
    "keyboard": [
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=600&q=80",
    ],
    "mouse": [
        "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=600&q=80",
    ],
    "desk_mat": [
        "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?auto=format&fit=crop&w=600&q=80",
    ],
    "wood_stand": [
        "https://images.unsplash.com/photo-1593062096033-9a26b09da705?auto=format&fit=crop&w=600&q=80",
    ],
    "microphone": [
        "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=600&q=80",
    ],
    "camera": [
        "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1512790182412-b19e6d62bc39?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=600&q=80",
    ],
    "backpack": [
        "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80",
    ],
    "lighting": [
        "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
    ],
    "power_bank": [
        "https://upload.wikimedia.org/wikipedia/commons/7/75/Portable_power_bank.jpg",
        "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&w=600&q=80",
    ],
    "charger": [
        "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1543512214-318c7553f230?auto=format&fit=crop&w=600&q=80",
    ],
    "herman_miller": [
        "https://upload.wikimedia.org/wikipedia/commons/b/b6/Aeron_Chair_at_Design_Show_2003.jpg",
    ],
    "chair": [
        "https://images.unsplash.com/photo-1579487785947-84da60b19c09?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1505797149-43b0069ec26b?auto=format&fit=crop&w=600&q=80",
    ],
    "standing_desk": [
        "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=600&q=80",
    ],
    "coffee_maker": [
        "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=600&q=80",
    ],
    "smart_mug": [
        "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=600&q=80",
    ],
    "ereader": [
        "https://images.unsplash.com/photo-1592496431122-2349e0fbc666?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80",
    ],
    "trackpad": [
        "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
    ],
    "wrist_rest": [
        "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
    ],
    "organizer_pouch": [
        "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?auto=format&fit=crop&w=600&q=80",
    ],
    "stream_controller": [
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=600&q=80",
    ],
    "switcher": [
        "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1547082299-de196ea013d6?auto=format&fit=crop&w=600&q=80",
    ],
    "desktop_pc": [
        "https://images.unsplash.com/photo-1547082299-de196ea013d6?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1587831990711-23ca6441447b?auto=format&fit=crop&w=600&q=80",
    ],
    "smartwatch": [
        "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80",
    ],
    "running_shoes": [
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=600&q=80",
    ],
    "strength": [
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=600&q=80",
    ],
    "yoga_mat": [
        "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?auto=format&fit=crop&w=600&q=80",
    ],
    "bottle_shaker": [
        "https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1593095948071-474c5cc2989d?auto=format&fit=crop&w=600&q=80",
    ],
    "fitness": [
        "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?auto=format&fit=crop&w=600&q=80",
    ],
}

PATTERNS = [
    ("herman_miller", re.compile(r"\b(herman miller|aeron)\b", re.I)),
    ("ereader", re.compile(r"\b(kindle|e-reader|ereader|paperwhite)\b", re.I)),
    ("trackpad", re.compile(r"\b(trackpad|trackpads|magic trackpad)\b", re.I)),
    ("wrist_rest", re.compile(r"\b(wrist rest|wristrest|carpio)\b", re.I)),
    ("organizer_pouch", re.compile(r"\b(organizer|tech kit|travel kit|pouch)\b", re.I)),
    ("stream_controller", re.compile(r"\b(stream deck|lcd keys|studio controller)\b", re.I)),
    ("switcher", re.compile(r"\b(atem|switcher|live streaming switcher)\b", re.I)),
    ("desktop_pc", re.compile(r"\b(mac studio|mac mini|desktop pc|mini pc)\b", re.I)),
    ("smartwatch", re.compile(r"\b(smartwatch|smart watch|forerunner|apple watch|watch ultra|gps watch|fitness tracker|fitbit|garmin|amazfit)\b", re.I)),
    ("running_shoes", re.compile(r"\b(running shoe|running shoes|sneaker|sneakers|trail runner|pegasus|ultraboost|vaporfly|Clifton|Speedgoat)\b", re.I)),
    ("strength", re.compile(r"\b(dumbbell|dumbbells|kettlebell|barbell|weight|weights|strength|power rack|squat rack|bench press)\b", re.I)),
    ("yoga_mat", re.compile(r"\b(yoga mat|yoga|pilates|foam roller|mobility)\b", re.I)),
    ("bottle_shaker", re.compile(r"\b(shaker|protein shaker|water bottle|insulated bottle|hydration bottle|sport bottle)\b", re.I)),
    ("earbuds", re.compile(r"\b(earbud|earbuds|in-ear|ear \(2\)|airpods pro|soundsport|sport earbuds)\b", re.I)),
    ("headphones_overear", re.compile(r"\b(headphone|headphones|headset|headsets|wh-1000xm|airpods max|bathys|ath-m50x|aonic|hd 660s2|dac)\b", re.I)),
    ("speaker", re.compile(r"\b(speaker|speakers|stanmore|era 300|soundcore|homepod)\b", re.I)),
    ("microphone", re.compile(r"\b(mic|mics|microphone|microphones|sm7b|wave:3|lark|rodecaster|boom arm)\b", re.I)),
    ("camera", re.compile(r"\b(camera|cameras|mirrorless|dslr|alpha 7)\b", re.I)),
    ("backpack", re.compile(r"\b(backpack|backpacks|duffel|gym bag|everyday backpack)\b", re.I)),
    ("lighting", re.compile(r"\b(screenbar|light|lights|lightstrip|lightstrips|lamp|lamps|nanoleaf|hue)\b", re.I)),
    ("desk_mat", re.compile(r"\b(desk mat|desk pad)\b", re.I)),
    ("wood_stand", re.compile(r"\b(monitor stand|desk shelf|riser|wood stand)\b", re.I)),
    ("display", re.compile(r"\b(monitor|monitors|display|displays|ultrasharp|ultrawide|proart|odyssey)\b", re.I)),
    ("dock_hub", re.compile(r"\b(dock|docks|docking|hub|hubs|adapter|adapters)\b", re.I)),
    ("power_bank", re.compile(r"\b(power bank|powercore|battery|portable charger)\b", re.I)),
    ("charger", re.compile(r"\b(charger|chargers|charging|gan|magsafe|magnetic wireless|plug|power meter)\b", re.I)),
    ("standing_desk", re.compile(r"\b(standing desk|uplift)\b", re.I)),
    ("fitness", re.compile(r"\b(fitness|workout|gym|athletic|recovery|massage gun|jump rope|resistance band|athleisure|training)\b", re.I)),
    ("chair", re.compile(r"\b(chair|chairs|steelcase|seating)\b", re.I)),
    ("coffee_maker", re.compile(r"\b(coffee|grinder|kettle|aeropress|pour-over|brew)\b", re.I)),
    ("smart_mug", re.compile(r"\b(mug|mugs|tumbler|tumblers|cup|kinto|yeti|ember)\b", re.I)),
    ("keyboard", re.compile(r"\b(keyboard|keyboards|keychron|nuphy|hhkb|wooting|mechanical)\b", re.I)),
    ("mouse", re.compile(r"\b(mouse|mice|deathadder|mx master)\b", re.I)),
    ("laptop", re.compile(r"\b(macbook|laptop|laptops|thinkpad|ultrabook|notebook)\b", re.I)),
]

def get_product_image(item_id: int, title: str, category: str) -> str:
    """Return high-resolution, matching tech product photography based on product title and category."""
    for pool_name, pattern in PATTERNS:
        if pattern.search(title):
            pool = IMAGE_COLLECTION[pool_name]
            return pool[item_id % len(pool)]

    cat_lower = category.lower()
    if "audio" in cat_lower:
        pool = IMAGE_COLLECTION["headphones_overear"] + IMAGE_COLLECTION["earbuds"]
    elif "display" in cat_lower or "computing" in cat_lower:
        pool = IMAGE_COLLECTION["display"] + IMAGE_COLLECTION["laptop"]
    elif "keyboard" in cat_lower or "peripheral" in cat_lower:
        pool = IMAGE_COLLECTION["keyboard"] + IMAGE_COLLECTION["mouse"]
    elif "creator" in cat_lower or "studio" in cat_lower:
        pool = IMAGE_COLLECTION["microphone"] + IMAGE_COLLECTION["camera"]
    elif "power" in cat_lower or "smart" in cat_lower:
        pool = IMAGE_COLLECTION["charger"] + IMAGE_COLLECTION["power_bank"]
    else:
        pool = IMAGE_COLLECTION["chair"] + IMAGE_COLLECTION["standing_desk"] + IMAGE_COLLECTION["coffee_maker"]

    return pool[item_id % len(pool)]

# Cache catalog
CATALOG = {}

# Curated fitness & athletic performance lineup for Max Sterling (persona 55).
# IDs 480-499 override procedural filler so Max has high-affinity matches
# while keeping all 6 category vectors / 8-dim model unchanged.
# Categories reuse the existing 6 so Two-Tower embeddings stay compatible.
MAX_STERLING_FITNESS_PRODUCTS = [
    {"title": "Garmin Forerunner 965 GPS Running Smartwatch with AMOLED Display", "category": "Workspace & Lifestyle", "price": 599.99, "rating": 4.8, "reviews": 3240, "badge": "Athlete Pick", "description": "Multisport GPS running smartwatch with wrist-based heart rate, training readiness and AMOLED display for serious runners."},
    {"title": "Apple Watch Ultra 2 Trail Loop GPS Fitness Tracker - Titanium", "category": "Workspace & Lifestyle", "price": 799.00, "rating": 4.9, "reviews": 5120, "badge": "Premium", "description": "Rugged titanium fitness tracker smartwatch with dual-frequency GPS, trail loop band and 36-hour battery for outdoor athletes."},
    {"title": "Bose SoundSport Wireless Fitness Earbuds with Heart-Rate Monitoring", "category": "Audio & Sound", "price": 199.00, "rating": 4.7, "reviews": 6840, "badge": "Workout Ready", "description": "Sweat-resistant wireless fitness earbuds with secure sport fit, heart-rate monitoring and punchy bass for training sessions."},
    {"title": "Jabra Elite 8 Active Workout Earbuds - ShakeGrip Sport Fit", "category": "Audio & Sound", "price": 179.99, "rating": 4.6, "reviews": 2930, "badge": "Sport Fit", "description": "Durable workout earbuds with ShakeGrip coating, adaptive noise cancellation and military-grade durability for gym training."},
    {"title": "Nike Pegasus Trail Running Shoes - Responsive Athletic Footwear", "category": "Workspace & Lifestyle", "price": 149.95, "rating": 4.8, "reviews": 8210, "badge": "Runner Favorite", "description": "Responsive trail running shoes with React foam cushioning and grippy outsole for road-to-trail athletic performance."},
    {"title": "Adidas Ultraboost Light Running Sneakers for Daily Training", "category": "Workspace & Lifestyle", "price": 189.99, "rating": 4.7, "reviews": 6450, "badge": "Best Seller", "description": "Lightweight daily training running sneakers with Boost midsole energy return for runners and gym athletes."},
    {"title": "Bowflex SelectTech Adjustable Dumbbell Pair - Strength Training", "category": "Workspace & Lifestyle", "price": 379.00, "rating": 4.9, "reviews": 11200, "badge": "Strength Pick", "description": "Space-saving adjustable dumbbell pair replacing 15 weight sets, ideal for home gym strength training and progressive overload."},
    {"title": "Kettlebell Kings Powder-Coat Kettlebell for Strength Workouts", "category": "Workspace & Lifestyle", "price": 89.00, "rating": 4.8, "reviews": 4310, "badge": "Gym Essential", "description": "Single-piece cast-iron kettlebell with powder-coat grip for swings, snatches and full-body strength workouts."},
    {"title": "Manduka PRO Yoga Mat 6mm - Extra Thick Athletic Recovery Mat", "category": "Workspace & Lifestyle", "price": 128.00, "rating": 4.8, "reviews": 5670, "badge": "Yoga Pro", "description": "Ultra-dense 6mm yoga mat with superior joint protection and grip for stretching, mobility and athletic recovery."},
    {"title": "TriggerPoint GRID Foam Roller for Mobility and Muscle Recovery", "category": "Workspace & Lifestyle", "price": 34.99, "rating": 4.8, "reviews": 18900, "badge": "Recovery", "description": "Multi-density foam roller for deep-tissue mobility work, post-workout muscle recovery and flexibility training."},
    {"title": "Hydro Flask Wide Mouth Insulated Sport Water Bottle 32 oz", "category": "Workspace & Lifestyle", "price": 44.95, "rating": 4.9, "reviews": 22400, "badge": "Hydration", "description": "Double-wall vacuum insulated sport water bottle keeping drinks cold for 24 hours through workouts and trail runs."},
    {"title": "BlenderBottle Classic Protein Shaker with Wire Whisk 28 oz", "category": "Workspace & Lifestyle", "price": 12.99, "rating": 4.8, "reviews": 31200, "badge": "Gym Staple", "description": "Leak-proof protein shaker with stainless whisk ball for smooth shakes, pre-workout and post-training nutrition."},
    {"title": "Theragun Mini Massage Gun for Athletic Recovery", "category": "Workspace & Lifestyle", "price": 199.00, "rating": 4.7, "reviews": 7860, "badge": "Recovery Pro", "description": "Compact percussive massage gun with 3 speeds for on-the-go athletic recovery, warm-up and soreness relief."},
    {"title": "Fitbit Charge 6 Fitness Tracker with Heart Rate and GPS", "category": "Workspace & Lifestyle", "price": 159.95, "rating": 4.6, "reviews": 9410, "badge": "Tracker", "description": "Slim fitness tracker with continuous heart rate, built-in GPS and 7-day battery for all-day activity and sleep tracking."},
    {"title": "Withings Body Smart Fitness Scale with App Sync and Coaching", "category": "Workspace & Lifestyle", "price": 99.95, "rating": 4.7, "reviews": 5120, "badge": "Smart Health", "description": "Wi-Fi connected smart fitness scale measuring weight, body composition and heart health with automatic app sync."},
    {"title": "Under Armour Athletic Training Duffel Gym Bag 40L", "category": "Workspace & Lifestyle", "price": 65.00, "rating": 4.7, "reviews": 3890, "badge": "Gym Bag", "description": "Durable 40L athletic training duffel gym bag with ventilated shoe pocket and water-resistant finish for daily workouts."},
    {"title": "Sony Float Run Wireless Workout Headphones - Off-Ear Sport Fit", "category": "Audio & Sound", "price": 129.99, "rating": 4.6, "reviews": 2140, "badge": "Run Ready", "description": "Off-ear wireless workout headphones that stay stable while running, with ambient awareness for safe outdoor training."},
    {"title": "Beats Powerbeats Pro Athletic Earbuds with Ear Hooks", "category": "Audio & Sound", "price": 249.99, "rating": 4.7, "reviews": 15300, "badge": "Athletic", "description": "Secure-fit athletic earbuds with adjustable ear hooks, sweat resistance and 9-hour battery for intense gym sessions."},
    {"title": "Gaiam Athletic Resistance Band Set - 3 Levels for Strength Training", "category": "Workspace & Lifestyle", "price": 24.98, "rating": 4.6, "reviews": 9780, "badge": "Training", "description": "Set of 3 athletic resistance bands for strength training, physical therapy, warm-ups and full-body home workouts."},
    {"title": "Nike Dri-FIT Athletic Training Jump Rope with Weighted Handles", "category": "Workspace & Lifestyle", "price": 29.99, "rating": 4.5, "reviews": 3420, "badge": "Cardio", "description": "Adjustable athletic jump rope with weighted handles and smooth bearings for cardio conditioning and boxing training."},
]

def _init_catalog():
    global CATALOG
    for i in range(500):
        # Max Sterling fitness lineup occupies the tail (480-499) so the
        # 0-59 flagship seeds and low-ID embeddings stay stable.
        if 480 <= i < 480 + len(MAX_STERLING_FITNESS_PRODUCTS):
            item = dict(MAX_STERLING_FITNESS_PRODUCTS[i - 480])
            item["item_id"] = i
            item["name"] = item["title"]
            item["image_url"] = get_product_image(i, item["title"], item["category"])
            CATALOG[i] = item
        elif i < len(REAL_PRODUCTS_SEED):
            item = dict(REAL_PRODUCTS_SEED[i])
            item["item_id"] = i
            item["name"] = item["title"]
            item["image_url"] = get_product_image(i, item["title"], item["category"])
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
            item_title = f"{brand} {itype} ({version})"

            CATALOG[i] = {
                "item_id": i,
                "title": item_title,
                "name": item_title,
                "category": cat_name,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "badge": badge,
                "image_url": get_product_image(i, item_title, cat_name),
            }

_init_catalog()

def get_item_metadata(item_id: int) -> dict:
    item_id = int(item_id)
    if item_id in CATALOG:
        item = CATALOG[item_id]
        if "name" not in item:
            item["name"] = item.get("title", f"Product #{item_id}")
        if "image_url" not in item:
            item["image_url"] = get_product_image(item_id, item.get("title", ""), item.get("category", ""))
        return item
    title = f"Workspace Tech Gear #{item_id}"
    cat = "Keyboards & Peripherals"
    return {
        "item_id": item_id,
        "title": title,
        "name": title,
        "category": cat,
        "price": 99.99,
        "rating": 4.7,
        "reviews": 1200,
        "badge": "Popular",
        "image_url": get_product_image(item_id, title, cat),
    }

CAT_NAME_TO_INDEX = {
    "Audio & Sound": 0,
    "Computing & Displays": 1,
    "Keyboards & Peripherals": 2,
    "Creator & Studio": 3,
    "Smart Home & Power": 4,
    "Workspace & Lifestyle": 5,
}

INDEX_TO_CAT_NAME = {v: k for k, v in CAT_NAME_TO_INDEX.items()}

def get_item_feature_vector(item_id: int):
    """
    Returns an 8-dimensional feature vector for item_id:
    Dims 0..5: Normalized category distribution
    Dim 6: Normalized price (price / 1000)
    Dim 7: Normalized rating (rating / 5.0)
    """
    import numpy as np
    meta = get_item_metadata(item_id)
    cat = meta.get("category", "Audio & Sound")
    idx = CAT_NAME_TO_INDEX.get(cat, 0)
    vec = np.zeros(8, dtype=np.float32)
    vec[idx] = 1.0

    # Cross-category affinity
    if cat == "Audio & Sound":
        vec[3] = 0.15  # Audio gear complements creator & studio
    elif cat == "Creator & Studio":
        vec[0] = 0.20  # Creator studio uses audio gear
    elif cat == "Computing & Displays":
        vec[2] = 0.25  # Displays use keyboards
    elif cat == "Keyboards & Peripherals":
        vec[1] = 0.25  # Keyboards connect to computers
    elif cat == "Workspace & Lifestyle":
        vec[1] = 0.15
        vec[2] = 0.15

    price = float(meta.get("price", 99.0))
    rating = float(meta.get("rating", 4.5))
    vec[6] = min(price / 1000.0, 1.0)
    vec[7] = min(rating / 5.0, 1.0)
    return vec

USER_PERSONAS = {
    0: {
        "name": "Alex Chen",
        "role": "Audiophile & Music Producer",
        "avatar": "🎧",
        "segment": "Audio & Hi-Fi Gear",
        "status_detail": "Warm Profile (18 views, 6 clicks, 2 purchases in Feast)",
        "affinity_tags": ["Audio & Sound", "Creator & Studio"],
        "primary_cat": "Audio & Sound",
        "primary_cat_idx": 0,
        "views": 18, "clicks": 6, "purchases": 2,
        "feature_vector": [1.0, 0.05, 0.0, 0.15, 0.0, 0.0, 0.85, 0.95],
    },
    12: {
        "name": "Devon Brooks",
        "role": "Mechanical Keyboard Modder",
        "avatar": "⌨️",
        "segment": "Custom Keyboards & Desk Gear",
        "status_detail": "Mechanical Enthusiast (28 views, 12 clicks, 4 purchases in Feast)",
        "affinity_tags": ["Keyboards & Peripherals", "Computing & Displays"],
        "primary_cat": "Keyboards & Peripherals",
        "primary_cat_idx": 2,
        "views": 28, "clicks": 12, "purchases": 4,
        "feature_vector": [0.0, 0.15, 1.0, 0.0, 0.0, 0.25, 0.75, 0.92],
    },
    15: {
        "name": "Liam Thorne",
        "role": "Smart Home & Power Architect",
        "avatar": "⚡",
        "segment": "GaN Fast Chargers & Smart IoT",
        "status_detail": "Power User (22 views, 8 clicks, 3 purchases in Feast)",
        "affinity_tags": ["Smart Home & Power", "Computing & Displays"],
        "primary_cat": "Smart Home & Power",
        "primary_cat_idx": 4,
        "views": 22, "clicks": 8, "purchases": 3,
        "feature_vector": [0.0, 0.20, 0.0, 0.05, 1.0, 0.10, 0.65, 0.88],
    },
    42: {
        "name": "Sarah Jenkins",
        "role": "Podcaster & Creative Director",
        "avatar": "🎙️",
        "segment": "Cameras, Lights & Studio Gear",
        "status_detail": "Active Profile (14 views, 5 clicks, 1 purchase in Feast)",
        "affinity_tags": ["Creator & Studio", "Audio & Sound"],
        "primary_cat": "Creator & Studio",
        "primary_cat_idx": 3,
        "views": 14, "clicks": 5, "purchases": 1,
        "feature_vector": [0.15, 0.05, 0.0, 1.0, 0.05, 0.0, 0.70, 0.90],
    },
    64: {
        "name": "Chloe Rivera",
        "role": "Ergonomics & Interior Architect",
        "avatar": "🪴",
        "segment": "Premium Ergonomics & Lifestyle",
        "status_detail": "Design Aficionado (32 views, 11 clicks, 6 purchases in Feast)",
        "affinity_tags": ["Workspace & Lifestyle", "Keyboards & Peripherals"],
        "primary_cat": "Workspace & Lifestyle",
        "primary_cat_idx": 5,
        "views": 32, "clicks": 11, "purchases": 6,
        "feature_vector": [0.0, 0.0, 0.15, 0.0, 0.10, 1.0, 0.90, 0.95],
    },
    89: {
        "name": "Marcus Vance",
        "role": "Workplace Minimalist",
        "avatar": "💻",
        "segment": "Displays, Docks & Ultrabooks",
        "status_detail": "Frequent Buyer (24 views, 9 clicks, 5 purchases in Feast)",
        "affinity_tags": ["Computing & Displays", "Keyboards & Peripherals"],
        "primary_cat": "Computing & Displays",
        "primary_cat_idx": 1,
        "views": 24, "clicks": 9, "purchases": 5,
        "feature_vector": [0.0, 0.95, 0.20, 0.0, 0.10, 0.15, 0.85, 0.90],
    },
    55: {
        "name": "Max Sterling",
        "role": "Fitness & Athletic Performance Tech",
        "avatar": "🏋️",
        "segment": "Fitness Tech & Athletic Lifestyle",
        "status_detail": "High-Activity Athlete (26 views, 10 clicks, 4 purchases in Feast)",
        "affinity_tags": ["Workspace & Lifestyle", "Audio & Sound", "Smart Home & Power"],
        "primary_cat": "Workspace & Lifestyle",
        "primary_cat_idx": 5,
        "secondary_cat": "Audio & Sound",
        "views": 26, "clicks": 10, "purchases": 4,
        "feature_vector": [0.35, 0.0, 0.0, 0.0, 0.20, 0.85, 0.65, 0.95],
    },
    999: {
        "name": "Elena Rostova",
        "role": "First-Time Guest Visitor",
        "avatar": "✨",
        "segment": "Cold-Start (Popularity Fallback)",
        "status_detail": "Zero Interaction History (Triggering Popularity Fallback)",
        "affinity_tags": ["Trending", "Best Sellers"],
        "primary_cat": None,
        "primary_cat_idx": None,
        "views": 0, "clicks": 0, "purchases": 0,
        "feature_vector": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
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
        "affinity_tags": ["Tech", "Peripherals"],
        "primary_cat": "Audio & Sound",
        "primary_cat_idx": 0,
        "views": 1, "clicks": 0, "purchases": 0,
        "feature_vector": [0.5, 0.3, 0.2, 0.0, 0.0, 0.0, 0.5, 0.8],
    }

