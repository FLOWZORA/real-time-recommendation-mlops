# Curated storewide best-sellers across diverse categories for cold-start exploration
FLAGSHIP_POPULAR_ITEMS = [
    0,   # Sony WH-1000XM5 Noise Canceling Wireless Headphones (Audio & Sound)
    10,  # Apple MacBook Pro 16" M3 Max (Computing & Displays)
    21,  # Logitech MX Master 3S Advanced Wireless Ergonomic Mouse (Keyboards & Peripherals)
    31,  # Shure SM7B Cardioid Dynamic Vocal Recording Microphone (Creator & Studio)
    40,  # Anker 737 Power Bank 140W Portable Charger (Smart Home & Power)
    52,  # Herman Miller Aeron Ergonomic Office Chair (Workspace & Lifestyle)
    3,   # Sennheiser HD 660S2 Dynamic Audiophile Headphones (Audio & Sound)
    11,  # Dell UltraSharp 32" 4K UHD USB-C Hub Monitor (Computing & Displays)
    20,  # Keychron Q1 Pro Wireless Custom Mechanical Keyboard (Keyboards & Peripherals)
    30,  # Elgato Stream Deck MK.2 Studio Controller (Creator & Studio)
    1,   # Bose QuietComfort Ultra Earbuds (Audio & Sound)
    50,  # Fellow Ode Gen 2 Brew Burr Coffee Grinder (Workspace & Lifestyle)
]

def popular_items(k=10):
    return FLAGSHIP_POPULAR_ITEMS[:k]

POPULAR_ITEMS = FLAGSHIP_POPULAR_ITEMS

