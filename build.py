import json, html, re, os
E = html.escape
SRC = {
 'IV Leveling':'https://www.icy-veins.com/mists-of-pandaria-classic/brewmaster-monk-leveling',
 'IV Rotation':'https://www.icy-veins.com/mists-of-pandaria-classic/brewmaster-monk-pve-rotation-cooldowns-abilities',
 'IV Talents':'https://www.icy-veins.com/mists-of-pandaria-classic/brewmaster-monk-pve-spec-builds-talents-glyphs',
 'IV Macros':'https://www.icy-veins.com/mists-of-pandaria-classic/monks-best-macros',
 'IV Dungeons':'https://www.icy-veins.com/mists-of-pandaria-classic/mists-of-pandaria-classic-dungeon-guides',
 'Wowhead BM Leveling':'https://www.wowhead.com/mop-classic/guide/classes/monk/brewmaster/tank-leveling-talent-builds-tips',
 'Wowhead BM Rotation':'https://www.wowhead.com/mop-classic/guide/classes/monk/brewmaster/tank-rotation-cooldowns-abilities-pve',
 'Wowhead Leveling Tips':'https://www.wowhead.com/mop-classic/guide/fastest-leveling-tips-mists-of-pandaria-classic',
 'Wowhead Wandering Isle':'https://www.wowhead.com/mop-classic/guide/zones/the-wandering-isle-overview',
 'Wowhead Pandaren':'https://www.wowhead.com/mop-classic/guide/pandaren-race-overview',
 'Wowhead Jade Forest':'https://www.wowhead.com/mop-classic/guide/zones/the-jade-forest-overview',
 'Wowhead Professions':'https://www.wowhead.com/mop-classic/guide/professions/profession-overview-bonuses',
 'Wowhead MoP Phase 1':'https://www.wowhead.com/mop-classic/guide/mists-of-pandaria-classic-phase-1-overview',
 'Wowhead Cata Dungeons':'https://www.wowhead.com/cata/guide/dungeons-overview',
 'Wowhead Cata Zones':'https://www.wowhead.com/cata/guide/leveling-tips-tricks-routes',
 'Wowhead TBC Dungeons':'https://www.wowhead.com/tbc/guide/dungeons-overview-burning-crusade-classic',
 'Wowhead WotLK Dungeons':'https://www.wowhead.com/wotlk/guide/dungeons-overview',
 'Warcraft Tavern Monk Leveling':'https://www.warcrafttavern.com/mop/guides/monk-leveling-guide/',
 'Warcraft Tavern Wandering Isle':'https://www.warcrafttavern.com/mop/guides/pandaren-starting-zone/',
 'Warcraft Tavern Cata 1-60':'https://www.warcrafttavern.com/cataclysm/guides/cataclysm-classic-1-60-leveling-guide/',
 'Warcraft Tavern Get to Pandaria':'https://www.warcrafttavern.com/mop/guides/how-to-get-to-pandaria/',
 'Warcraft Tavern MoP Dungeons':'https://www.warcrafttavern.com/mop/guides/dungeons/',
 'Warcraft Tavern BM Talents':'https://www.warcrafttavern.com/mop/guides/pve-brewmaster-monk-tank-talents-builds-glyphs/',
 'Warcraft Tavern BM Rotation':'https://www.warcrafttavern.com/mop/guides/pve-brewmaster-monk-tank-rotations-cooldowns/',
 'Warcraft Tavern BM Professions':'https://www.warcrafttavern.com/mop/guides/pve-brewmaster-monk-tank-best-professions/',
 'Blizzard Dungeon Level Changes':'http://worldofwarcraft.blizzard.com/en-gb/news/9976910',
 'Warcraft Wiki Monk abilities':'https://warcraft.wiki.gg/wiki/Monk_abilities_(Classic)',
 'Warcraft Wiki A New Fate':'https://warcraft.wiki.gg/wiki/A_New_Fate',
 'Warcraft Wiki Wandering Isle':'https://warcraft.wiki.gg/wiki/Wandering_Isle_storyline',
 'OmniCC (CurseForge)':'https://www.curseforge.com/wow/addons/omni-cc',
 'Wowhead forum: error speech':'https://www.wowhead.com/mop-classic/forums/topic/disabling-your-characters-voice-not-enough-energy-annoying-44911',
 'Blizzard forum: Sound_EnableErrorSpeech':'https://us.forums.blizzard.com/en/wow/t/sound-enableerrorspeech-not-toggling-correctly-in-the-body-of-a-macro/210142',
}
def S(*k):
    return '<span class="src sources">Sources: '+' '.join(f'<a href="{SRC[x]}" target="_blank" rel="noopener">{E(x)}</a>' for x in k)+'</span>'
