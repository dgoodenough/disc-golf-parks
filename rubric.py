"""Apply the 7-dimension rubric to every park.

Calibration anchors (preserved from user's original criteria sheet):
  Winthrop / USDGC      → total 8
  European Open (Beast) → total 7

Scoring scale per dimension: -3 to +3.
"""

# DG Community score per metro (UDisc Health "higher of variety or availability"
# mapped to -3..+3). User's original scores preserved where available; new
# metros estimated from PDGA membership density and regional reputation.
DG_COMMUNITY = {
    "Minneapolis-St. Paul": 3,    # user; MN consistently #1 availability
    "Denver": 3,                   # user; CO top-tier
    "Charlotte": 2,                # user; NC strong + Charlotte #2 large city
    "St. Louis": 2,                # user; MO #12 variety
    "Austin": 2,                   # user; central TX hub
    "Chicago": 1,                  # user; IL middling
    "Dallas-Fort Worth": 1,        # user
    "Houston": 1,                  # user
    "San Antonio": 1,              # user
    "Portland OR": 1,              # user
    "Pittsburgh": 1,               # user
    "Cincinnati": 1,               # user
    "Kansas City": 1,              # user
    "Columbus OH": 1,              # user
    "Indianapolis": 1,             # user
    "Raleigh": 1,                  # user
    "Oklahoma City": 1,            # user
    "Grand Rapids": 1,             # user (MI #10 variety)
    "Rochester NY": 1,             # user
    "Tulsa": 1,                    # user
    "Riverside-San Bernardino": 0, # user
    "Detroit": 0,                  # user
    "San Diego": 0,                # user
    "Atlanta": -1,                 # user
    "New York City": -3,           # user
    "Washington DC": -2,           # user
    "Boston": -1,                  # user
    "Philadelphia": -1,            # user
    "Seattle": -1,                 # user
    "Phoenix": -1,                 # user
    # Blue-sky additions (estimated from PDGA density + state reputation)
    "Los Angeles": -1,
    "San Francisco Bay": -2,
    "Miami": -2,
    "Tampa": -1,                   # user had Tampa at -1
    "Nashville": 0,
    "Las Vegas": -1,
    "Sacramento": 0,
    "Orlando": 0,
    "Baltimore": -1,
    "Milwaukee": 0,                # WI has decent scene
    "Salt Lake City": 0,
    "New Orleans": -2,
    "Honolulu": -2,
    "Memphis": 0,
    "Jacksonville": -1,
    "Buffalo": -1,                 # rust belt NY; some scene
    "Birmingham": -1,
    "Hartford": -1,
}

def score_size(acres):
    """User's original: 50-100=-1, 100-120=0, 120-140=+1, 140+=+2 (no upper cap)."""
    if acres < 50:
        return -2
    if acres < 100:
        return -1
    if acres < 120:
        return 0
    if acres < 140:
        return 1
    return 2

def score_population(pop_100mi):
    """New scale built for 100-mile-radius population.

    0-1.5M: -2 / 1.5-3M: -1 / 3-5M: 0 / 5-7M: 1 / 7-10M: 2 / 10M+: 3
    Calibrated so Denver (5M) ≈ 0-1 and NYC (30M) hits the ceiling.
    """
    if pop_100mi < 1_500_000:
        return -2
    if pop_100mi < 3_000_000:
        return -1
    if pop_100mi < 5_000_000:
        return 0
    if pop_100mi < 7_000_000:
        return 1
    if pop_100mi < 10_000_000:
        return 2
    return 3

def score_centrality_distance(miles_to_dt):
    """Approximation of transit/centrality from straight-line distance to downtown.
    Reality also depends on transit network quality — overlaid manually per park.
    """
    if miles_to_dt < 2:
        return 3   # downtown / walkable
    if miles_to_dt < 5:
        return 2   # close-in
    if miles_to_dt < 10:
        return 1   # transit-accessible suburb
    if miles_to_dt < 20:
        return 0
    return -1

