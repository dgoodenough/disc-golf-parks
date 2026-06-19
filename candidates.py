"""Candidate parks for the disc golf tournament host analysis.

Coordinates are park interior points (not entrances), accurate to ~0.001 deg
(well within the 100-mile-radius tolerance). Acreage from city park system
listings, Wikipedia, or TPL ParkServe where available.

Downtown lat/lng used for the centrality/transit dimension.
"""

# (metro_name, downtown_lat, downtown_lng)
METROS = [
    ("Minneapolis-St. Paul", 44.9778, -93.2650),
    ("Denver", 39.7392, -104.9903),
    ("Charlotte", 35.2271, -80.8431),
    ("St. Louis", 38.6270, -90.1994),
    ("Austin", 30.2672, -97.7431),
    ("Chicago", 41.8781, -87.6298),
    ("Dallas-Fort Worth", 32.7767, -96.7970),
    ("Houston", 29.7604, -95.3698),
    ("San Antonio", 29.4241, -98.4936),
    ("Portland OR", 45.5152, -122.6784),
    ("Pittsburgh", 40.4406, -79.9959),
    ("Cincinnati", 39.1031, -84.5120),
    ("Kansas City", 39.0997, -94.5786),
    ("Columbus OH", 39.9612, -82.9988),
    ("Indianapolis", 39.7684, -86.1581),
    ("Raleigh", 35.7796, -78.6382),
    ("Oklahoma City", 35.4676, -97.5164),
    ("Grand Rapids", 42.9634, -85.6681),
    ("Rochester NY", 43.1566, -77.6088),
    ("Tulsa", 36.1540, -95.9928),
    ("Riverside-San Bernardino", 33.9533, -117.3962),
    ("Detroit", 42.3314, -83.0458),
    ("San Diego", 32.7157, -117.1611),
    ("Atlanta", 33.7490, -84.3880),
    ("New York City", 40.7128, -74.0060),
    ("Washington DC", 38.9072, -77.0369),
    ("Boston", 42.3601, -71.0589),
    ("Philadelphia", 39.9526, -75.1652),
    ("Seattle", 47.6062, -122.3321),
    ("Phoenix", 33.4484, -112.0740),
    ("Los Angeles", 34.0522, -118.2437),
    ("San Francisco Bay", 37.7749, -122.4194),
    ("Miami", 25.7617, -80.1918),
    ("Tampa", 27.9506, -82.4572),
    ("Nashville", 36.1627, -86.7816),
    ("Las Vegas", 36.1716, -115.1391),
    ("Sacramento", 38.5816, -121.4944),
    ("Orlando", 28.5383, -81.3792),
    ("Baltimore", 39.2904, -76.6122),
    ("Milwaukee", 43.0389, -87.9065),
    ("Salt Lake City", 40.7608, -111.8910),
    ("New Orleans", 29.9511, -90.0715),
    ("Honolulu", 21.3099, -157.8581),
    ("Memphis", 35.1495, -90.0490),
    ("Jacksonville", 30.3322, -81.6557),
    ("Buffalo", 42.8864, -78.8784),
    ("Birmingham", 33.5186, -86.8104),
    ("Hartford", 41.7658, -72.6734),
]

