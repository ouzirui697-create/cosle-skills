# COSMO Framework Reference

## Source
Yu et al. (2024). COSMO: A Large-Scale E-commerce Common Sense Knowledge Generation and Serving System at Amazon. SIGMOD-Companion '24.

---

## The 15 COSMO Relation Types

COSMO organizes e-commerce knowledge into 15 relation types organized as (head_entity, relation, tail_entity) triples. Each relation maps to an intent level and Rufus Prompt pattern.

| Relation | English Name | Tail Type | E-commerce Example | Intent Level | Rufus Prompt Form | Conversion |
|----------|-------------|-----------|-------------------|--------------|-------------------|------------|
| `capable_of` | Capable of | Function/Usage | "portable router capable of gigabit speeds" | **L1 高典型性** | Does [brand] have a [product] with [feature]? | ★★★★★ |
| `used_for_func` | Used for Func | Function/Usage | "travel router used for securing hotel WiFi" | **L1 高典型性** | Does [brand] have a [product] for [function]? | ★★★★☆ |
| `used_to` | Used to | Function/Usage | "router used to create private WiFi hotspot" | **L1 高典型性** | Does [brand] have [product] to [action]? | ★★★★☆ |
| `xWant` | xWant | Activity | "buyer wants to secure public WiFi connection" | **L1 高典型性** | Does [brand] have [product] that [outcome]? | ★★★★☆ |
| `used_for_eve` | Used for Event | Event/Activity | "portable router used for RV camping trips" | **L2 中典型性** | What [brand] router works for [event]? | ★★★☆☆ |
| `used_for_aud` | Used for Aud | Audience | "VPN router for remote workers / travelers" | **L2 中典型性** | What [brand] router is best for [audience]? | ★★★☆☆ |
| `used_as` | Used as | Concept/Product | "device used as mobile WiFi repeater" | **L2 中典型性** | [Brand] [product] used as [role] | ★★★☆☆ |
| `used_on` | Used on | Time/Season/Event | "router used on international business trips" | **L2 中典型性** | [Brand] router for [occasion] | ★★★☆☆ |
| `used_in_loc` | Used in Loc | Location/Facility | "portable router used in hotels/airports" | **L2 中典型性** | Does [brand] router work in [location]? | ★★★☆☆ |
| `used_with` | Used with | Complementary | "router used with VPN subscription services" | **L2 中典型性** | What [brand] product works with [accessory]? | ★★★☆☆ |
| `used_by` | Used by | Audience | "router used by digital nomads / IT professionals" | **L2 中典型性** | What [brand] router is used by [user type]? | ★★★☆☆ |
| `xIs_a` | xIs a | Audience | "buyer is a frequent traveler / remote worker" | **L2 中典型性** | Best [product] for [user persona]? | ★★★☆☆ |
| `used_in_body` | Used in Body | Body Part | "serum used on face/neck" | **L2 中典型性** | Does [brand] [product] work for [body area]? | ★★☆☆☆ |
| `is_a` | Is a | Concept/Type | "GL-MT3000 is a portable travel router" | **L3 低典型性** | [Brand] [product type] | ★★☆☆☆ |
| `xInterested_in` | xInterested in | Interest | "customers interested in network security" | **L3 低典型性** | Why choose [brand] for [interest area]? | ★☆☆☆☆ |

---

## Intent Level Definitions

### L1 — 高典型性 (High Typicality)
- Buyer has **specific functional requirement**
- COSMO can match product to query via precise capability triple
- Listing must contain **exact numbers and specs** to achieve high typicality score
- **75% of purchases** in test data came from L1 Prompts
- Action: Keep and boost bids after verifying listing quality

### L2 — 中典型性 (Medium Typicality)
- Buyer has scenario/audience/occasion context but no specific feature requirement
- Rufus gives broader answers, lower conversion
- Listing should include relevant scene/audience keywords
- Action: Monitor, optimize listing for scene coverage, don't over-invest in bids