# Per-park manual adjustments to the formulaic baseline.
# (metro, park_name) -> dict with overrides for any of:
#   centrality, amenities, parking, history, beauty
# Defaults if not overridden: amenities=0, parking=1, history=0, beauty=0
# Reasoning is in the comment after each row.
PARK_OVERRIDES = {
    # ── Minneapolis ──────────────────────────────────────────────
    ("Minneapolis-St. Paul", "Como Regional Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # zoo+conservatory+pavilion; near light rail; lakeside
    ("Minneapolis-St. Paul", "Theodore Wirth Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1},  # chalet + trails; less transit; lake
    ("Minneapolis-St. Paul", "Minnehaha Regional Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 2, "centrality": 2},  # waterfall; LRT station onsite
    ("Minneapolis-St. Paul", "Powderhorn Park"): {"amenities": 0, "parking": 0, "history": 0, "beauty": 0, "centrality": 2},  # central but small

    # ── Denver ───────────────────────────────────────────────────
    ("Denver", "City Park"): {"amenities": 3, "parking": 2, "history": 1, "beauty": 1, "centrality": 2},  # museum+zoo+lake+skyline view
    ("Denver", "Sloan's Lake Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 2},  # large lake; skyline view; less infra
    ("Denver", "Washington Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1},  # historic; gardens; smaller
    ("Denver", "Cheesman Park"): {"amenities": 0, "parking": 0, "history": -1, "beauty": 1},  # former cemetery (-1); pavilion

    # ── Charlotte ────────────────────────────────────────────────
    ("Charlotte", "Freedom Park"): {"amenities": 2, "parking": 1, "history": 0, "beauty": 1, "centrality": 1},  # bandshell + festival; pond
    ("Charlotte", "Reedy Creek Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # nature preserve; far NE
    ("Charlotte", "McAlpine Creek Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 0},  # greenway hub
    ("Charlotte", "Romare Bearden Park"): {"amenities": 1, "parking": -1, "history": 1, "beauty": 1, "centrality": 3},  # uptown; tiny

    # ── St. Louis ────────────────────────────────────────────────
    ("St. Louis", "Forest Park"): {"amenities": 3, "parking": 2, "history": 2, "beauty": 1, "centrality": 2},  # museum+zoo+skating+bandshell; -1 mental note for golf course
    ("St. Louis", "Tower Grove Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 2},  # Victorian pavilions; tree canopy
    ("St. Louis", "Carondelet Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # two lakes; pavilion
    ("St. Louis", "Creve Coeur Lake Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # large lake; far suburb

    # ── Austin ───────────────────────────────────────────────────
    ("Austin", "Zilker Park"): {"amenities": 3, "parking": 2, "history": 1, "beauty": 1, "centrality": 2},  # ACL venue; on Town Lake; springs
    ("Austin", "Pease District Park"): {"amenities": 0, "parking": 0, "history": 1, "beauty": 1, "centrality": 2},  # creek; small
    ("Austin", "Mueller Lake Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 1},  # new urbanist; lake; too small
    ("Austin", "Festival Beach"): {"amenities": 0, "parking": 0, "history": 0, "beauty": 1, "centrality": 2},  # lakefront

    # ── Chicago ──────────────────────────────────────────────────
    ("Chicago", "Grant Park"): {"amenities": 3, "parking": 2, "history": 2, "beauty": 1, "centrality": 3},  # Lolla + Buckingham + Pritzker; transit-saturated
    ("Chicago", "Lincoln Park"): {"amenities": 3, "parking": 2, "history": 2, "beauty": 2, "centrality": 2},  # zoo+conservatory+lake; bus density
    ("Chicago", "Humboldt Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # boathouse; cultural center
    ("Chicago", "Jackson Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 1, "centrality": 1},  # World's Fair site; Obama Center incoming
    ("Chicago", "Washington Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # Olmsted; big meadow; under-utilized

    # ── Dallas-Fort Worth ────────────────────────────────────────
    ("Dallas-Fort Worth", "Trinity Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # FW; Trinity River; botanic adj
    ("Dallas-Fort Worth", "White Rock Lake Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": 0},  # iconic Dallas lake
    ("Dallas-Fort Worth", "Reverchon Park"): {"amenities": 0, "parking": 0, "history": 0, "beauty": 0, "centrality": 2},  # uptown; small
    ("Dallas-Fort Worth", "Trinity Forest"): {"amenities": 0, "parking": 0, "history": 0, "beauty": 1, "centrality": 0},  # giant urban forest; minimal infra

    # ── Houston ──────────────────────────────────────────────────
    ("Houston", "Memorial Park"): {"amenities": 2, "parking": 2, "history": 1, "beauty": 1, "centrality": 1},  # tennis+pool+pavilion; -1 for golf course nearby
    ("Houston", "Hermann Park"): {"amenities": 3, "parking": 2, "history": 2, "beauty": 2, "centrality": 2},  # zoo+museums+outdoor theater
    ("Houston", "Buffalo Bayou Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 2, "centrality": 3},  # linear waterway; downtown
    ("Houston", "Discovery Green"): {"amenities": 3, "parking": 1, "history": 1, "beauty": 1, "centrality": 3},  # downtown; great infra; too small

    # ── San Antonio ──────────────────────────────────────────────
    ("San Antonio", "Brackenridge Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 1, "centrality": 1},  # zoo+golf+sunken garden+river
    ("San Antonio", "Hardberger Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # land bridge; suburban
    ("San Antonio", "McAllister Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 0},  # large; sport-heavy

    # ── Portland OR ──────────────────────────────────────────────
    ("Portland OR", "Washington Park"): {"amenities": 3, "parking": 1, "history": 2, "beauty": 2, "centrality": 2},  # zoo+arboretum+rose garden; MAX adj
    ("Portland OR", "Mount Tabor Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 2, "centrality": 1},  # extinct volcano; views
    ("Portland OR", "Laurelhurst Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 1, "centrality": 2},  # historic; small; transit

    # ── Pittsburgh ───────────────────────────────────────────────
    ("Pittsburgh", "Schenley Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 2},  # Phipps Conservatory adj; -1 for university adjacency
    ("Pittsburgh", "Frick Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": 1},  # wooded ravines; biggest in city
    ("Pittsburgh", "Highland Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # zoo entrance; reservoir
    ("Pittsburgh", "Riverview Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 1, "centrality": 0},  # observatory; N side

    # ── Cincinnati ───────────────────────────────────────────────
    ("Cincinnati", "Devou Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 3, "centrality": 1},  # skyline view across river; bandshell
    ("Cincinnati", "Eden Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 2},  # art museum; reservoir; vista
    ("Cincinnati", "Mt Airy Forest"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": -1},  # 1st US municipal forest; far NW
    ("Cincinnati", "Ault Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 2, "centrality": 0},  # pavilion; observation deck

    # ── Kansas City ──────────────────────────────────────────────
    ("Kansas City", "Penn Valley Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 1, "centrality": 3},  # Liberty Memorial adj; downtown views
    ("Kansas City", "Swope Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 1, "centrality": 0},  # zoo+theater+golf; largest
    ("Kansas City", "Loose Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": 2},  # rose garden; Plaza adj
    ("Kansas City", "Kessler Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 2, "centrality": 1},  # bluffside; views

    # ── Columbus OH ──────────────────────────────────────────────
    ("Columbus OH", "Franklin Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # conservatory; central
    ("Columbus OH", "Antrim Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # lake; suburban N
    ("Columbus OH", "Goodale Park"): {"amenities": 0, "parking": -1, "history": 1, "beauty": 1, "centrality": 3},  # Short North; tiny
    ("Columbus OH", "Schiller Park"): {"amenities": 0, "parking": 0, "history": 1, "beauty": 1, "centrality": 2},  # German Village; tiny

    # ── Indianapolis ─────────────────────────────────────────────
    ("Indianapolis", "Garfield Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 1, "centrality": 1},  # conservatory + sunken gardens
    ("Indianapolis", "White River State Park"): {"amenities": 3, "parking": 2, "history": 1, "beauty": 1, "centrality": 3},  # downtown; museums; canal
    ("Indianapolis", "Holliday Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 0},  # ruins sculpture; small
    ("Indianapolis", "Eagle Creek Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # massive; reservoir; far W

    # ── Raleigh ──────────────────────────────────────────────────
    ("Raleigh", "Dorothea Dix Park"): {"amenities": 1, "parking": 1, "history": 2, "beauty": 1, "centrality": 2},  # former hospital; skyline views; redev
    ("Raleigh", "Pullen Park"): {"amenities": 2, "parking": 0, "history": 2, "beauty": 1, "centrality": 2},  # historic carousel; small
    ("Raleigh", "Lake Wheeler Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 0},  # boat-focused lake
    ("Raleigh", "Umstead State Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": -1},  # pine forest; far W

    # ── Oklahoma City ────────────────────────────────────────────
    ("Oklahoma City", "Scissortail Park"): {"amenities": 2, "parking": 1, "history": 0, "beauty": 1, "centrality": 3},  # new downtown; stage
    ("Oklahoma City", "Will Rogers Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 0},  # gardens; central
    ("Oklahoma City", "Lake Hefner"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # reservoir focused; far NW

    # ── Grand Rapids ─────────────────────────────────────────────
    ("Grand Rapids", "Millennium Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 0},  # reclaimed gravel pit; lakes
    ("Grand Rapids", "John Ball Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # zoo; central W
    ("Grand Rapids", "Riverside Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 1},  # Grand River frontage

    # ── Rochester NY ─────────────────────────────────────────────
    ("Rochester NY", "Highland Park"): {"amenities": 1, "parking": 1, "history": 2, "beauty": 2, "centrality": 1},  # Olmsted; Lilac Festival; rolling
    ("Rochester NY", "Genesee Valley Park"): {"amenities": 1, "parking": 1, "history": 2, "beauty": 1, "centrality": 1},  # Olmsted; -1 for golf course
    ("Rochester NY", "Cobbs Hill Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": 1},  # reservoir; views
    ("Rochester NY", "Durand Eastman Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": -1},  # Lake Ontario; far NE; -1 for golf course

    # ── Tulsa ────────────────────────────────────────────────────
    ("Tulsa", "Gathering Place"): {"amenities": 3, "parking": 1, "history": 1, "beauty": 2, "centrality": 1},  # major recent build; riverfront
    ("Tulsa", "Mohawk Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": -1},  # zoo; far N; -1 for size sweet spot violation (>>140 but isolated)
    ("Tulsa", "LaFortune Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 0},  # central S; -1 for golf course
    ("Tulsa", "Woodward Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 2, "centrality": 1},  # rose garden; arboretum

    # ── Riverside-San Bernardino ─────────────────────────────────
    ("Riverside-San Bernardino", "Fairmount Park"): {"amenities": 1, "parking": 1, "history": 2, "beauty": 1, "centrality": 1},  # Olmsted-Vaux; lake; golf-adj
    ("Riverside-San Bernardino", "Mt Rubidoux Park"): {"amenities": 0, "parking": 0, "history": 2, "beauty": 2, "centrality": 2},  # iconic hill; cross + views

    # ── Detroit ──────────────────────────────────────────────────
    ("Detroit", "Belle Isle Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 1},  # river island; conservatory + aquarium; -1 for golf course
    ("Detroit", "Palmer Park"): {"amenities": 1, "parking": 0, "history": 2, "beauty": 1, "centrality": 0},  # log cabin; old growth; -1 for golf course
    ("Detroit", "River Rouge Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # large; W; underused; -1 for golf course

    # ── San Diego ────────────────────────────────────────────────
    ("San Diego", "Balboa Park"): {"amenities": 3, "parking": 2, "history": 3, "beauty": 2, "centrality": 2},  # zoo + 17 museums; Spanish architecture; -1 for golf course
    ("San Diego", "Mission Bay Park"): {"amenities": 2, "parking": 2, "history": 0, "beauty": 2, "centrality": 1},  # massive aquatic; SeaWorld
    ("San Diego", "Presidio Park"): {"amenities": 1, "parking": 0, "history": 2, "beauty": 1, "centrality": 2},  # historic; small

    # ── Atlanta ──────────────────────────────────────────────────
    ("Atlanta", "Piedmont Park"): {"amenities": 3, "parking": 1, "history": 1, "beauty": 1, "centrality": 2},  # festival venue; MARTA Midtown
    ("Atlanta", "Centennial Olympic Park"): {"amenities": 3, "parking": 1, "history": 2, "beauty": 1, "centrality": 3},  # CNN/aquarium adj; too small
    ("Atlanta", "Grant Park (ATL)"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 1, "centrality": 1},  # zoo; oldest in city

    # ── New York City ────────────────────────────────────────────
    ("New York City", "Central Park"): {"amenities": 3, "parking": 1, "history": 3, "beauty": 2, "centrality": 3},  # iconic; -1 for "everything's already there"
    ("New York City", "Prospect Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 2},  # Olmsted; Brooklyn

    # ── Washington DC ────────────────────────────────────────────
    ("Washington DC", "National Mall"): {"amenities": 3, "parking": 0, "history": 3, "beauty": 2, "centrality": 3},  # monuments; museums; iconic
    ("Washington DC", "Rock Creek Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": 1},  # wooded ravine; -1 transit
    ("Washington DC", "Anacostia Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # waterfront; under-utilized

    # ── Boston ───────────────────────────────────────────────────
    ("Boston", "Franklin Park"): {"amenities": 1, "parking": 1, "history": 2, "beauty": 1, "centrality": 0},  # Olmsted; zoo; -1 for golf course
    ("Boston", "Boston Common + Public Garden"): {"amenities": 3, "parking": 0, "history": 3, "beauty": 2, "centrality": 3},  # oldest public park; downtown; too small

    # ── Philadelphia ─────────────────────────────────────────────
    ("Philadelphia", "Fairmount Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 1},  # art museum; Schuylkill; -1 for golf course
    ("Philadelphia", "FDR Park"): {"amenities": 1, "parking": 2, "history": 1, "beauty": 1, "centrality": 1},  # lakes; near stadiums; -1 for golf course

    # ── Seattle ──────────────────────────────────────────────────
    ("Seattle", "Discovery Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 3, "centrality": -1},  # bluffs; Sound; lighthouse; far NW
    ("Seattle", "Lincoln Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": 0},  # Puget Sound; W Seattle
    ("Seattle", "Volunteer Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 2},  # conservatory; reservoir

    # ── Phoenix ──────────────────────────────────────────────────
    ("Phoenix", "Encanto Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 2},  # lagoon; central; -1 for golf course
    ("Phoenix", "Papago Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 2, "centrality": 0},  # zoo + botanical; red buttes
    ("Phoenix", "South Mountain Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": -1},  # mountainous; largest municipal park in US

    # ── Los Angeles (blue sky) ──────────────────────────────────
    ("Los Angeles", "Griffith Park"): {"amenities": 3, "parking": 2, "history": 3, "beauty": 3, "centrality": 1},  # observatory + Hollywood Sign + zoo + Greek Theatre + planetarium
    ("Los Angeles", "Elysian Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 2},  # 2nd oldest LA park; Dodger Stadium adj
    ("Los Angeles", "Exposition Park"): {"amenities": 3, "parking": 2, "history": 2, "beauty": 1, "centrality": 1},  # museums + Coliseum; -1 for USC adj
    ("Los Angeles", "Kenneth Hahn State Rec Area"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 2, "centrality": 1},  # hilltop views
    ("Los Angeles", "Echo Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 2, "centrality": 2},  # iconic lake; too small

    # ── SF Bay (blue sky) ───────────────────────────────────────
    ("San Francisco Bay", "Golden Gate Park"): {"amenities": 3, "parking": 1, "history": 3, "beauty": 3, "centrality": 1},  # museums + conservatory + bison; -1 for golf course
    ("San Francisco Bay", "Presidio"): {"amenities": 2, "parking": 2, "history": 3, "beauty": 3, "centrality": 1},  # Golden Gate views; -1 for golf course
    ("San Francisco Bay", "Lake Merritt / Lakeside Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 2},  # Oakland; BART; iconic lagoon
    ("San Francisco Bay", "Tilden Regional Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 2, "centrality": -1},  # Berkeley hills; -1 for golf course

    # ── Miami (blue sky) ────────────────────────────────────────
    ("Miami", "Tropical Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # central
    ("Miami", "Crandon Park"): {"amenities": 2, "parking": 2, "history": 1, "beauty": 3, "centrality": -1},  # beach + nature; -1 for golf course
    ("Miami", "Bayfront Park"): {"amenities": 2, "parking": 0, "history": 1, "beauty": 1, "centrality": 3},  # downtown; small
    ("Miami", "Amelia Earhart Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 0},

    # ── Tampa (blue sky) ────────────────────────────────────────
    ("Tampa", "Al Lopez Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 1},
    ("Tampa", "Lettuce Lake Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 2, "centrality": -1},
    ("Tampa", "Curtis Hixon Waterfront Park"): {"amenities": 2, "parking": 0, "history": 0, "beauty": 2, "centrality": 3},

    # ── Nashville (blue sky) ────────────────────────────────────
    ("Nashville", "Centennial Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 1, "centrality": 2},  # Parthenon replica; iconic
    ("Nashville", "Shelby Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": 1},  # Cumberland River
    ("Nashville", "Percy Warner Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": -1},  # hilly; far SW
    ("Nashville", "Bicentennial Capitol Mall State Park"): {"amenities": 2, "parking": 0, "history": 2, "beauty": 1, "centrality": 3},

    # ── Las Vegas (blue sky) ────────────────────────────────────
    ("Las Vegas", "Sunset Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 0},
    ("Las Vegas", "Floyd Lamb Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": -1},
    ("Las Vegas", "Tule Springs Fossil Beds"): {"amenities": 0, "parking": 0, "history": 2, "beauty": 1, "centrality": -1},

    # ── Sacramento (blue sky) ───────────────────────────────────
    ("Sacramento", "William Land Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},  # zoo + rose garden
    ("Sacramento", "Discovery Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": 1},  # river confluence
    ("Sacramento", "McKinley Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 1, "centrality": 2},

    # ── Orlando (blue sky) ──────────────────────────────────────
    ("Orlando", "Lake Eola Park"): {"amenities": 2, "parking": 0, "history": 1, "beauty": 2, "centrality": 3},
    ("Orlando", "Loch Haven Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 1, "centrality": 2},
    ("Orlando", "Bill Frederick Park at Turkey Lake"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},

    # ── Baltimore (blue sky) ────────────────────────────────────
    ("Baltimore", "Druid Hill Park"): {"amenities": 2, "parking": 1, "history": 3, "beauty": 1, "centrality": 1},  # 3rd-oldest landscaped park; zoo
    ("Baltimore", "Patterson Park"): {"amenities": 1, "parking": 1, "history": 2, "beauty": 1, "centrality": 2},  # pagoda; iconic
    ("Baltimore", "Federal Hill Park"): {"amenities": 0, "parking": 0, "history": 2, "beauty": 2, "centrality": 3},  # harbor view; tiny

    # ── Milwaukee (blue sky) ────────────────────────────────────
    ("Milwaukee", "Lake Park"): {"amenities": 1, "parking": 1, "history": 2, "beauty": 3, "centrality": 1},  # Lake Michigan bluff; Olmsted
    ("Milwaukee", "Veterans Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 2, "centrality": 2},  # lakefront festival site
    ("Milwaukee", "Whitnall Park"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 1, "centrality": -1},  # SW suburb

    # ── Salt Lake City (blue sky) ───────────────────────────────
    ("Salt Lake City", "Liberty Park"): {"amenities": 2, "parking": 1, "history": 1, "beauty": 1, "centrality": 2},  # central; pond + aviary
    ("Salt Lake City", "Sugar House Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 1, "centrality": 1},
    ("Salt Lake City", "This Is The Place Heritage Park"): {"amenities": 2, "parking": 1, "history": 3, "beauty": 1, "centrality": 0},  # historic village

    # ── New Orleans (blue sky) ──────────────────────────────────
    ("New Orleans", "City Park"): {"amenities": 3, "parking": 2, "history": 2, "beauty": 3, "centrality": 1},  # 1300 ac; oaks; art museum; lagoons; iconic
    ("New Orleans", "Audubon Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 3, "centrality": 1},  # streetcar; oaks; -1 for golf course
    ("New Orleans", "Crescent Park"): {"amenities": 1, "parking": 0, "history": 0, "beauty": 1, "centrality": 2},

    # ── Honolulu (blue sky) ─────────────────────────────────────
    ("Honolulu", "Kapiolani Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 3, "centrality": 1},  # Diamond Head adj; oldest in HI
    ("Honolulu", "Ala Moana Beach Park"): {"amenities": 2, "parking": 2, "history": 1, "beauty": 3, "centrality": 2},  # beach + lagoon
    ("Honolulu", "Magic Island"): {"amenities": 1, "parking": 1, "history": 0, "beauty": 3, "centrality": 2},

    # ── Memphis (blue sky) ──────────────────────────────────────
    ("Memphis", "Shelby Farms Park"): {"amenities": 2, "parking": 2, "history": 0, "beauty": 1, "centrality": -1},  # 5x Central Park
    ("Memphis", "Overton Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 1},  # old-growth + zoo + art college (-1)
    ("Memphis", "Tom Lee Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 2, "centrality": 3},  # Mississippi riverfront

    # ── Jacksonville (blue sky) ─────────────────────────────────
    ("Jacksonville", "Hanna Park"): {"amenities": 2, "parking": 2, "history": 0, "beauty": 3, "centrality": -1},  # beach + lake combo
    ("Jacksonville", "Friendship Fountain Park / Riverside"): {"amenities": 1, "parking": 0, "history": 0, "beauty": 2, "centrality": 3},
    ("Jacksonville", "Hemming Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 0, "centrality": 3},

    # ── Buffalo (blue sky) ──────────────────────────────────────
    ("Buffalo", "Delaware Park"): {"amenities": 2, "parking": 1, "history": 2, "beauty": 1, "centrality": 1},  # Olmsted; zoo adj; -1 for golf course
    ("Buffalo", "South Park"): {"amenities": 1, "parking": 1, "history": 2, "beauty": 2, "centrality": 0},  # Olmsted; botanical

    # ── Birmingham (blue sky) ───────────────────────────────────
    ("Birmingham", "Railroad Park"): {"amenities": 2, "parking": 0, "history": 1, "beauty": 1, "centrality": 3},
    ("Birmingham", "Avondale Park"): {"amenities": 1, "parking": 0, "history": 1, "beauty": 1, "centrality": 1},
    ("Birmingham", "Ruffner Mountain Nature Preserve"): {"amenities": 0, "parking": 1, "history": 0, "beauty": 2, "centrality": 0},

    # ── Hartford (blue sky) ─────────────────────────────────────
    ("Hartford", "Bushnell Park"): {"amenities": 2, "parking": 0, "history": 3, "beauty": 1, "centrality": 3},  # oldest publicly funded park in US
    ("Hartford", "Elizabeth Park"): {"amenities": 1, "parking": 1, "history": 1, "beauty": 2, "centrality": 1},
}

# Default per-dimension fallback if not overridden
DEFAULTS = {"amenities": 0, "parking": 1, "history": 0, "beauty": 0}

def score_park(metro, park_name, acres, pop_100mi, miles_to_dt):
    size = score_size(acres)
    population = score_population(pop_100mi)
    centrality_base = score_centrality_distance(miles_to_dt)
    dg = DG_COMMUNITY.get(metro, 0)

    o = PARK_OVERRIDES.get((metro, park_name), {})
    centrality = o.get("centrality", centrality_base)
    amenities = o.get("amenities", DEFAULTS["amenities"])
    parking = o.get("parking", DEFAULTS["parking"])
    history = o.get("history", DEFAULTS["history"])
    beauty = o.get("beauty", DEFAULTS["beauty"])

    total = size + amenities + centrality + parking + dg + population + history + beauty
    return {
        "Size": size,
        "Amenities": amenities,
        "Centrality": centrality,
        "Parking": parking,
        "DG_Community": dg,
        "Population": population,
        "History": history,
        "Beauty": beauty,
        "Total": total,
    }