def W(t): return f'<span class="flag">⚠️ {t}</span>'

SP = json.load(open('/tmp/ids.json'))
def sp(n,label=None):
    v=SP[n]; return f'<a class="sp" href="https://www.wowhead.com/mop-classic/spell={v[0]}" target="_blank" rel="noopener"><img class="ic" src="icons/spells/{v[2]}.jpg" alt="" loading="lazy">{E(label or n)}</a>'

# ---------- abilities by level (Warcraft Wiki Monk abilities (Classic), cross-checked with Wowhead spell tooltips) ----------
GEN=[(1,'Jab'),(3,'Tiger Palm'),(5,'Roll'),(7,'Blackout Kick'),(14,'Provoke'),(18,'Resuscitate'),(20,'Detox'),(20,'Zen Pilgrimage'),(22,'Legacy of the Emperor'),(22,'Touch of Death'),(23,'Swift Reflexes'),(24,'Fortifying Brew'),(26,'Expel Harm'),(28,'Disable'),(30,'Nimble Brew'),(32,'Spear Hand Strike'),(44,'Paralysis'),(44,'Reawaken'),(46,'Spinning Crane Kick'),(54,'Crackling Jade Lightning'),(64,'Healing Sphere'),(68,'Grapple Weapon'),(82,'Zen Meditation'),(87,'Transcendence')]
BM=[(10,'Stance of the Sturdy Ox'),(10,'Dizzying Haze'),(10,'Dual Wield'),(10,'Vengeance'),(11,'Keg Smash'),(18,'Breath of Fire'),(18,'Clash'),(26,'Guard'),(34,'Brewmaster Training'),(36,'Elusive Brew'),(45,'Desperate Measures'),(48,'Avert Harm'),(50,'Leather Specialization'),(56,'Gift of the Ox'),(70,'Summon Black Ox Statue'),(75,'Purifying Brew'),(80,'Mastery: Elusive Brawler')]
TAL={15:'Talent tier 1',30:'Talent tier 2',45:'Talent tier 3',60:'Talent tier 4',75:'Talent tier 5',90:'Talent tier 6'}
def learn(lo,hi):
    items=[]
    for lv,n in sorted(GEN+BM+[(k,v) for k,v in TAL.items()]):
        if lo<=lv<=hi: items.append((lv,n))
    if not items: return ''
    return '<div class="learn"><b>Learned:</b> '+' · '.join(f'{n} <span class="tiny">(L{lv})</span>' for lv,n in items)+'</div>'

# ---------- level path rows ----------
def dtable(rows):
    return '<table class="dng">'+''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a,b in rows)+'</table>'
OLD_DUN=lambda *n:[x for x in OLD if x[0] in n]
OLD=[('Ragefire Chasm','Orgrimmar · 15-21 (enter at 10)'),('The Deadmines','Westfall · 15-21 (enter at 10)'),('Wailing Caverns','The Barrens · 15-25 (enter at 10)'),('Shadowfang Keep','Silverpine Forest · 16-26 (enter at 11)'),('Stormwind Stockade','Stormwind · 20-30 (enter at 15)'),('Blackfathom Deeps','Ashenvale · 20-30 (enter at 15)'),('Gnomeregan','Dun Morogh · 24-34 (enter at 19)'),('Scarlet Monastery: Graveyard','Tirisfal Glades · 26-36 (enter at 21)'),('Scarlet Monastery: Library','Tirisfal Glades · 29-39 (enter at 21)'),('Scarlet Monastery: Armory','Tirisfal Glades · 32-42 (enter at 21)'),('Scarlet Monastery: Cathedral','Tirisfal Glades · 35-45 (enter at 21)'),('Razorfen Kraul','The Barrens · 30-40 (enter at 25)'),('Maraudon: Purple','Desolace · 30-40 (enter at 25)'),('Maraudon: Orange','Desolace · 32-42 (enter at 25)'),('Maraudon: Pristine Waters','Desolace · 34-44 (enter at 25)'),('Uldaman','Badlands · 35-45 (enter at 30)'),('Dire Maul East','Dire Maul · 36-46 (enter at 31)'),('Scholomance','Western Plaguelands · 38-48 (enter at 33)'),('Dire Maul West','Dire Maul · 39-49 (enter at 34)'),('Razorfen Downs','The Barrens · 40-50 (enter at 35)'),('Dire Maul North','Dire Maul · 42-52 (enter at 37)'),('Stratholme: Main Gate','Eastern Plaguelands · 42-52 (enter at 37)'),("Zul'Farrak",'Tanaris · 44-54 (enter at 39)'),('Stratholme: Service Entrance','Eastern Plaguelands · 46-56 (enter at 41)'),('Blackrock Depths: Prison','Blackrock Mountain · 47-57 (enter at 42)'),('Sunken Temple','Swamp of Sorrows · 50-60 (enter at 45)'),('Blackrock Depths: Upper City','Blackrock Mountain · 51-61 (enter at 46)'),('Lower Blackrock Spire','Blackrock Mountain · 55-65 (enter at 48)'),('Upper Blackrock Spire','Blackrock Mountain · 55-65 (enter at 48)')]
def od(*names):
    return dtable([x for n in names for x in OLD if x[0]==n])