# (metro, park_name, lat, lng, acres, notes)
# acres: official park acreage when known; rough estimate where marked ~
PARKS = [
    # Minneapolis-St. Paul (combined 6 in triage)
    ("Minneapolis-St. Paul", "Como Regional Park", 44.9810, -93.1495, 384, "User original; lake + zoo + conservatory + golf course"),
    ("Minneapolis-St. Paul", "Theodore Wirth Park", 44.9858, -93.3210, 759, "Largest regional park in city; bike trails, golf course on one side"),
    ("Minneapolis-St. Paul", "Minnehaha Regional Park", 44.9153, -93.2110, 193, "Iconic waterfall; light rail station; ~5mi from downtown"),
    ("Minneapolis-St. Paul", "Powderhorn Park", 44.9430, -93.2540, 65, "Smaller; central S Mpls; hosts MayDay festival"),

    # Denver (combined 6)
    ("Denver", "City Park", 39.7461, -104.9486, 314, "User original; zoo + museum + lake + golf adjacent"),
    ("Denver", "Sloan's Lake Park", 39.7497, -105.0500, 290, "Lake-centered; west of downtown"),
    ("Denver", "Washington Park", 39.6989, -104.9700, 165, "Lake + flower gardens; high-density neighborhood"),
    ("Denver", "Cheesman Park", 39.7333, -104.9648, 80, "Former cemetery; central; smaller"),

    # Charlotte (combined 4)
    ("Charlotte", "Freedom Park", 35.1965, -80.8400, 98, "Most-visited Charlotte park; festival venue; central"),
    ("Charlotte", "Reedy Creek Park", 35.2640, -80.7330, 727, "Large nature preserve; suburban NE"),
    ("Charlotte", "McAlpine Creek Park", 35.1280, -80.7400, 462, "Greenway hub; SE Charlotte"),
    ("Charlotte", "Romare Bearden Park", 35.2275, -80.8470, 5.4, "Uptown; too small as host but flagship Uptown park"),

    # St. Louis (combined 4)
    ("St. Louis", "Forest Park", 38.6357, -90.2845, 1326, "User original; massive; has golf + zoo + museums"),
    ("St. Louis", "Tower Grove Park", 38.6086, -90.2510, 289, "Victorian park; central; tree canopy"),
    ("St. Louis", "Carondelet Park", 38.5650, -90.2570, 180, "S city; two lakes; historic"),
    ("St. Louis", "Creve Coeur Lake Park", 38.7100, -90.4800, 2156, "Largest STL Co park; lake; ~15mi out"),

    # Austin (combined 4)
    ("Austin", "Zilker Park", 30.2669, -97.7729, 351, "User original; ACL festival venue; central; on Town Lake"),
    ("Austin", "Pease District Park", 30.2860, -97.7570, 84, "Linear creek park; downtown adjacent"),
    ("Austin", "Mueller Lake Park", 30.2960, -97.7050, 30, "New-urbanist redev; central; too small for host event alone"),
    ("Austin", "Festival Beach", 30.2540, -97.7250, 22, "Lakeside; central; small"),

    # Chicago (combined 4)
    ("Chicago", "Grant Park", 41.8757, -87.6189, 319, "User original; lakefront; Lollapalooza venue; transit-saturated"),
    ("Chicago", "Lincoln Park", 41.9214, -87.6336, 1208, "Largest in city; lakefront; zoo + conservatory"),
    ("Chicago", "Humboldt Park", 41.9039, -87.7053, 207, "User mentioned; lagoon + fieldhouse; W side"),
    ("Chicago", "Jackson Park", 41.7806, -87.5780, 543, "S side; lakefront; Olmsted-designed"),
    ("Chicago", "Washington Park", 41.7920, -87.6166, 367, "S side; large flat meadow; Olmsted-designed"),

    # Dallas-Fort Worth (combined 4)
    ("Dallas-Fort Worth", "Trinity Park", 32.7430, -97.3550, 252, "User original; Fort Worth; Trinity River; central"),
    ("Dallas-Fort Worth", "White Rock Lake Park", 32.8330, -96.7220, 1015, "Lake + trail; E Dallas; iconic"),
    ("Dallas-Fort Worth", "Reverchon Park", 32.8050, -96.8120, 36, "Uptown Dallas; small"),
    ("Dallas-Fort Worth", "Trinity Forest", 32.7290, -96.7170, 6000, "Largest urban hardwood forest in US; S Dallas"),

    # Houston (combined 4)
    ("Houston", "Memorial Park", 29.7644, -95.4444, 1466, "User original; massive; central; golf course on E side"),
    ("Houston", "Hermann Park", 29.7180, -95.3900, 445, "Museum district; zoo; central"),
    ("Houston", "Buffalo Bayou Park", 29.7600, -95.3950, 160, "Linear; downtown adjacent"),
    ("Houston", "Discovery Green", 29.7530, -95.3596, 12, "User original; downtown; too small alone"),

    # San Antonio (combined 3)
    ("San Antonio", "Brackenridge Park", 29.4625, -98.4730, 343, "User original; zoo; San Antonio River; central"),
    ("San Antonio", "Hardberger Park", 29.5650, -98.5050, 330, "Land bridge; NW suburb"),
    ("San Antonio", "McAllister Park", 29.5520, -98.4520, 976, "Largest SA park; NE; suburban"),

    # Portland OR (combined 3)
    ("Portland OR", "Washington Park", 45.5117, -122.7160, 410, "User original; zoo + arboretum; MAX light rail"),
    ("Portland OR", "Mount Tabor Park", 45.5110, -122.5950, 191, "Extinct volcano cone; iconic SE"),
    ("Portland OR", "Laurelhurst Park", 45.5220, -122.6240, 26, "Historic urban park; small"),

    # Pittsburgh (combined 3)
    ("Pittsburgh", "Schenley Park", 40.4357, -79.9417, 456, "User original; near CMU/Pitt; ravines"),
    ("Pittsburgh", "Frick Park", 40.4380, -79.9000, 644, "Largest in city; wooded ravines; E end"),
    ("Pittsburgh", "Highland Park", 40.4810, -79.9230, 380, "Reservoir + zoo entrance; E end"),
    ("Pittsburgh", "Riverview Park", 40.4830, -80.0220, 251, "N side; observatory; less central"),

    # Cincinnati (combined 3)
    ("Cincinnati", "Devou Park", 39.0850, -84.5350, 700, "User original; Covington KY; skyline views"),
    ("Cincinnati", "Eden Park", 39.1135, -84.4940, 186, "Art museum; reservoir; central E"),
    ("Cincinnati", "Mt Airy Forest", 39.1900, -84.5750, 1471, "Largest urban forest; less central NW"),
    ("Cincinnati", "Ault Park", 39.1300, -84.4180, 224, "Pavilion; gardens; observation deck"),

    # Kansas City (combined 3)
    ("Kansas City", "Penn Valley Park", 39.0855, -94.5882, 176, "User original; near Crown Center; central"),
    ("Kansas City", "Swope Park", 38.9930, -94.5320, 1805, "Largest in city; zoo; S side"),
    ("Kansas City", "Loose Park", 39.0420, -94.5950, 75, "Country Club Plaza adjacent; rose garden"),
    ("Kansas City", "Kessler Park", 39.1180, -94.5550, 240, "User original; cliffside; NE"),

    # Columbus OH (combined 3)
    ("Columbus OH", "Franklin Park", 39.9700, -82.9560, 88, "User original; Conservatory; central E"),
    ("Columbus OH", "Antrim Park", 40.0750, -83.0270, 116, "Lake + trails; N suburbs"),
    ("Columbus OH", "Goodale Park", 39.9740, -83.0090, 32, "Short North; historic; small"),
    ("Columbus OH", "Schiller Park", 39.9450, -82.9920, 23, "German Village; small"),

    # Indianapolis (combined 3)
    ("Indianapolis", "Garfield Park", 39.7320, -86.1400, 136, "Conservatory + sunken gardens; S"),
    ("Indianapolis", "White River State Park", 39.7680, -86.1730, 250, "Downtown; museums; canal"),
    ("Indianapolis", "Holliday Park", 39.8650, -86.1740, 94, "Riverside; ruins; N side"),
    ("Indianapolis", "Eagle Creek Park", 39.8460, -86.2950, 5300, "Largest; reservoir; W far out"),

    # Raleigh (combined 3)
    ("Raleigh", "Dorothea Dix Park", 35.7710, -78.6660, 308, "Former hospital; central; redev"),
    ("Raleigh", "Pullen Park", 35.7820, -78.6580, 66, "Historic; central; small"),
    ("Raleigh", "Lake Wheeler Park", 35.7140, -78.6700, 150, "S Raleigh; lake-focused"),
    ("Raleigh", "Umstead State Park", 35.8800, -78.7560, 5580, "Between Raleigh + Durham; pine forest"),

    # Oklahoma City (combined 3)
    ("Oklahoma City", "Scissortail Park", 35.4530, -97.5180, 70, "New downtown park; stage; central"),
    ("Oklahoma City", "Will Rogers Park", 35.5040, -97.5610, 130, "Gardens; central NW"),
    ("Oklahoma City", "Lake Hefner", 35.5450, -97.5900, 2500, "Reservoir-focused; NW"),

    # Grand Rapids (combined 3)
    ("Grand Rapids", "Millennium Park", 42.9290, -85.7560, 1400, "Lakes + trails; SW; ex-gravel pit reclaimed"),
    ("Grand Rapids", "John Ball Park", 42.9660, -85.7050, 100, "Zoo; central W"),
    ("Grand Rapids", "Riverside Park", 43.0080, -85.6500, 87, "Grand River; N"),

    # Rochester NY (combined 3)
    ("Rochester NY", "Highland Park", 43.1330, -77.6080, 150, "User original; Lilac Festival; Olmsted"),
    ("Rochester NY", "Genesee Valley Park", 43.1240, -77.6400, 800, "Olmsted; river; U of R adjacent"),
    ("Rochester NY", "Cobbs Hill Park", 43.1480, -77.5660, 109, "Reservoir hill; views; E"),
    ("Rochester NY", "Durand Eastman Park", 43.2300, -77.5400, 965, "Lake Ontario; far NE"),

    # Tulsa (combined 3)
    ("Tulsa", "Gathering Place", 36.1230, -95.9760, 100, "Riverside; major recent build; downtown adjacent"),
    ("Tulsa", "Mohawk Park", 36.2360, -95.9100, 2800, "Largest; zoo + nature center; N"),
    ("Tulsa", "LaFortune Park", 36.0900, -95.9170, 270, "Central S; trails + golf"),
    ("Tulsa", "Woodward Park", 36.1270, -95.9710, 45, "Rose garden; central; small"),

    # Riverside-San Bernardino (combined 3, pop 3 / dg 0)
    ("Riverside-San Bernardino", "Fairmount Park", 33.9990, -117.3920, 200, "Riverside; lake; Olmsted-Vaux"),
    ("Riverside-San Bernardino", "Mt Rubidoux Park", 33.9750, -117.3960, 161, "Hill summit; central Riverside"),

    # Detroit (combined 3 in pop, 0 dg)
    ("Detroit", "Belle Isle Park", 42.3380, -82.9810, 982, "Island in Detroit River; state park; central"),
    ("Detroit", "Palmer Park", 42.4220, -83.1080, 296, "Wooded; N Detroit; historic"),
    ("Detroit", "River Rouge Park", 42.3700, -83.2480, 1184, "Largest in city; W side; less central"),

    # San Diego (combined 3 in pop, 0 dg)
    ("San Diego", "Balboa Park", 32.7320, -117.1450, 1200, "Zoo + museums; central; iconic"),
    ("San Diego", "Mission Bay Park", 32.7780, -117.2270, 4235, "Largest aquatic park; W"),
    ("San Diego", "Presidio Park", 32.7560, -117.1980, 50, "Historic; small"),

    # User's already-scored references (combined ≤2 but in user's criteria sheet)
    ("Atlanta", "Piedmont Park", 33.7860, -84.3735, 200, "User original; central; festival venue"),
    ("Atlanta", "Centennial Olympic Park", 33.7600, -84.3930, 21, "Downtown; small"),
    ("Atlanta", "Grant Park (ATL)", 33.7370, -84.3700, 131, "S of downtown; zoo"),
    ("New York City", "Central Park", 40.7829, -73.9654, 843, "User original; iconic; transit-saturated"),
    ("New York City", "Prospect Park", 40.6602, -73.9690, 526, "Brooklyn; Olmsted; lakes"),
    ("Washington DC", "National Mall", 38.8895, -77.0228, 309, "User original; iconic; transit-saturated"),
    ("Washington DC", "Rock Creek Park", 38.9580, -77.0470, 1754, "Largest in DC; wooded; less transit"),
    ("Washington DC", "Anacostia Park", 38.8770, -76.9700, 1200, "River; SE; less developed"),
    ("Boston", "Franklin Park", 42.3010, -71.0870, 527, "Largest in Boston; Olmsted Emerald Necklace"),
    ("Boston", "Boston Common + Public Garden", 42.3550, -71.0660, 75, "Iconic; downtown; small"),
    ("Philadelphia", "Fairmount Park", 39.9870, -75.2160, 2052, "Largest urban park system; Schuylkill"),
    ("Philadelphia", "FDR Park", 39.9070, -75.1840, 348, "S Philly; lakes"),
    ("Seattle", "Discovery Park", 47.6580, -122.4200, 534, "Largest Seattle park; bluffs"),
    ("Seattle", "Lincoln Park", 47.5310, -122.3970, 135, "Puget Sound; W Seattle"),
    ("Seattle", "Volunteer Park", 47.6300, -122.3160, 48, "Capitol Hill; central; small"),
    ("Phoenix", "Encanto Park", 33.4730, -112.0890, 222, "Central; lagoon"),
    ("Phoenix", "Papago Park", 33.4530, -111.9430, 1500, "Zoo + botanical garden; red buttes; E"),
    ("Phoenix", "South Mountain Park", 33.3500, -112.0470, 16000, "Largest municipal park in US; mountainous"),

    # ── BLUE SKY: huge metros with weak existing DG scenes ──────────
    # ── Los Angeles ─────────────────────────────────────────────
    ("Los Angeles", "Griffith Park", 34.1366, -118.2940, 4310, "One of largest urban parks in US; observatory; Hollywood Sign; canyons"),
    ("Los Angeles", "Elysian Park", 34.0810, -118.2390, 600, "2nd largest LA park; near Dodger Stadium; central"),
    ("Los Angeles", "Exposition Park", 34.0160, -118.2860, 160, "USC adj; museums; stadium; transit; -1 for university"),
    ("Los Angeles", "Kenneth Hahn State Rec Area", 34.0050, -118.3700, 401, "Hills + lake; central LA basin views"),
    ("Los Angeles", "Echo Park", 34.0780, -118.2600, 50, "Iconic lake + lotus; central; too small alone"),

    # ── San Francisco Bay ───────────────────────────────────────
    ("San Francisco Bay", "Golden Gate Park", 37.7694, -122.4862, 1017, "1017 acres; museums; bison; iconic; transit-rich"),
    ("San Francisco Bay", "Presidio", 37.7989, -122.4662, 1500, "Former military post; Golden Gate views; National Park"),
    ("San Francisco Bay", "Lake Merritt / Lakeside Park", 37.8050, -122.2570, 155, "Oakland; tidal lagoon; central; BART"),
    ("San Francisco Bay", "Tilden Regional Park", 37.9000, -122.2470, 2079, "Berkeley hills; redwoods; large"),

    # ── Miami ───────────────────────────────────────────────────
    ("Miami", "Tropical Park", 25.7350, -80.3360, 275, "Lakes; central Miami-Dade; established event venue"),
    ("Miami", "Crandon Park", 25.7180, -80.1580, 808, "Key Biscayne; beach + nature center; less central"),
    ("Miami", "Bayfront Park", 25.7740, -80.1860, 32, "Downtown; small; transit-central"),
    ("Miami", "Amelia Earhart Park", 25.8760, -80.2890, 515, "Lakes; Hialeah; central"),

    # ── Tampa ───────────────────────────────────────────────────
    ("Tampa", "Al Lopez Park", 28.0140, -82.5040, 132, "Lakes; central; near stadium"),
    ("Tampa", "Lettuce Lake Park", 28.0790, -82.3640, 240, "Cypress swamp boardwalk; NE; nature-focused"),
    ("Tampa", "Curtis Hixon Waterfront Park", 27.9510, -82.4620, 8, "Downtown riverfront; small"),

    # ── Nashville ───────────────────────────────────────────────
    ("Nashville", "Centennial Park", 36.1490, -86.8130, 132, "Parthenon replica; central; festival venue"),
    ("Nashville", "Shelby Park", 36.1690, -86.7480, 361, "Cumberland River; E Nashville; trails"),
    ("Nashville", "Percy Warner Park", 36.0680, -86.8990, 2684, "Largest; hilly; horse trails; SW"),
    ("Nashville", "Bicentennial Capitol Mall State Park", 36.1700, -86.7860, 19, "Downtown; small; capitol-adj"),

    # ── Las Vegas ───────────────────────────────────────────────
    ("Las Vegas", "Sunset Park", 36.0640, -115.1170, 324, "Central Clark Co; lake; pavilion"),
    ("Las Vegas", "Floyd Lamb Park", 36.3120, -115.2710, 680, "Lakes; far NW; historic ranch"),
    ("Las Vegas", "Tule Springs Fossil Beds", 36.3800, -115.2700, 22650, "National monument; far NW; minimal infra"),

    # ── Sacramento ──────────────────────────────────────────────
    ("Sacramento", "William Land Park", 38.5390, -121.5040, 166, "Zoo; rose garden; central"),
    ("Sacramento", "Discovery Park", 38.6080, -121.5070, 302, "American River confluence; floods seasonally"),
    ("Sacramento", "McKinley Park", 38.5870, -121.4640, 32, "Historic; small; central E"),

    # ── Orlando ─────────────────────────────────────────────────
    ("Orlando", "Lake Eola Park", 28.5440, -81.3720, 43, "Downtown lake; iconic but small"),
    ("Orlando", "Loch Haven Park", 28.5700, -81.3680, 45, "Museums cluster; central"),
    ("Orlando", "Bill Frederick Park at Turkey Lake", 28.4710, -81.4710, 192, "Lake; W; less central"),

    # ── Baltimore ───────────────────────────────────────────────
    ("Baltimore", "Druid Hill Park", 39.3210, -76.6510, 745, "Zoo; reservoir; 3rd-oldest landscaped park in US"),
    ("Baltimore", "Patterson Park", 39.2890, -76.5790, 137, "Central E; historic; pagoda"),
    ("Baltimore", "Federal Hill Park", 39.2790, -76.6080, 8, "Iconic harbor view; tiny"),

    # ── Milwaukee ───────────────────────────────────────────────
    ("Milwaukee", "Lake Park", 43.0710, -87.8770, 138, "Lake Michigan bluff; Olmsted; central E"),
    ("Milwaukee", "Veterans Park", 43.0470, -87.8920, 78, "Lakefront; festival site; central"),
    ("Milwaukee", "Whitnall Park", 42.9270, -88.0410, 660, "Largest Milw Co park; botanical garden; SW suburb"),

    # ── Salt Lake City ──────────────────────────────────────────
    ("Salt Lake City", "Liberty Park", 40.7460, -111.8760, 80, "Central; pond; tracy aviary"),
    ("Salt Lake City", "Sugar House Park", 40.7220, -111.8580, 110, "Pond + pavilion; central SE"),
    ("Salt Lake City", "This Is The Place Heritage Park", 40.7530, -111.8160, 450, "Historic village; foothills; transit limited"),

    # ── New Orleans ─────────────────────────────────────────────
    ("New Orleans", "City Park", 30.0010, -90.0950, 1300, "Live oaks; art museum; lagoons; iconic; larger than Central Park"),
    ("New Orleans", "Audubon Park", 29.9300, -90.1290, 350, "St Charles streetcar; oaks; -1 for golf course"),
    ("New Orleans", "Crescent Park", 29.9550, -90.0490, 20, "Riverfront; new; small"),

    # ── Honolulu ────────────────────────────────────────────────
    ("Honolulu", "Kapiolani Park", 21.2670, -157.8170, 300, "Diamond Head adj; oldest park in HI; Waikiki"),
    ("Honolulu", "Ala Moana Beach Park", 21.2900, -157.8470, 100, "Beach + lagoon; central"),
    ("Honolulu", "Magic Island", 21.2880, -157.8530, 30, "Ala Moana peninsula; small"),

    # ── Memphis ─────────────────────────────────────────────────
    ("Memphis", "Shelby Farms Park", 35.1500, -89.8550, 4500, "5x Central Park; central E; lake; trails"),
    ("Memphis", "Overton Park", 35.1430, -89.9970, 342, "Old-growth forest; zoo; art college; central; -1 for college adj"),
    ("Memphis", "Tom Lee Park", 35.1320, -90.0610, 31, "Mississippi riverfront; downtown; recently redev"),

    # ── Jacksonville ────────────────────────────────────────────
    ("Jacksonville", "Hanna Park", 30.3120, -81.4090, 450, "Beach + lake; freshwater + saltwater; E coast"),
    ("Jacksonville", "Friendship Fountain Park / Riverside", 30.3220, -81.6580, 50, "Riverfront; downtown"),
    ("Jacksonville", "Hemming Park", 30.3300, -81.6580, 1, "Downtown plaza; tiny"),

    # ── Buffalo ─────────────────────────────────────────────────
    ("Buffalo", "Delaware Park", 42.9380, -78.8650, 350, "Olmsted; zoo adj; central N"),
    ("Buffalo", "South Park", 42.8410, -78.8290, 156, "Olmsted; botanical garden; S"),

    # ── Birmingham ──────────────────────────────────────────────
    ("Birmingham", "Railroad Park", 33.5100, -86.8090, 19, "Downtown; modern; too small"),
    ("Birmingham", "Avondale Park", 33.5340, -86.7720, 36, "Central E; historic"),
    ("Birmingham", "Ruffner Mountain Nature Preserve", 33.5640, -86.7080, 1040, "Forest; minimal infra; central NE"),

    # ── Hartford ────────────────────────────────────────────────
    ("Hartford", "Bushnell Park", 41.7660, -72.6810, 50, "Oldest publicly-funded park in US; capitol-adj; downtown"),
    ("Hartford", "Elizabeth Park", 41.7660, -72.7290, 102, "Rose garden; suburban W; central"),
]
