/**
 * Tech hardware product photography matcher.
 * Maps product title keywords and categories to verified high-resolution tech gear photos.
 */

const FALLBACK_COLLECTIONS: Record<string, string[]> = {
  earbuds: [
    "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?auto=format&fit=crop&w=600&q=80",
  ],
  headphones_overear: [
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?auto=format&fit=crop&w=600&q=80",
  ],
  speaker: [
    "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80",
  ],
  microphone: [
    "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?auto=format&fit=crop&w=600&q=80",
  ],
  camera: [
    "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1512790182412-b19e6d62bc39?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=600&q=80",
  ],
  backpack: [
    "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80",
  ],
  lighting: [
    "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
  ],
  desk_mat: [
    "https://images.unsplash.com/photo-1600080972464-8e5f35f63d08?auto=format&fit=crop&w=600&q=80",
  ],
  wood_stand: [
    "https://images.unsplash.com/photo-1593062096033-9a26b09da705?auto=format&fit=crop&w=600&q=80",
  ],
  display: [
    "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1547082299-de196ea013d6?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1586210579191-33b45e38fa2c?auto=format&fit=crop&w=600&q=80",
  ],
  dock_hub: [
    "https://images.unsplash.com/photo-1544652478-6653e09f18a2?auto=format&fit=crop&w=600&q=80",
  ],
  power_bank: [
    "https://images.unsplash.com/photo-1621259182978-fbf93132d53d?auto=format&fit=crop&w=600&q=80",
  ],
  charger: [
    "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1543512214-318c7553f230?auto=format&fit=crop&w=600&q=80",
  ],
  standing_desk: [
    "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=600&q=80",
  ],
  chair: [
    "https://images.unsplash.com/photo-1589384267710-7a170981ca78?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1592078615290-033ee584e267?auto=format&fit=crop&w=600&q=80",
  ],
  coffee_maker: [
    "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=600&q=80",
  ],
  smart_mug: [
    "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=600&q=80",
  ],
  keyboard: [
    "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=600&q=80",
  ],
  mouse: [
    "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=600&q=80",
  ],
  laptop: [
    "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=600&q=80",
    "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=600&q=80",
  ],
};

const PATTERNS: [string, RegExp][] = [
  ["earbuds", /\b(earbud|earbuds|in-ear|ear \(2\)|airpods pro)\b/i],
  ["headphones_overear", /\b(headphone|headphones|headset|headsets|wh-1000xm|airpods max|bathys|ath-m50x|aonic|hd 660s2|dac)\b/i],
  ["speaker", /\b(speaker|speakers|stanmore|era 300|soundcore|homepod)\b/i],
  ["microphone", /\b(mic|mics|microphone|microphones|sm7b|wave:3|lark|rodecaster|boom arm)\b/i],
  ["camera", /\b(camera|cameras|mirrorless|dslr|alpha 7|atem|switcher|stream deck)\b/i],
  ["backpack", /\b(backpack|bag|bags|organizer|tech kit)\b/i],
  ["lighting", /\b(screenbar|light|lights|lightstrip|lightstrips|lamp|lamps|nanoleaf|hue)\b/i],
  ["desk_mat", /\b(desk mat|wrist rest|carpio|desk pad)\b/i],
  ["wood_stand", /\b(monitor stand|desk shelf|riser|wood stand)\b/i],
  ["display", /\b(monitor|monitors|display|displays|ultrasharp|ultrawide|proart|odyssey)\b/i],
  ["dock_hub", /\b(dock|docks|docking|hub|hubs|adapter|adapters)\b/i],
  ["power_bank", /\b(power bank|powercore|battery|kindle)\b/i],
  ["charger", /\b(charger|chargers|charging|gan|magsafe|magnetic wireless|plug|power meter)\b/i],
  ["standing_desk", /\b(standing desk|uplift)\b/i],
  ["chair", /\b(chair|chairs|aeron|steelcase|seating)\b/i],
  ["coffee_maker", /\b(coffee|grinder|kettle|aeropress|pour-over|brew)\b/i],
  ["smart_mug", /\b(mug|mugs|tumbler|tumblers|cup|kinto|yeti|ember)\b/i],
  ["keyboard", /\b(keyboard|keyboards|keychron|nuphy|hhkb|wooting|mechanical)\b/i],
  ["mouse", /\b(mouse|mice|trackpad|trackpads|deathadder|mx master)\b/i],
  ["laptop", /\b(macbook|laptop|laptops|thinkpad|ultrabook|mac studio|notebook)\b/i],
];

export function getProductImageUrl(
  imageUrl?: string | null,
  title?: string,
  category?: string,
  itemId?: number
): string {
  // If the image URL is already valid and NOT a random picsum placeholder, use it
  if (imageUrl && !imageUrl.includes("picsum.photos")) {
    return imageUrl;
  }

  const numericId = typeof itemId === "number" && !isNaN(itemId) ? itemId : 0;
  const t = title || "";

  for (const [poolName, pattern] of PATTERNS) {
    if (pattern.test(t)) {
      const pool = FALLBACK_COLLECTIONS[poolName];
      return pool[numericId % pool.length];
    }
  }

  const catLower = (category || "").toLowerCase();
  let pool = FALLBACK_COLLECTIONS.headphones_overear;

  if (catLower.includes("audio")) {
    pool = [...FALLBACK_COLLECTIONS.headphones_overear, ...FALLBACK_COLLECTIONS.earbuds];
  } else if (catLower.includes("display") || catLower.includes("computing")) {
    pool = [...FALLBACK_COLLECTIONS.display, ...FALLBACK_COLLECTIONS.laptop];
  } else if (catLower.includes("keyboard") || catLower.includes("peripheral")) {
    pool = [...FALLBACK_COLLECTIONS.keyboard, ...FALLBACK_COLLECTIONS.mouse];
  } else if (catLower.includes("creator") || catLower.includes("studio")) {
    pool = [...FALLBACK_COLLECTIONS.microphone, ...FALLBACK_COLLECTIONS.camera];
  } else if (catLower.includes("power") || catLower.includes("smart")) {
    pool = [...FALLBACK_COLLECTIONS.charger, ...FALLBACK_COLLECTIONS.power_bank];
  } else {
    pool = [...FALLBACK_COLLECTIONS.chair, ...FALLBACK_COLLECTIONS.standing_desk, ...FALLBACK_COLLECTIONS.coffee_maker];
  }

  return pool[numericId % pool.length];
}