# NOTE: dungeon zone names above are only the instance's location; levels/ entry levels are Blizzard's Cataclysm level-change list.

ROWS=[
 dict(lv=(1,10),sum='Wandering Isle (Pandaren start)',zone='Wandering Isle',body='''
  <p>Everything is on the <b>Start</b> tab. You finish around level 10 and then <span class="flag">choose Alliance or Horde</span>.</p>'''+S('Warcraft Tavern Wandering Isle','Warcraft Wiki A New Fate'),learn=(1,9)),
 dict(lv=(10,15),sum='Out of the capital, first zones',zone='Westfall / N. Barrens',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Westfall (10-15). Alternatives for 10-20: Loch Modan, Darkshore, Bloodmyst Isle.</div>
  <div class="fac h"><b>Horde</b>Northern Barrens or Azshara (10-20). Alternatives: Silverpine Forest, Ghostlands.</div></div>
  <p class="note">Use the <b>Hero's Call Board</b> (Alliance, Stormwind Trade District) or <b>Warchief's Command Board</b> (Horde, in front of Grommash Hold, Orgrimmar). They always hand you a breadcrumb to a zone for your level.</p>
  <p><b>Dungeons you can enter now (Cataclysm-era levels):</b></p>'''+od('Ragefire Chasm','The Deadmines','Wailing Caverns','Shadowfang Keep')+
  '<p class="note">Specialization abilities (Stance of the Sturdy Ox, Keg Smash) start at level 10 and 11. Pick Brewmaster at 10.</p>'+W('The pick-your-spec prompt timing at 10 is inferred from the ability table; no page says it outright.')+S('Warcraft Tavern Cata 1-60','Wowhead Cata Zones','Warcraft Wiki Wandering Isle','Warcraft Tavern Monk Leveling','Blizzard Dungeon Level Changes','Warcraft Wiki Monk abilities'),learn=(10,14)),
 dict(lv=(15,20),sum='Redridge / still in the Barrens',zone='Redridge / Barrens',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Redridge Mountains (15-20).</div>
  <div class="fac h"><b>Horde</b>Finish Northern Barrens / Azshara (10-20).</div></div>
  <p><b>Dungeons:</b></p>'''+od('Stormwind Stockade','Blackfathom Deeps')+'<p class="note">Plus the level 10 dungeons above (Deadmines, Ragefire, Wailing Caverns, Shadowfang).</p>'+S('Warcraft Tavern Cata 1-60','Blizzard Dungeon Level Changes'),learn=(15,19)),
 dict(lv=(20,25),sum='Zen Pilgrimage + mount unlock',zone='Duskwood / Ashenvale',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Duskwood (20-25). Alternatives: Wetlands, Hillsbrad Foothills (20-25).</div>
  <div class="fac h"><b>Horde</b>Ashenvale (20-25). Alternatives: Wetlands, Hillsbrad Foothills.</div></div>
  <div class="barch"><b>Level 20 Monk milestone</b> Zen Pilgrimage takes you to the Peak of Serenity (Monk hub: trainers, profession trainers, class quest). A new class quest unlocks every 10 levels, and each repeats as a daily that gives <b>Enlightenment</b> (50% more experience for 1 hour). First mount is also level 20; Pandaren can use the dragon turtles (rare ones need level 20).</div>
  <p><b>Dungeons:</b></p>'''+od('Gnomeregan','Scarlet Monastery: Graveyard')+S('Warcraft Tavern Monk Leveling','Wowhead Pandaren','Warcraft Tavern Cata 1-60','Blizzard Dungeon Level Changes'),learn=(20,24)),
 dict(lv=(25,30),sum='Stranglethorn / Stonetalon',zone='N. Stranglethorn / Stonetalon',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Northern Stranglethorn (25-30). Alternative: Arathi Highlands.</div>
  <div class="fac h"><b>Horde</b>Stonetalon Mountains (25-30). Alternatives: Northern Stranglethorn, Arathi Highlands.</div></div>
  <p><b>Dungeons:</b></p>'''+od('Razorfen Kraul','Maraudon: Purple','Scarlet Monastery: Library')+'<p class="note">Gnomeregan, Scarlet Graveyard, Stockade and Blackfathom are still in range.</p>'+S('Warcraft Tavern Cata 1-60','Blizzard Dungeon Level Changes'),learn=(25,29)),
 dict(lv=(30,35),sum='Cape of Stranglethorn / Southern Barrens',zone='Cape STV / S. Barrens',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Cape of Stranglethorn or The Hinterlands (30-35).</div>
  <div class="fac h"><b>Horde</b>Southern Barrens (30-35) or Desolace (30-40).</div></div>
  <p class="note">At 30 a Monk trainer can teach Dual Specialization (info only).</p>
  <p><b>Dungeons:</b></p>'''+od('Scarlet Monastery: Armory','Maraudon: Orange','Maraudon: Pristine Waters','Uldaman')+S('Warcraft Tavern Cata 1-60','Warcraft Tavern Monk Leveling','Blizzard Dungeon Level Changes'),learn=(30,34)),
 dict(lv=(35,40),sum='Western Plaguelands / Feralas',zone='W. Plaguelands / Feralas',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Western Plaguelands (35-40).</div>
  <div class="fac h"><b>Horde</b>Feralas (35-40). Warcraft Tavern says skip Dustwallow Marsh (unchanged).</div></div>
  <p><b>Dungeons:</b></p>'''+od('Scarlet Monastery: Cathedral','Dire Maul East','Scholomance','Dire Maul West','Razorfen Downs')+S('Warcraft Tavern Cata 1-60','Blizzard Dungeon Level Changes'),learn=(35,39)),
 dict(lv=(40,45),sum='Eastern Plaguelands / Thousand Needles',zone='E. Plaguelands / 1000 Needles',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Eastern Plaguelands (40-45).</div>
  <div class="fac h"><b>Horde</b>Thousand Needles (40-45).</div></div>
  <p><b>Dungeons:</b></p>'''+od('Dire Maul North','Stratholme: Main Gate',"Zul'Farrak")+S('Warcraft Tavern Cata 1-60','Blizzard Dungeon Level Changes'),learn=(40,44)),
 dict(lv=(45,50),sum='Badlands / Felwood / Tanaris',zone='Badlands / Felwood',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Badlands (44-48), then Searing Gorge (47-51) or Burning Steppes (47-52). Warcraft Tavern: don't skip Badlands, the Deathwing quest chain starts there.</div>
  <div class="fac h"><b>Horde</b>Felwood or Tanaris (45-50).</div></div>
  <p><b>Dungeons:</b></p>'''+od('Stratholme: Service Entrance','Blackrock Depths: Prison')+S('Warcraft Tavern Cata 1-60','Blizzard Dungeon Level Changes'),learn=(45,49)),
 dict(lv=(50,55),sum='Swamp of Sorrows / Un\'Goro / Winterspring',zone='Swamp / Un\'Goro',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Swamp of Sorrows (51-55); Burning Steppes still fits.</div>
  <div class="fac h"><b>Horde</b>Un'Goro Crater or Winterspring (50-55).</div></div>
  <div class="barch"><b>Level 50</b> Leather Specialization: from here on wear Leather over Cloth (Warcraft Tavern).</div>
  <p><b>Dungeons:</b></p>'''+od('Sunken Temple','Blackrock Depths: Upper City')+S('Warcraft Tavern Cata 1-60','Warcraft Tavern Monk Leveling','Blizzard Dungeon Level Changes'),learn=(50,54)),
 dict(lv=(55,60),sum='Blasted Lands / Silithus',zone='Blasted Lands / Silithus',body='''
  <div class="two"><div class="fac a"><b>Alliance</b>Blasted Lands (55-60).</div>
  <div class="fac h"><b>Horde</b>Silithus (55-60). Un'Goro/Winterspring should get you to 58.</div></div>
  <p><b>Dungeons:</b></p>'''+od('Lower Blackrock Spire','Upper Blackrock Spire')+'<p class="note">Outland opens at 58, so you don\'t have to finish this zone.</p>'+S('Warcraft Tavern Cata 1-60','Warcraft Tavern Monk Leveling','Blizzard Dungeon Level Changes'),learn=(55,59)),
 dict(lv=(58,70),sum='Outland',zone='Outland',body='''
  <p>Same for both factions. Go to Outland at 58 (Warcraft Tavern: big jump in loot and XP per expansion). Zone ranges: Hellfire Peninsula 58-62 · Zangarmarsh 61-64 · Terokkar Forest 62-66 · Nagrand 64-66 · Blade's Edge Mountains 65-68 · Netherstorm 67-70 · Shadowmoon Valley 67-70.</p>
  <p><b>Dungeons (Burning Crusade Classic ranges):</b></p>'''+dtable([('Hellfire Ramparts','60-62'),('The Blood Furnace','61-63'),('The Slave Pens','62-64'),('The Underbog','63-65'),('Mana-Tombs','64-66'),('Auchenai Crypts','65-67'),('Old Hillsbrad Foothills','66-68'),('Sethekk Halls','67-69'),('The Steamvault','68-70'),('Shadow Labyrinth','69-70'),('The Shattered Halls','69-70'),('Black Morass, Botanica, Mechanar, Arcatraz','70')])+W('Zone ranges come from Wowhead\'s Cataclysm Classic page and dungeon ranges from its Burning Crusade Classic page. I did not find a MoP Classic page restating them.')+S('Wowhead Cata Zones','Wowhead TBC Dungeons','Warcraft Tavern Monk Leveling'),learn=(60,67)),
 dict(lv=(68,80),sum='Northrend',zone='Northrend',body='''
  <p>Go to Northrend at 68 (Warcraft Tavern). Zone ranges: Borean Tundra and Howling Fjord 68-72 · Dragonblight 71-75 · Grizzly Hills 73-75 · Zul'Drak 74-76 · Sholazar Basin 76-78 · Crystalsong Forest, Storm Peaks, Icecrown 77-80.</p>
  <p><b>Dungeons (Wrath Classic ranges):</b></p>'''+dtable([('Utgarde Keep','70-72'),('The Nexus','71-73'),('Azjol-Nerub','72-74'),('Ahn\'kahet: The Old Kingdom','73-75'),('Drak\'Tharon Keep','74-76'),('The Violet Hold','75-77'),('Gundrak','76-78'),('Halls of Stone','77-79'),('Halls of Lightning, Oculus, Utgarde Pinnacle, Culling of Stratholme, Trial of the Champion, Forge of Souls, Pit of Saron, Halls of Reflection','79-80')])+'<div class="barch"><b>Level 70</b> Summon Black Ox Statue. <b>Level 75</b> Purifying Brew, the most important ability in your defensive kit (Wowhead).</div>'+W('Same caveat as Outland: Wowhead Wrath Classic page, not a MoP Classic page.')+S('Wowhead Cata Zones','Wowhead WotLK Dungeons','Wowhead BM Leveling'),learn=(68,79)),
 dict(lv=(80,85),sum='Cataclysm zones',zone='Hyjal / Deepholm / Uldum',body='''
  <p>Zone ranges: Mount Hyjal and Vashj'ir 80-82 · Deepholm 82-83 · Uldum 83-84 · Twilight Highlands 84-85. Mastery unlocks at 80 (it only improves Stagger for you, so Wowhead says mostly ignore it while leveling).</p>
  <p><b>Dungeons (Cataclysm Classic launch table):</b></p>'''+dtable([('Blackrock Caverns','80+'),('Throne of the Tides','80+'),('The Stonecore','81+'),('The Vortex Pinnacle','82+'),('Halls of Origination','83+'),('Lost City of the Tol\'vir','83+'),('Grim Batol','84+')])+'<p class="note">At 85 the Heroic Deadmines and Shadowfang Keep also open.</p>'+W('A different source (PC Gamer) lists slightly different recommended ranges (e.g. 80-83, 82-85). I used Wowhead.')+S('Wowhead Cata Zones','Wowhead Cata Dungeons','Wowhead BM Leveling'),learn=(80,84)),
 dict(lv=(85,90),sum='Pandaria',zone='Jade Forest → Dread Wastes',body='''
  <div class="barch"><b>How you get there at 85</b> Alliance: The King's Command (King Varian, Stormwind Keep), then The Mission. Horde: The Art of War (General Nazgrim, Grommash Hold), All Aboard!, Into the Mists. You land in the Jade Forest. After you reach Paw'don Village (Alliance) or Honeydew Village (Horde), a portal opens in your capital (Alliance: Stormwind, Eastern Earthshrine · Horde: Orgrimmar, Valley of Honor).</div>
  <p><b>Zone order:</b> Jade Forest 85-87 → Valley of the Four Winds 86-90 and Krasarang Wilds 86-90 (either order) → Kun-Lai Summit 86-90 → Townlong Steppes 88-90 → Dread Wastes 89-90. Vale of Eternal Blossoms is level 90 content.</p>
  <p>The Jade Forest storyline (putting the Serpent's Heart together) leads you to the Temple of the Jade Serpent dungeon, and finishing it hands you Moving On, which sends you to the Valley of the Four Winds (Wowhead).</p>
  <p><b>Dungeons:</b></p>'''+dtable([('Temple of the Jade Serpent','85-90 · LFD 85-87 · Jade Forest (56, 58)'),('Stormstout Brewery','85-90 · LFD 85-87 · Valley of the Four Winds (36, 69)'),('Shado-Pan Monastery','87-90 · LFD 87-88 · Kun-Lai Summit (36.8, 47.6)'),("Mogu'shan Palace",'87-90 · LFD 87-88 · Vale of Eternal Blossoms (80.8, 32.7)'),('Gate of the Setting Sun','88-90 · LFD 89 · Vale of Eternal Blossoms (16, 75)'),('Siege of Niuzao Temple','88-90 · LFD 89 · Townlong Steppes (36, 84)')])+'<p class="note">Item level requirements: 325 for the first two, 393 for the rest. Heroics (Scarlet Halls, Scarlet Monastery, Scholomance and the six above) need level 90. Pick up each dungeon\'s quests before you queue (Wowhead, Icy Veins).</p>'+W('Apart from the Jade Forest chain leading into Temple of the Jade Serpent, I did not find a source naming the quest that sends you to each dungeon. Check the quest log when you reach each hub.')+S('Wowhead Leveling Tips','Warcraft Tavern Get to Pandaria','Wowhead Jade Forest','Warcraft Tavern MoP Dungeons','Wowhead MoP Phase 1','IV Dungeons'),learn=(85,90)),
]

def path_html():
    out=[]
    for i,r in enumerate(ROWS):
        lo,hi=r['lv']; lab=f'{lo}-{hi}'
        out.append(f'''<div class="row" data-lo="{lo}" data-hi="{hi}" id="r{i}"><div class="row-head"><button class="chk" aria-label="Mark {lab} done" data-k="r{i}"></button><span class="lv" style="width:54px">{lab}</span><span class="sum">{E(r['sum'])}</span><span class="zone">{E(r['zone'])}</span></div><div class="row-body">{learn(*r['learn']) if 'learn' in r else ''}{r['body']}</div></div>''')
    return '\n'.join(out)

# ---------- Wandering Isle ----------
WI=[
 ('Training grounds with Master Shang Xi (level 1-2)',['Much to Learn → The Lesson of the Iron Bough: grab weapons from a weapon rack and equip them.','The Lesson of the Sandy Fist: destroy 5 training targets.','The Lesson of Stifled Pride: defeat 6 sparring trainees in the sparring hut to the east.','The Lesson of the Burning Scroll: take the stairs (don\'t jump) to the Edict of Temperance on the top floor of the hut.','The Disciple\'s Challenge: beat Jaomin Ro near the gazebo (harmless at this level).']),
 ('Fu\'s Pond (Aysa) and Wu-Song Village (Ji)',['Aysa of the Tushui: go to Merchant Lorvo at Fu\'s Pond. He has The Missing Driver (find Min Dimwind to the north) and Items of Utmost Importance (6 Stolen Training Supplies from Amberleaf Scamps). Then The Way of the Tushui at the cave (a progress bar fills as you fight Amberleaf Troublemakers).','Ji of the Huojin: Wu-Song Village to the north. The Way of the Huojin (8 Fe-Feng), Kindling the Fire (5 Dry Dogwood Root), Fanning the Flames (Shrine of the Summer Breeze, use the small Wind Stone at the big one).','The Spirit\'s Guardian → Shrine of Inner-Light cave (west of the village) → Master Li Fei: The Challenger\'s Fires (light the torch, then the Red, Blue and Violet braziers), Only the Worthy Shall Pass (defeat Li Fei), Huo, the Spirit of Fire.']),
 ('Temple of Five Dawns',['The Passion of Shen-zin Su: bring Huo to the temple (south). The innkeeper Cheng Dawnscrive is there, so you can set your Hearthstone.']),
 ('Singing Pools (Aysa, Jojo, Old Man Liang)',['The Singing Pools: meet Aysa. Whittler Dewei\'s hut on the way teaches gathering and crafting professions.','Stronger Than Reeds (Jojo): 8 Hard Tearwood Reeds. Required, not optional. Water turns you into a frog and cranes will eat you, so stay on dry land.','The Lesson of Dry Fur: cross the balance poles to the Training Bell (only get on a pole from dry land). The Lesson of the Balanced Rock: fight 6 Tushui Monks while standing on a pole.','Finding an Old Friend → The Sun Pearl (from an Ancient Clam in the pool) and The Sting of Learning (6 Water Pincers) → Shu, the Spirit of Water → A New Friend (ride 5 water spouts).']),
 ('Dai-Lo Farmstead (Ji, Wugou)',['The Source of Our Livelihood: ride the yak cart to Ji. Rascals (10 Plump Virmen), Still Good! (3 turnips, 3 carrots, 3 pumpkins), Missing Mallet (Ki-Han Brewery; Raggis can be pulled to the guards), Stronger Than Wood (12 planks, for Jojo), Raucous Rousing (ring the gong), Not In the Face! (ask Shu), then ride the cart back for The Spirit and Body of Shen-Zin Su.']),
 ('Morning Breeze Village (Ji, Dafeng) — Zhao-Ren',['Morning Breeze Village → Rewritten Wisdoms (burn 5 scrolls), Tools of the Enemy (8 brushes), Stronger Than Stone (12 stone blocks, for Jojo).','The Direct Solution (20 Fe-Feng in Fe-Feng Village; Ji helps with AoE), Do No Evil (Ruk-Ruk), Monkey Advisory Warning (8 firework bundles), Stronger Than Bone (Jade Tiger Pillar to Jojo).','Balanced Perspective (Aysa on the ropes) → Dafeng, the Spirit of Air in the Chamber of Whispers (wait for the winds to stop; it only appears after Stronger Than Bone) → Battle for the Skies: use the firework launchers when Zhao-Ren is overhead, then fight him when he lands.']),
 ('Wood of Staves → Pei-Wu Forest → Wreck of the Skyseeker',['Worthy of Passing (Guardian of the Elders), Unwelcome Nature (8 Thornbranch Scamps), Small, But Significant (8 charms), Passing Wisdom, The Suffering of Shen-zin Su (hot air balloon, then talk to Elder Shaopai).','Bidden to Greatness (open the Mandori Village and Pei-Wu gates), Preying on the Predators (9 tigers), Stocking Stalks (10 bamboo), Wrecking the Wreck, Handle With Care (8 charges), Evil from the Seas (8 Darkened), Urgent News.','Delora: None Left Behind (3 sailors), Medical Supplies (8), From Bad to Worse (8 Deepscale Tormentors), An Ancient Evil (Vordraka: dodge the spike wave and the wide cone smash; kill the adds while Aysa tanks), Risking It All (follow Aysa right away or the quest can stick; if it does, abandon and retake it), The Healing of Shen-zin Su (defend the healers).']),
 ('The finale: New Allies → A New Fate',['New Allies: ride the cart back to the Temple of Five Dawns and turn in to the Spirit of Master Shang Xi.','A New Fate: talk to Aysa and Ji if you want to hear their thoughts, then choose Alliance or Horde with the Spirit. After a cutscene you appear outside your new capital and speak to Aysa (Alliance) or Ji (Horde). It cannot be changed by in-game means.']),
]
def wi_html():
    o=[]
    for i,(h,items) in enumerate(WI):
        o.append(f'<div class="card"><h3><label class="ci inline"><input type="checkbox" data-k="wi{i}"><span>{i+1}. {E(h)}</span></label></h3><ul>'+''.join(f'<li>{E(x)}</li>' for x in items)+'</ul></div>')
    return '\n'.join(o)

# ---------- tabs ----------
def talents_html():
    T=[
     ('15','Tiger\'s Lust',[('Celerity','Roll/Chi Torpedo recharge 5 s shorter, +1 charge'),('Tiger\'s Lust','Removes snares/roots from you or a friend and +70% move speed for 6 s, 30 s cooldown'),('Momentum','+25% move speed for 10 s per Roll, stacks to 2')],
      'Icy Veins and Warcraft Tavern both pick Tiger\'s Lust: it gets you out of sticky spots and melee mobs snare a lot. Momentum is the speed-run alternative before you own a mount (up to +50%).',('IV Leveling','Warcraft Tavern Monk Leveling')),
     ('30','Chi Wave',[('Chi Wave','Bounces between up to 7 nearby allies/enemies, 15 s cooldown, free'),('Zen Sphere','Healing/damage sphere, 10 s cooldown, free'),('Chi Burst','40-yard cone heal/damage, 30 s cooldown')],
      'All three leveling guides lead with Chi Wave (damage and healing at once, free). Wowhead says swap to Chi Burst for big dungeon pulls. Zen Sphere is the weakest solo.',('IV Leveling','Warcraft Tavern Monk Leveling','Wowhead BM Leveling')),
     ('45','Chi Brew',[('Power Strikes','Extra Chi from some abilities (20 s internal cooldown)'),('Ascension','+1 max Chi, +15% Energy regen'),('Chi Brew','Instantly gain 2 Chi, 45 s cooldown; Wowhead: also 5 Elusive Brew stacks per cast')],
      'My pick: Chi Brew. Icy Veins calls it excellent for dungeons and group content and Warcraft Tavern picks it (fast fight starts). Wowhead says pure solo questing prefers Power Strikes; Warcraft Tavern calls Ascension good for steady energy, especially AoE. All three are fine.',('IV Leveling','Warcraft Tavern Monk Leveling','Wowhead BM Leveling')),
     ('60','Charging Ox Wave',[('Ring of Peace','Silence/disarm ring, 45 s cooldown'),('Charging Ox Wave','30-yard line stun for 3 s, 30 s cooldown'),('Leg Sweep','5-yard stun for 5 s, 45 s cooldown')],
      'Icy Veins and Warcraft Tavern both pick Charging Ox Wave for leveling (shortest cooldown). Leg Sweep is the endgame dungeon default per Warcraft Tavern\'s tank guide.',('IV Leveling','Warcraft Tavern Monk Leveling','Warcraft Tavern BM Talents')),
     ('75','Diffuse Magic',[('Healing Elixirs','Heals 15% max health when you use a Brew (internal cooldown)'),('Dampen Harm','Halves the next 3 big hits, 1.5 min cooldown'),('Diffuse Magic','-90% magic damage for 6 s and reflects spells')],
      'Icy Veins and Warcraft Tavern pick Diffuse Magic for leveling. Icy Veins calls Dampen Harm "basically useless" while leveling because quest mobs seldom hit that hard (it becomes the default pick in raids).',('IV Leveling','Warcraft Tavern Monk Leveling','Warcraft Tavern BM Talents')),
     ('90','Rushing Jade Wind / Xuen',[('Rushing Jade Wind','AoE option, best at 3+ targets'),('Invoke Xuen, the White Tiger','Single-target option; Xuen also taunts'),('Chi Torpedo','Longer, healing Roll')],
      'Only matters if you reach 90. Warcraft Tavern: Rushing Jade Wind for AoE pulls, Xuen for single targets, and you swap between them.',('Warcraft Tavern BM Talents','IV Talents')),
    ]
    o=[]
    for lv,pick,opts,why,srcs in T:
        o.append(f'<div class="card tier"><h3>Level {lv}: <span class="pick">{E(pick)}</span></h3><table>'+''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td></tr>' for a,b in opts)+f'</table><p class="note">{E(why)}</p>{S(*srcs)}</div>')
    return '\n'.join(o)

def build():
    ids=json.load(open('/tmp/ids.json'))
    spells={n:{'i':v[2],'u':f'https://www.wowhead.com/mop-classic/spell={v[0]}'} for n,v in ids.items()}
    spells['Food']={'i':'inv_misc_food_15'}; spells['Hearthstone']={'i':'inv_misc_rune_01'}; spells['Mount']={'i':'ability_mount_charger'}
    data={'spells':spells}
    page=open('template.html').read()
    page=page.replace('{{PATH}}',path_html()).replace('{{WI}}',wi_html()).replace('{{TALENTS}}',talents_html())
    # inline sp() helpers {sp:Name}
    page=re.sub(r'\{sp:([^}]+)\}',lambda m:sp(m.group(1)),page)
    page=re.sub(r'\{S:([^}]+)\}',lambda m:S(*[x.strip() for x in m.group(1).split('|')]),page)
    page=re.sub(r'\{W:([^}]+)\}',lambda m:W(m.group(1)),page)
    page=page.replace('{{DATA}}','window.SPELLS='+json.dumps(spells)+';')
    open('index.html','w').write(page)
    icons=sorted({v['i'] for v in spells.values()}|{'classicon_monk'})
    files=['./','index.html','style.css','app.js','manifest.webmanifest','icons/icon-180.png','icons/icon-192.png','icons/icon-512.png']+[f'icons/spells/{i}.jpg' for i in icons]
    sw=open('sw.js').read()
    sw=re.sub(r"const C='gm-v\d+',F=\[[^\]]*\]","const C='gm-v1',F="+json.dumps(files),sw)
    open('sw.js','w').write(sw)
if __name__=='__main__': build()
