"""
my fav relays list
2023/03
"""

"""
NIP-11
 "name": <string identifying relay>,
 "description": <string with detailed information>,
 "pubkey": <administrative contact pubkey>,
 "contact": <administrative alternate contact>,
 "supported_nips": <a list of NIP numbers supported by the relay>,
 "software": <string identifying relay software URL>,
 "version": <string version identifier>
"""
nip_11_struct = [ "name","description","pubkey","contact","supported_nips","software","version"]
nip_11_struct_adv = [ "name","description","pubkey","contact","supported_nips","software","version","limitation"]



relays_list = [
"wss://relay.damus.io",
"wss://relay.plebstr.com",
"wss://nostr.mnethome.de",
"wss://relay.snort.social/",
#"wss://nostr.wine/",
#"wss://nostr-pub.wellorder.net",
]


relays_big_list = [
"wss://relay.damus.io",
"wss://relay.plebstr.com",
"wss://relay.nostrplebs.com",
"wss://nostr.mnethome.de",
"wss://nostr-pub.wellorder.net",
"wss://at.nostrworks.com",
"wss://deschooling.us",
"wss://knostr.neutrine.com",
"wss://node01.nostress.cc",
"wss://nos.lol",
"wss://nostr.anchel.nl",
"wss://no.str.cr",
"wss://eden.nostr.land",
"wss://nostr-01.bolt.observer",
"wss://nostr-1.nbo.angani.co",
"wss://nostr3.actn.io",
"wss://nostr.sidnlabs.nl",
"wss://nostr.wine",
"wss://nostr.8e23.net",
"wss://nostr.actn.io",
"wss://nostr.bch.ninja",
"wss://nostr.bitcoiner.social",
"wss://nostr.bongbong.com",
"wss://nostr.bostonbtc.com",
"wss://nostr.cercatrova.me",
"wss://nostr.coollamer.com",
"wss://nostr.corebreach.com",
"wss://nostr.delo.software",
"wss://nostr-dev.wellorder.net",
"wss://nostr.drss.io",
"wss://nostr.easydns.ca",
"wss://nostr.einundzwanzig.space",
"wss://nostrex.fly.dev",
"wss://nostr.fmt.wiz.biz",
"wss://nostr.gromeul.eu",
"wss://nostr.hackerman.pro",
"wss://nostr.handyjunky.com",
"wss://nostr.hugo.md",
"wss://nostrical.com",
"wss://nostrich.friendship.tw",
"wss://nostr.kollider.xyz",
"wss://nostr.lu.ke",
"wss://nostr.mikedilger.com",
"wss://nostr.milou.lol",
"wss://nostr.mom",
"wss://nostr.mouton.dev",
"wss://nostr.nodeofsven.com",
"wss://nostr.ownscale.org",
"wss://nostr.orangepill.dev",
"wss://nostr.oxtr.dev",
"wss://nostr-pub1.southflorida.ninja",
"wss://nostr-pub.wellorder.net",
"wss://nostr-relay.bitcoin.ninja",
"wss://nostr-relay.derekross.me",
"wss://nostr.zebedee.cloud",
"wss://nostr-relay.lnmarkets.com",
"wss://nostr-relay.schnitzel.world",
"wss://nostr.bitcoin.sex",
"wss://relay.nostrich.de",
"wss://nostr.roundrockbitcoiners.com",
"wss://nostr.screaminglife.io",
"wss://nostr.sectiontwo.org",
"wss://nostr.semisol.dev",
"wss://nostr.shawnyeager.net",
"wss://nostr.slothy.win",
"wss://nostr.supremestack.xyz",
"wss://nostr.swiss-enigma.ch",
"wss://nostr.uselessshit.co",
"wss://nostr-verified.wellorder.net",
"wss://nostr-verif.slothy.win",
"wss://nostr.vulpem.com",
"wss://nostr.w3ird.tech",
"wss://nostr.walletofsatoshi.com",
"wss://nostr.zaprite.io",
"wss://nostr.zebedee.cloud",
"wss://relay.current.fyi",
"wss://relay.cryptocculture.com",
"wss://relay.lexingtonbitcoin.org",
"wss://relay.ryzizub.com",
"wss://relay.n057r.club",
"wss://relay.nostr.au",
"wss://relay.nostr.band",
"wss://relay.nostr.bg",
"wss://nostramsterdam.vpx.moe",
"wss://relay.nostrgraph.net",
"wss://relay.nostrich.de",
"wss://relay.nostrid.com",
"wss://relay.nostr.nu",
"wss://relay.nostr.ro",
"wss://relay.nostr.scot",
"wss://relay.austrich.net",
"wss://relay.sendstr.com",
"wss://relay.snort.social",
"wss://relay.taxi",
"wss://relay-pub.deschooling.us",
"wss://relay.ryzizub.com",
"wss://nostr-01.dorafactory.org",
"wss://rsslay.nostr.moe",
"wss://sg.qemura.xyz",
"wss://paid.no.str.cr",
]


# ------------------------------
#"wss://relay.nostr.ch",
#"wss://nostr.onsats.org",
#"wss://lightningrelay.com",
#"wss://nostr.massmux.com",
#"wss://nostr.noones.com",
#"wss://nostr.relayer.se",
#"wss://nostr.rocks",
#"wss://relay.minds.com/nostr/v1/ws",
#"wss://relay.nvote.co",
#"wss://relay.nvote.co:443",
#"wss://rasca.asnubes.art",
#"wss://brb.io",
#"wss://public.nostr.swissrouting.com",
#"wss://nostr.sandwich.farm",
#"wss://relay.nostr.info",
#"wss://relay.nostr.express",
#"wss://nostr.middling.mydns.jp",