### L3 — 低典型性 (Low Typicality)
- Generic brand questions or pure category browsing
- Rufus often answers with a different (competitor) product
- Near-zero conversion, negative ROI once CPC billing starts
- Action: **Pause immediately** when CPC billing activates

---

## Typicality Scoring Principles

From §3.3.2 of the COSMO paper — "Typicality annotation":

**High typicality** (score 8–10): 
- Contains exact numbers: "capable of drilling 20mm concrete in 5 seconds"
- Comparative specs: "6× thinner than standard wefts"
- Specific materials + grade: "Grade 12A 100% unprocessed Brazilian virgin human hair"
- Precise capacity: "handles up to 120 simultaneous device connections"

**Medium typicality** (score 5–7):
- Functional but vague: "capable of connecting multiple devices"
- Partial spec: "100% human hair" without grade or origin
- Scene without detail: "suitable for travel"

**Low typicality** (score 1–4):
- Pure adjectives: "high quality", "comfortable", "natural-looking"
- Generic brand statement: "trusted by millions"
- No functional information

**The Apple Watch anti-example**: A listing that says "for fitness tracking" is low typicality. "Capable of measuring blood oxygen with ±2% accuracy" is high typicality. The distinction is always: can COSMO extract a specific capability triple from your description?

---

## ESCI Match Classification

From §4.1 of the paper — when COSMO evaluates relevance between a Prompt and a product:

| ESCI Type | Meaning | Typical Situation | Action |
|-----------|---------|-------------------|--------|
| **Exact** | Product perfectly answers the Prompt | L1 Prompt, listing describes the feature | Boost bid |
| **Substitute** | Similar product, but not ideal match | Feature exists but described vaguely | Fix listing, then re-evaluate |
| **Complement** | Related product, not a direct match | Correct category, wrong intent | Monitor or pause |
| **Irrelevant** | Product doesn't match the Prompt at all | Wrong ASIN shown, or L3 mismatch | Pause immediately |

---

## Category-Specific Examples

### Hair & Beauty
- **capable_of** high typicality: "capable of being dyed up to 3 shades lighter without damage" / "holds style for 72+ hours in humidity"
- **capable_of** low typicality: "made of real human hair" / "natural look"
- **used_for_aud** example: "designed for women with fine hair seeking volume"
- **used_for_eve** example: "perfect for wedding day, graduation, special occasions"

### Electronics/Routers
- **capable_of** high typicality: "capable of 1800Mbps dual-band throughput with 120 simultaneous devices"
- **capable_of** low typicality: "fast WiFi" / "supports multiple devices"

### Apparel
- **capable_of** high typicality: "capable of wicking 150ml/hour moisture; UPF 50+ UV protection"
- **used_for_eve** example: "designed for marathon training on asphalt"
- **used_in_body** example: "targets core temperature regulation via mesh underarm panels"

### Home & Kitchen
- **capable_of** high typicality: "capable of maintaining 165°F for 6 hours; 6-quart capacity feeds 8 adults"
- **used_with** example: "compatible with all standard induction cooktops (1800W–3500W)"

---

## Semantic Gap Bridging (§4.1)

COSMO bridges the "semantic gap" between buyer queries and product listings using the knowledge graph. The cross-encoder uses:

```
Relevance(Q, P) = f(Q, P, COSMO_knowledge(Q, P))
```

Where `COSMO_knowledge` adds commonsense triples like:
- "winter clothes" → [capable_of keeping warm] → matches "insulated jacket"
- "pre-installed VPN" → [capable_of connecting VPN instantly] → matches listing with explicit "pre-installed"

**Implication**: Your listing text feeds directly into COSMO's knowledge extraction. If your listing says "supports VPN", COSMO generates a weaker triple than if you say "pre-installed OpenVPN and WireGuard — connect to 30+ providers in seconds without setup".

---

## Multi-Turn Navigation (§4.3)

COSMO builds a hierarchy from coarse to fine:
- camping → winter camping → winter camping sleeping bag → insulated sleeping bag for -20°C

For sellers: having BOTH broad L2 terms (camping) AND specific L1 specs (-20°C rated) in your listing helps you appear at multiple levels of buyer navigation.
