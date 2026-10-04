#include "digimon.h"
#include "i18n.h"

DigiPet digiPet;

// Digital Monster COLOR Ver.1-5 core rosters. The numeric power is used only
// as a compact balance seed; TamaPoke calculates four independent stats.
#define D(n,v,s,p,y) {n,v,s,p,y}
const DigiSpecies DIGI_SPECIES[] = {
 D("Botamon",1,0,10,0),D("Koromon",1,1,15,0),D("Agumon",1,2,30,0),D("Betamon",1,2,25,3),
 D("Greymon",1,3,50,0),D("Tyranomon",1,3,45,3),D("Devimon",1,3,50,1),D("Meramon",1,3,45,0),D("Airdramon",1,3,50,2),D("Seadramon",1,3,45,3),D("Numemon",1,3,40,3),
 D("MetalGreymon_Virus",1,4,100,0),D("Mamemon",1,4,85,1),D("Monzaemon",1,4,100,3),D("BlitzGreymon",1,5,170,0),D("BanchoMamemon",1,5,150,1),D("ShinMonzaemon",1,5,170,3),
 D("Punimon",2,0,10,0),D("Tsunomon",2,1,15,0),D("Gabumon",2,2,30,1),D("Elecmon",2,2,25,2),
 D("Kabuterimon",2,3,50,1),D("Garurumon",2,3,45,2),D("Angemon",2,3,50,0),D("Yukidarumon",2,3,45,3),D("Birdramon",2,3,50,2),D("Whamon",2,3,45,3),D("Vegimon",2,3,40,3),
 D("SkullGreymon",2,4,100,0),D("MetalMamemon",2,4,85,1),D("Vademon",2,4,100,2),D("SkullMammon",2,5,170,1),D("CresGarurumon",2,5,150,2),D("Ebemon",2,5,170,0),
 D("Poyomon",3,0,10,0),D("Tokomon",3,1,15,0),D("Patamon",3,2,30,2),D("Kunemon",3,2,25,1),
 D("Unimon",3,3,50,2),D("Centalmon",3,3,45,2),D("Ogremon",3,3,50,0),D("Bakemon",3,3,45,2),D("Shellmon",3,3,50,1),D("Drimogemon",3,3,45,0),D("Scumon",3,3,40,3),
 D("Andromon",3,4,100,1),D("Giromon",3,4,85,2),D("Etemon",3,4,100,0),D("Chimairamon",3,4,100,3),D("HiAndromon",3,5,150,1),D("Gokumon",3,5,170,0),D("BanchoLeomon",3,5,180,2),
 D("Yuramon",4,0,10,0),D("Tanemon",4,1,15,0),D("Piyomon",4,2,30,2),D("Palmon",4,2,25,3),
 D("Monochromon",4,3,50,1),D("Cockatrimon",4,3,45,2),D("Leomon",4,3,50,0),D("Kuwagamon",4,3,45,0),D("Coelamon",4,3,50,3),D("Mojyamon",4,3,45,1),D("Nanimon",4,3,40,3),
 D("Megadramon",4,4,100,0),D("Piccolomon",4,4,85,2),D("Digitamamon",4,4,100,3),D("Darkdramon",4,5,170,0),D("BloomLordmon",4,5,150,2),D("Gankoomon",4,5,170,1),
 D("Zurumon",5,0,10,0),D("Pagumon",5,1,15,0),D("Gazimon",5,2,30,0),D("Gizamon",5,2,25,2),
 D("DarkTyranomon",5,3,50,0),D("Cyclomon",5,3,45,1),D("Devidramon",5,3,50,2),D("Tuskmon",5,3,45,0),D("Flymon",5,3,50,2),D("Deltamon",5,3,45,1),D("Raremon",5,3,40,3),
 D("MetalTyranomon",5,4,100,0),D("Nanomon",5,4,85,2),D("ExTyranomon",5,4,100,3),D("Mugendramon",5,5,170,0),D("Raidenmon",5,5,150,2),D("Gaioumon",5,5,180,1),
 // DF/DX entries use version 0 so they have one stable Dex/SD identity even
 // when their materials originate in two different COLOR versions.
 D("Omnimon Alter-S",0,5,220,0),D("Chaosmon",0,5,215,0),D("Millenniummon",0,5,225,3),D("Chaosdramon",0,5,210,1),
// Pendulum COLOR ZERO/1-5. Version codes: P0=10, P1=11 ... P5=15.
// The final entries in each group are combination-only Ultimate+ species.
 D("Bubbmon",11,0,10,3),
 D("Mochimon",11,1,15,0),
 D("Angoramon",11,2,30,1),
 D("Tentomon",11,2,30,2),
 D("Gottsumon",11,2,30,3),
 D("Otamamon",11,2,30,0),
 D("SymbareAngoramon",11,3,50,2),
 D("Kabuterimon",11,3,50,3),
 D("Tortamon",11,3,50,0),
 D("Tailmon",11,3,50,1),
 D("Monochromon",11,3,50,2),
 D("Starmon",11,3,50,3),
 D("Gekomon",11,3,50,0),
 D("Kuwagamon",11,3,50,1),
 D("Lamortmon",11,4,95,3),
 D("AtlurKabuterimonBlue",11,4,95,0),
 D("Jyagamon",11,4,95,1),
 D("Angewomon",11,4,95,2),
 D("Triceramon",11,4,95,3),
 D("Piccolomon",11,4,95,0),
 D("TonosamaGekomon",11,4,95,1),
 D("Okuwamon",11,4,95,2),
 D("Diarbbitmon",11,5,170,0),
 D("HerakleKabuterimon",11,5,170,1),
 D("Blastmon",11,5,170,2),
 D("Holydramon",11,5,170,3),
 D("SaberLeomon",11,5,170,0),
 D("ElDoradimon",11,5,170,1),
 D("MetalEtemon",11,5,170,2),
 D("GranKuwagamon",11,5,170,3),
 D("Mastemon",11,5,220,1),
 D("Tlalocmon",11,5,220,2),
 D("Pitchmon",12,0,10,0),
 D("Pukamon",12,1,15,1),
 D("Gomamon",12,2,30,2),
 D("Jellymon",12,2,30,3),
 D("Ganimon",12,2,30,0),
 D("Shakomon",12,2,30,1),
 D("Rukamon",12,3,50,3),
 D("Ikkakumon",12,3,50,0),
 D("TeslaJellymon",12,3,50,1),
 D("Seadramon",12,3,50,2),
 D("Coelamon",12,3,50,3),
 D("Ebidramon",12,3,50,0),
 D("Octmon",12,3,50,1),
 D("Gesomon",12,3,50,2),
 D("WhamonPerfect",12,4,95,0),
 D("Zudomon",12,4,95,1),
 D("Thetismon",12,4,95,2),
 D("MegaSeadramon",12,4,95,3),
 D("Anomalocarimon",12,4,95,0),
 D("Hangyomon",12,4,95,1),
 D("Dagomon",12,4,95,2),
 D("MarinDevimon",12,4,95,3),
 D("MarinAngemon",12,5,170,1),
 D("Amphimon",12,5,170,2),
 D("Plesiomon",12,5,170,3),
 D("JumboGamemon",12,5,170,0),
 D("MetalSeadramon",12,5,170,1),
 D("Cthyllamon",12,5,170,2),
 D("Pukumon",12,5,170,3),
 D("Vikemon",12,5,170,0),
 D("Aegisdramon",12,5,220,2),
 D("Mitamamon",12,5,220,3),
 D("Mokumon",13,0,10,1),
 D("PetitMeramon",13,1,15,2),
 D("Bakumon",13,2,30,3),
 D("Candmon",13,2,30,0),
 D("Loogamon",13,2,30,1),
 D("PicoDevimon",13,2,30,2),
 D("Hanumon",13,3,50,0),
 D("Garurumon",13,3,50,1),
 D("Meramon",13,3,50,2),
 D("Wizarmon",13,3,50,3),
 D("Devimon",13,3,50,0),
 D("Bakemon",13,3,50,1),
 D("Dokugumon",13,3,50,2),
 D("Loogarmon",13,3,50,3),
 D("Mammon",13,4,95,1),
 D("WereGarurumon",13,4,95,2),
 D("DeathMeramon",13,4,95,3),
 D("Pumpmon",13,4,95,0),
 D("Soloogarmon",13,4,95,1),
 D("Vamdemon",13,4,95,2),
 D("Fantomon",13,4,95,3),
 D("LadyDevimon",13,4,95,0),
 D("SkullMammon",13,5,170,2),
 D("Anubimon",13,5,170,3),
 D("Boltmon",13,5,170,0),
 D("NoblePumpmon",13,5,170,1),
 D("Fenriloogamon",13,5,170,2),
 D("Callismon",13,5,170,3),
 D("Piemon",13,5,170,0),
 D("Demon",13,5,170,1),
 D("Mastemon",13,5,220,3),
 D("Voltobautamon",13,5,220,0),
 D("Nyokimon",14,0,10,2),
 D("Pyocomon",14,1,15,3),
 D("Piyomon",14,2,30,0),
 D("Pteromon",14,2,30,1),
 D("Palmon",14,2,30,2),
 D("Floramon",14,2,30,3),
 D("Mushmon",14,2,30,0),
 D("Vdramon",14,3,50,1),
 D("Birdramon",14,3,50,2),
 D("Galemon",14,3,50,3),
 D("Togemon",14,3,50,0),
 D("Kiwimon",14,3,50,1),
 D("RedVegimon",14,3,50,2),
 D("Woodmon",14,3,50,3),
 D("AeroVdramon",14,4,95,2),
 D("Garudamon",14,4,95,3),
 D("GrandGalemon",14,4,95,0),
 D("Lilimon",14,4,95,1),
 D("Blossomon",14,4,95,2),
 D("Delumon",14,4,95,3),
 D("Jyureimon",14,4,95,0),
 D("Gerbemon",14,4,95,1),
 D("UlforceVdramon",14,5,170,3),
 D("Hououmon",14,5,170,0),
 D("Zephagamon",14,5,170,1),
 D("Griffomon",14,5,170,2),
 D("Rosemon",14,5,170,3),
 D("Rafflesimon",14,5,170,0),
 D("Hydramon",14,5,170,1),
 D("Pinochimon",14,5,170,2),
 D("Mitamamon",14,5,220,0),
 D("Cernumon",14,5,220,1),
 D("Choromon",15,0,10,3),
 D("Caprimon",15,1,15,0),
 D("ToyAgumon",15,2,30,1),
 D("Kokuwamon",15,2,30,2),
 D("Hagurumon",15,2,30,3),
 D("Commandramon",15,2,30,0),
 D("Greymon",15,3,50,2),
 D("Revolmon",15,3,50,3),
 D("Clockmon",15,3,50,0),
 D("Thunderballmon",15,3,50,1),
 D("Tankmon",15,3,50,2),
 D("Guardromon",15,3,50,3),
 D("Mechanorimon",15,3,50,0),
 D("HiCommandramon",15,3,50,1),
 D("MetalGreymon",15,4,95,3),
 D("Andromon",15,4,95,0),
 D("Cyberdramon",15,4,95,1),
 D("BigMamemon",15,4,95,2),
 D("Knightmon",15,4,95,3),
 D("Megadramon",15,4,95,0),
 D("WaruMonzaemon",15,4,95,1),
 D("Cargodramon",15,4,95,2),
 D("WarGreymon",15,5,170,0),
 D("HiAndromon",15,5,170,1),
 D("MetalGarurumon",15,5,170,2),
 D("Brigadramon",15,5,170,3),
 D("ZekeGreymon",15,5,170,0),
 D("Mugendramon",15,5,170,1),
 D("VenomVamdemon",15,5,170,2),
 D("Ragnamon",15,5,170,3),
 D("Omegamon",15,5,220,1),
 D("Chaosdramon",15,5,220,2),
 D("YukimiBotamon",10,0,10,2),
 D("Nyaromon",10,1,15,3),
 D("Agumon",10,2,30,0),
 D("Plotmon",10,2,30,1),
 D("Gabumon",10,2,30,2),
 D("Gammamon",10,2,30,3),
 D("Greymon",10,3,50,1),
 D("Leomon",10,3,50,2),
 D("Tailmon",10,3,50,3),
 D("Garurumon",10,3,50,0),
 D("Angemon",10,3,50,1),
 D("BetelGammamon",10,3,50,2),
 D("Igamon",10,3,50,3),
 D("KausGammamon",10,3,50,0),
 D("WezenGammamon",10,3,50,1),
 D("GulusGammamon",10,3,50,2),
 D("MetalGreymon",10,4,95,2),
 D("Asuramon",10,4,95,3),
 D("WereGarurumon",10,4,95,0),
 D("HolyAngemon",10,4,95,1),
 D("Angewomon",10,4,95,2),
 D("Canoweissmon",10,4,95,3),
 D("MetalMamemon",10,4,95,0),
 D("Regulusmon",10,4,95,1),
 D("WarGreymon",10,5,170,3),
 D("Siriusmon",10,5,170,0),
 D("Dominimon",10,5,170,1),
 D("MetalGarurumon",10,5,170,2),
 D("Quantumon",10,5,170,3),
 D("Arcturusmon",10,5,170,0),
 D("Omegamon",10,5,220,0),
 D("Mastemon",10,5,220,1),
 D("Proximamon",10,5,220,2),
 // Digimon Unlimited (DMUL) sprite-source expansion. The 37 requested Child+
 // forms stay append-only, and selected DMUL Baby I/II sprites are appended
 // after them so existing draft IDs 283-319 never move. The egg now starts
 // at Baby I and uses device-like Route A-D evolution conditions.
 D("Guilmon",16,2,32,0),
 D("Growmon",16,3,52,0),
 D("MegaloGrowlmon",16,4,100,0),
 D("Dukemon",16,5,178,1),
 D("Dukemon Crimson Mode",16,5,230,0),
 D("Keramon",17,2,30,2),
 D("Kurisarimon",17,3,48,1),
 D("Infermon",17,4,98,2),
 D("Diablomon",17,5,178,2),
 D("Lunamon",18,2,30,2),
 D("Lekismon",18,3,50,2),
 D("Crescemon",18,4,96,2),
 D("Dianamon",18,5,172,2),
 D("Gaomon",19,2,30,2),
 D("Gaogamon",19,3,50,2),
 D("MachGaogamon",19,4,96,2),
 D("MirageGaogamon",19,5,174,2),
 D("Renamon",20,2,30,2),
 D("Kyubimon",20,3,50,2),
 D("Taomon",20,4,96,3),
 D("Sakuyamon",20,5,174,1),
 D("Hackmon",21,2,32,0),
 D("BaoHackmon",21,3,52,0),
 D("SaviorHackmon",21,4,100,0),
 D("Jesmon",21,5,180,0),
 D("DORUmon",16,2,32,0),
 D("DORUgamon",16,3,52,0),
 D("DORUguremon",16,4,100,0),
 D("DORUgoramon",16,5,180,0),
 D("Raptordramon",16,3,52,2),
 D("Grademon",16,4,102,0),
 D("Alphamon",16,5,184,1),
 D("Ryudamon",16,2,32,1),
 D("Ginryumon",16,3,52,1),
 D("Hisyaryumon",16,4,100,1),
 D("Ouryumon",16,5,182,0),
 D("Alphamon Ouryuken",16,5,235,0),
 // Selected Digimon Unlimited Baby I / Baby II roster. These are real DMUL
 // field/secret-egg sprites and intentionally keep their dedicated DMUL version
 // even when a same-named classic DMC/Pendulum entry already exists.
 D("Dodomon",16,0,8,0),
 D("Dorimon",16,1,14,0),
 D("Gigimon",16,1,14,0),
 D("Kuramon",17,0,8,3),
 D("Tsumemon",17,1,14,3),
 D("Pitchmon",18,0,8,2),
 D("Moonmon",18,1,14,2),
 D("Bubbmon",19,0,8,1),
 D("Mochimon",19,1,14,1),
 D("Mokumon",20,0,8,3),
 D("Pokomon",20,1,14,0),
 D("Botamon",21,0,8,0),
 D("Koromon",21,1,14,0),

 // v3.93.0 catalog-only append: r8 resource-survey roster. Existing IDs 0..332 stay fixed.
 D("Dracomon",16,2,32,0),
 D("Coredramon Blue",16,3,52,0),
 D("Coredramon Green",16,3,52,0),
 D("GeoGreymon",16,3,52,0),
 D("Wingdramon",16,4,100,0),
 D("Groundramon",16,4,100,0),
 D("RizeGreymon",16,4,100,0),
 D("Slayerdramon",16,5,180,0),
 D("Breakdramon",16,5,180,0),
 D("Examon",16,5,180,0),
 D("Dracmon",17,2,32,0),
 D("Ghostmon",17,2,32,0),
 D("Tsukaimon",17,2,32,2),
 D("Soulmon",17,3,52,0),
 D("IceDevimon",17,3,52,0),
 D("Sangloupmon",17,3,52,0),
 D("Fangmon",17,3,52,0),
 D("Witchmon",17,3,52,2),
 D("Boogiemon",17,3,52,0),
 D("Matadormon",17,4,100,0),
 D("Astamon",17,4,100,0),
 D("NeoDevimon",17,4,100,2),
 D("SkullBaluchimon",17,4,100,0),
 D("Wisemon",17,4,100,2),
 D("Cerberumon",17,4,100,0),
 D("GranDracmon",17,5,180,0),
 D("Barbamon",17,5,180,2),
 D("Lilithmon",17,5,180,2),
 D("BeelStarmon",17,5,180,0),
 D("Murmukusmon",17,5,180,2),
 D("Swimmon",18,2,32,2),
 D("Kamemon",18,2,32,2),
 D("Sangomon",18,2,32,2),
 D("Penmon",18,2,32,2),
 D("Dolphmon",18,3,52,2),
 D("Tylomon",18,3,52,2),
 D("Tobiumon",18,3,52,2),
 D("Orcamon",18,3,52,2),
 D("MarinChimairamon",18,4,100,3),
 D("Gusokumon",18,4,100,3),
 D("WaruSeadramon",18,4,100,3),
 D("Divemon",18,4,100,3),
 D("Regalecusmon",18,5,180,3),
 D("Neptunemon",18,5,180,3),
 D("Leviamon",18,5,180,3),
 D("AncientMermaimon",18,5,180,3),
 D("Pomumon",19,2,32,2),
 D("Funbeemon",19,2,32,2),
 D("Lalamon",19,2,32,2),
 D("Parasaurmon",19,3,52,2),
 D("Sunflowmon",19,3,52,2),
 D("Waspmon",19,3,52,2),
 D("Ajatarmon",19,4,100,2),
 D("CannonBeemon",19,4,100,2),
 D("Lilamon",19,4,100,2),
 D("GrandisKuwagamon",19,5,180,2),
 D("TigerVespamon",19,5,180,2),
 D("Lotusmon",19,5,180,2),
 D("Bancho Lilimon",19,5,180,2),
 D("Impmon",20,2,32,0),
 D("Gazimon",20,2,32,0),
 D("Goblimon",20,2,32,0),
 D("Phascomon",20,2,32,2),
 D("Sorcermon",20,3,52,2),
 D("BlackTailmon",20,3,52,0),
 D("Musyamon",20,3,52,0),
 D("Fugamon",20,3,52,0),
 D("Baalmon",20,4,100,2),
 D("Bastemon",20,4,100,0),
 D("Archnemon",20,4,100,0),
 D("SkullSatamon",20,4,100,0),
 D("Beelzebumon",20,5,180,0),
 D("Gulfmon",20,5,180,0),
 D("Plutomon",20,5,180,2),
 D("Kuzuhamon",20,5,180,2),
 D("Kudamon",21,2,32,1),
 D("Lucemon",21,2,32,1),
 D("Patamon",21,2,32,1),
 D("Morphomon",21,2,32,1),
 D("Gladimon",21,3,52,1),
 D("Reppamon",21,3,52,1),
 D("Pidmon",21,3,52,1),
 D("Darcmon",21,3,52,1),
 D("Chirinmon",21,4,100,1),
 D("Hippogriffomon",21,4,100,1),
 D("Mistymon",21,4,100,1),
 D("Seraphimon",21,5,180,1),
 D("Ophanimon",21,5,180,1),
 D("Duftmon",21,5,180,1),
 D("Craniummon",21,5,180,1),
 D("Sleipmon",21,5,180,1),
 D("Armagemon",17,5,225,0),
 D("GraceNovamon",0,5,225,1),
 D("Coronamon",21,2,32,1),
 D("Firamon",21,3,52,1),
 D("Flaremon",21,4,100,1),
 D("Apollomon",21,5,180,1),
 D("MirageGaogamon Burst Mode",19,5,225,2),
 D("Beelzebumon Blast Mode",20,5,225,0),
 D("JESmon GX",21,5,225,1),
 D("Lucemon Falldown Mode",21,5,225,1),
 D("Lucemon Satan Mode",21,5,225,1),
 D("Chibomon",22,0,8,0),
 D("DemiVeemon",22,1,14,0),
 D("Veemon",22,2,32,0),
 D("Wormmon",22,2,32,0),
 D("Hawkmon",22,2,32,0),
 D("Armadillomon",22,2,32,0),
 D("ExVeemon",22,3,52,0),
 D("Snimon",22,3,52,0),
 D("Aquilamon",22,3,52,0),
 D("Ankylomon",22,3,52,0),
 D("JewelBeemon",22,4,100,1),
 D("Yatagaramon",22,4,100,1),
 D("Meteormon",22,4,100,1),
 D("Paildramon",22,4,225,1),
 D("Dinobeemon",22,4,225,1),
 D("Silphymon",22,4,225,1),
 D("Shakkoumon",22,4,225,1),
 D("Valkyrimon",22,5,180,0),
 D("Ravmon",22,5,180,0),
 D("Imperialdramon Dragon Mode",22,5,225,1),
 D("Imperialdramon Fighter Mode",22,5,225,1),
 D("Imperialdramon Paladin Mode",22,5,225,1),
 D("Imperialdramon OmegaX",22,5,255,0),
};
#undef D
const uint16_t DIGI_SPECIES_COUNT = sizeof(DIGI_SPECIES)/sizeof(DIGI_SPECIES[0]);
static_assert(DIGI_SPECIES_COUNT <= DIGI_SPECIES_CAP, "increase DIGI_SPECIES_CAP");
#include "digimon_types.generated.h"

// Display-only Korean names. DIGI_SPECIES[].name deliberately remains the
// stable ASCII key used by type rules, serial tooling and SD sprite matching.
static const char *const DIGI_NAMES_KO[] = {
 "보타몬",
 "코로몬",
 "아구몬",
 "베타몬",
 "그레이몬",
 "티라노몬",
 "데블몬",
 "메라몬",
 "에어드라몬",
 "시드라몬",
 "워매몬",
 "메탈그레이몬(바이러스)",
 "콩알몬",
 "퍼펫몬",
 "블리츠그레이몬",
 "반쵸콩알몬",
 "신퍼펫몬",
 "푸니몬",
 "츠노몬",
 "파피몬",
 "에렉몬",
 "캅테리몬",
 "가루몬",
 "엔젤몬",
 "프리지몬",
 "버드라몬",
 "고래몬",
 "베지몬",
 "스컬그레이몬",
 "메탈콩알몬",
 "베이더몬",
 "스컬맘몬",
 "크레스가루몬",
 "이바몬",
 "포요몬",
 "토코몬",
 "파닥몬",
 "쿠네몬",
 "유니몬",
 "켄터스몬",
 "우가몬",
 "고스몬",
 "쉘몬",
 "두리몬",
 "스카몬",
 "안드로몬",
 "째리몬",
 "에테몬",
 "키메라몬",
 "하이안드로몬",
 "고쿠몬",
 "반쵸레오몬",
 "유라몬",
 "타네몬",
 "피요몬",
 "팔몬",
 "모노크로몬",
 "꼬끼몬",
 "레오몬",
 "쿠가몬",
 "실리컨몬",
 "모털몬",
 "모야몬",
 "메가드라몬",
 "픽콜몬",
 "디지타마몬",
 "다크드라몬",
 "블룸로드몬",
 "간쿠몬",
 "즈루몬",
 "파구몬",
 "가지몬",
 "기자몬",
 "다크티라노몬",
 "사이크로몬",
 "데블드라몬",
 "태스크몬",
 "플라이몬",
 "델타몬",
 "레어몬",
 "메탈티라노몬",
 "데이터몬",
 "엑스티라노몬",
 "파워드라몬",
 "라이덴몬",
 "가이오몬",
 "오메가몬 alter-S",
 "카오스몬",
 "밀레니엄몬",
 "카오스드라몬",
 "뽀글몬",
 "모치몬",
 "앙고라몬",
 "텐타몬",
 "곳츠몬",
 "올챙몬",
 "심바레앙고라몬",
 "캅테리몬",
 "토터몬",
 "가트몬",
 "모노크로몬",
 "스타몬",
 "개굴몬",
 "쿠가몬",
 "라모르몬",
 "아트라캅테리몬(청)",
 "쟈가몬",
 "엔젤우몬",
 "트리케라몬",
 "픽콜몬",
 "왕개굴몬",
 "왕쿠가몬",
 "딜비트몬",
 "헤라클레스캅테리몬",
 "블래스트몬",
 "홀리드라몬",
 "샤벨레오몬",
 "엘도라디몬",
 "메탈에테몬",
 "그랑쿠가몬",
 "마스테몬",
 "틀랄록몬",
 "피치몬",
 "푸카몬",
 "쉬라몬",
 "젤리몬",
 "가니몬",
 "샤코몬",
 "루카몬",
 "원뿔몬",
 "테슬라젤리몬",
 "시드라몬",
 "실리컨몬",
 "에비드라몬",
 "옥토몬",
 "게소몬",
 "고래몬",
 "쥬드몬",
 "테티스몬",
 "메가시드라몬",
 "아노말로카리몬",
 "다이버몬",
 "드라고몬",
 "마린데블몬",
 "마린엔젤몬",
 "암피몬",
 "플레시오몬",
 "점보가메몬",
 "메탈시드라몬",
 "크틸라몬",
 "푸쿠몬",
 "바이킹몬",
 "이지스드라몬",
 "미타마몬",
 "모쿠몬",
 "푸치메라몬",
 "바쿠몬",
 "캔들몬",
 "루가몬",
 "피코데블몬",
 "하누몬",
 "가루몬",
 "메라몬",
 "위자몬",
 "데블몬",
 "고스몬",
 "도쿠구몬",
 "루가루몬",
 "맘몬",
 "워가루몬",
 "데스메라몬",
 "펌프몬",
 "솔루가루몬",
 "묘티스몬",
 "팬텀몬",
 "레이디데블몬",
 "스컬맘몬",
 "아누비스몬",
 "볼트몬",
 "노블펌프몬",
 "펜리루가몬",
 "콜리스몬",
 "피에몬",
 "마왕몬",
 "마스테몬",
 "볼토바우타몬",
 "뇨키몬",
 "어니몬",
 "피요몬",
 "프테로몬",
 "팔몬",
 "플로라몬",
 "머쉬몬",
 "브이드라몬",
 "버드라몬",
 "게일몬",
 "니드몬",
 "키위몬",
 "레드베지몬",
 "우드몬",
 "에어로브이드라몬",
 "가루다몬",
 "그랜드게일몬",
 "릴리몬",
 "블로섬몬",
 "데라몬",
 "쥬레이몬",
 "가비지몬",
 "알포스브이드라몬",
 "호우오우몬",
 "제퍼가몬",
 "그리포몬",
 "로제몬",
 "라플레시몬",
 "히드라몬",
 "피노키몬",
 "미타마몬",
 "케르누몬",
 "쵸로몬",
 "카프리몬",
 "토이아구몬",
 "코쿠와몬",
 "톱니몬",
 "코만드라몬",
 "그레이몬",
 "리볼몬",
 "클락몬",
 "썬더볼몬",
 "탱크몬",
 "가드로몬",
 "메카노몬",
 "하이코만드라몬",
 "메탈그레이몬",
 "안드로몬",
 "사이버드라몬",
 "빅콩알몬",
 "나이트몬",
 "메가드라몬",
 "배드퍼펫몬",
 "카고드라몬",
 "워그레이몬",
 "하이안드로몬",
 "메탈가루몬",
 "브리가드라몬",
 "지크그레이몬",
 "파워드라몬",
 "베놈묘티스몬",
 "라그나몬",
 "오메가몬",
 "카오스드라몬",
 "유키미보타몬",
 "냐로몬",
 "아구몬",
 "플롯트몬",
 "파피몬",
 "감마몬",
 "그레이몬",
 "레오몬",
 "가트몬",
 "가루몬",
 "엔젤몬",
 "베텔감마몬",
 "이가몬",
 "카우스감마몬",
 "웨즌감마몬",
 "굴루스감마몬",
 "메탈그레이몬",
 "아수라몬",
 "워가루몬",
 "홀리엔젤몬",
 "엔젤우몬",
 "카노바이스몬",
 "메탈콩알몬",
 "레굴루스몬",
 "워그레이몬",
 "시리우스몬",
 "도미니몬",
 "메탈가루몬",
 "퀀텀몬",
 "아크투루스몬",
 "오메가몬",
 "마스테몬",
 "프로시마몬",
 "길몬",
 "그라우몬",
 "메가로그라우몬",
 "듀크몬",
 "듀크몬 크림슨 모드",
 "케라몬",
 "크리사리몬",
 "인페르몬",
 "디아블로몬",
 "루나몬",
 "레키스몬",
 "크레스몬",
 "디아나몬",
 "가오몬",
 "가오가몬",
 "마하가오가몬",
 "미라쥬가오가몬",
 "레나몬",
 "구미호몬",
 "도사몬",
 "샤크라몬",
 "헉몬",
 "바오헉몬",
 "세이버헉몬",
 "제스몬",
 "돌몬",
 "도루가몬",
 "도루그레몬",
 "도루고라몬",
 "라프타드라몬",
 "그레이드몬",
 "알파몬",
 "류우다몬",
 "긴류우몬",
 "히샤류우몬",
 "오류우몬",
 "알파몬 왕룡검",
 "도도몬",
 "도리몬",
 "기기몬",
 "쿠라몬",
 "츠메몬",
 "피치몬",
 "문몬",
 "뽀글몬",
 "모치몬",
 "모쿠몬",
 "포코몬",
 "보타몬",
 "코로몬",
 "드라코몬",
 "코어드라몬(청)",
 "코어드라몬(녹)",
 "지오그레이몬",
 "윙드라몬",
 "그라운드라몬",
 "라이즈그레이몬",
 "슬레이어드라몬",
 "브레이크드라몬",
 "엑자몬",
 "드라크몬",
 "고스트몬",
 "츠카이몬",
 "소울몬",
 "아이스데블몬",
 "상글루몬",
 "팡몬",
 "위치몬",
 "부기몬",
 "마타돌몬",
 "아스타몬",
 "네오데블몬",
 "스컬발루치몬",
 "와이즈몬",
 "케르베로스몬",
 "그란드라크몬",
 "발바몬",
 "리리스몬",
 "베르스타몬",
 "무르무쿠스몬",
 "스윔몬",
 "카메몬",
 "산고몬",
 "펜몬",
 "돌프몬",
 "티로몬",
 "토비우몬",
 "오르카몬",
 "마린키메라몬",
 "구소쿠몬",
 "와루시드라몬",
 "다이브몬",
 "리갈렉스몬",
 "넵튠몬",
 "리바이어몬",
 "에이션트머메이몬",
 "포무몬",
 "펀비몬",
 "라라몬",
 "파라사우몬",
 "선플라우몬",
 "와스프몬",
 "아자타몬",
 "캐논비몬",
 "라일라몬",
 "그랜디스쿠가몬",
 "타이거베스파몬",
 "로터스몬",
 "반쵸릴리몬",
 "임프몬",
 "가지몬",
 "고블리몬",
 "파스코몬",
 "소서리몬",
 "블랙테일몬",
 "무샤몬",
 "푸가몬",
 "바알몬",
 "바스테몬",
 "아라크네몬",
 "스컬사탄몬",
 "베르제브몬",
 "걸프몬",
 "플루토몬",
 "쿠즈하몬",
 "쿠다몬",
 "루체몬",
 "파닥몬",
 "모르포몬",
 "그라디몬",
 "레파몬",
 "피드몬",
 "다르크몬",
 "치린몬",
 "히포그리포몬",
 "미스티몬",
 "세라피몬",
 "오파니몬",
 "두프트몬",
 "크레니엄몬",
 "슬레이프몬",
 "아마게몬",
 "그레이스노바몬",
 "코로나몬",
 "파이라몬",
 "플레어몬",
 "아폴로몬",
 "미라쥬가오가몬 버스트 모드",
 "베르제브몬 블래스트 모드",
 "제스몬 GX",
 "루체몬 폴다운 모드",
 "루체몬 사탄 모드",
 "치코몬",
 "꼬마몬",
 "브이몬",
 "추추몬",
 "호크몬",
 "아르마몬",
 "엑스브이몬",
 "스나이몬",
 "아큐라몬",
 "황금아르마몬",
 "주엘비몬",
 "야타가라몬",
 "메테오몬",
 "파일드라몬",
 "다이노몬",
 "실피드몬",
 "토우몬",
 "발키리몬",
 "레이브몬",
 "황제드라몬 드래곤 모드",
 "황제드라몬 파이터 모드",
 "황제드라몬 팔라딘 모드",
 "황제드라몬 오메가X",
};
static_assert(sizeof(DIGI_NAMES_KO)/sizeof(DIGI_NAMES_KO[0]) == sizeof(DIGI_SPECIES)/sizeof(DIGI_SPECIES[0]),
              "Korean Digimon name table must match species catalog");
const char *digimonNameKo(uint16_t index){return index<DIGI_SPECIES_COUNT?DIGI_NAMES_KO[index]:"?";}

// Compact Korean display names for TamaPoke's small round screen.
// DIGI_NAMES_KO above remains the full Korean name table; this function only
// abbreviates forms whose full names would otherwise be hard to read at a
// useful font size. Internal species keys/IDs are never changed.
const char *digimonNameKoShort(uint16_t index){
 if(index>=DIGI_SPECIES_COUNT)return "?";
 const char*n=DIGI_SPECIES[index].name;
 if(!strcmp(n,"Omegamon Alter-S"))return "오메가몬S";
 if(!strcmp(n,"Dukemon Crimson Mode"))return "듀크몬 CM";
 if(!strcmp(n,"MirageGaogamon Burst Mode"))return "미라쥬가오가몬 BM";
 if(!strcmp(n,"Beelzebumon Blast Mode"))return "베르제브몬 BM";
 if(!strcmp(n,"Lucemon Falldown Mode"))return "루체몬 FD";
 if(!strcmp(n,"Lucemon Satan Mode"))return "루체몬 SM";
 if(!strcmp(n,"Imperialdramon Dragon Mode"))return "황제드라몬 DM";
 if(!strcmp(n,"Imperialdramon Fighter Mode"))return "황제드라몬 FM";
 if(!strcmp(n,"Imperialdramon Paladin Mode"))return "황제드라몬 PM";
 if(!strcmp(n,"Imperialdramon OmegaX"))return "황제드라몬 OX";
 if(!strcmp(n,"Coredramon Blue"))return "코어드라몬 청";
 if(!strcmp(n,"Coredramon Green"))return "코어드라몬 녹";
 if(!strcmp(n,"AtlurKabuterimonBlue"))return "아트라캅테리몬 청";
 if(!strcmp(n,"WhamonPerfect"))return "고래몬(완)";
 if(!strcmp(n,"MetalGreymon_Virus")||!strcmp(n,"MetalGreymon Virus"))return "메탈그레이몬V";
 return DIGI_NAMES_KO[index];
}

static uint16_t firstOf(uint8_t ver, uint8_t stage) {
  for (uint16_t i=0;i<DIGI_SPECIES_COUNT;i++) if(DIGI_SPECIES[i].version==ver&&DIGI_SPECIES[i].stage==stage) return i;
  return 0;
}
static uint16_t countOf(uint8_t ver, uint8_t stage) {
  uint16_t n=0; for(uint16_t i=0;i<DIGI_SPECIES_COUNT;i++) n += DIGI_SPECIES[i].version==ver&&DIGI_SPECIES[i].stage==stage; return n;
}
static uint16_t firstStarterOf(uint8_t ver) {
  uint16_t id=firstOf(ver,DIGI_BABY1);
  if(ver==16 || DIGI_SPECIES[id].version!=ver) id=firstOf(ver,DIGI_CHILD);
  return id;
}
static uint16_t randomStarterOf(uint8_t ver) {
  if(ver!=16) return firstStarterOf(ver);
  uint16_t n=countOf(ver,DIGI_CHILD); if(!n) return 0;
  uint16_t pick=(uint16_t)random(n);
  for(uint16_t i=0;i<DIGI_SPECIES_COUNT;i++) if(DIGI_SPECIES[i].version==ver&&DIGI_SPECIES[i].stage==DIGI_CHILD && pick--==0) return i;
  return firstStarterOf(ver);
}

void DigiPet::begin(){ prefs.begin("digipet",false); enabled=prefs.getBool("on",false);egg=prefs.getBool("egg",false);shiny=prefs.getBool("shy",false);eggShiny=prefs.getBool("eshy",false);eggTaps=prefs.getUChar("etap",0);version=prefs.getUChar("ver",1);if(!isDigimonDeviceVersion(version))version=1;speciesId=prefs.getUShort("id",firstStarterOf(version));if(speciesId>=DIGI_SPECIES_COUNT)speciesId=firstStarterOf(version);prefs.getBytes("iv",iv,sizeof(iv));prefs.getBytes("tr",training,sizeof(training));size_t rl=prefs.getBytesLength("reg");if(rl) prefs.getBytes("reg",registered,min(rl,sizeof(registered)));size_t sl=prefs.getBytesLength("sreg");if(sl)prefs.getBytes("sreg",shinyRegistered,min(sl,sizeof(shinyRegistered)));size_t bl=prefs.getBytesLength("best");if(bl)prefs.getBytes("best",bestLevel,min(bl,sizeof(bestLevel)));if(prefs.getBytesLength("moves")==sizeof(moves))prefs.getBytes("moves",moves,sizeof(moves));else relearnMoves();levelMinutes=prefs.getUInt("mins",0);lastTick=millis();recordCurrentLevel();}
void DigiPet::recordCurrentLevel(){if(enabled&&!egg&&speciesId<DIGI_SPECIES_COUNT){uint8_t lv=level();if(lv>bestLevel[speciesId])bestLevel[speciesId]=lv;}}
void DigiPet::save(){
 recordCurrentLevel();
 prefs.putBool("on",enabled);prefs.putBool("egg",egg);prefs.putBool("shy",shiny);prefs.putBool("eshy",eggShiny);prefs.putUChar("etap",eggTaps);
 prefs.putUChar("ver",version);prefs.putUShort("id",speciesId);
 prefs.putBytes("iv",iv,sizeof(iv));prefs.putBytes("tr",training,sizeof(training));
 // Keep the large 2048-species reserve out of NVS until species actually exist.
 // Old shorter blobs load at the front of these zero-initialised arrays.
 prefs.putBytes("reg",registered,(DIGI_SPECIES_COUNT+7u)/8u);
 prefs.putBytes("sreg",shinyRegistered,(DIGI_SPECIES_COUNT+7u)/8u);
 prefs.putBytes("best",bestLevel,DIGI_SPECIES_COUNT);
 prefs.putBytes("moves",moves,sizeof(moves));prefs.putUInt("mins",levelMinutes);
}
void DigiPet::start(uint8_t v){ if(!isDigimonDeviceVersion(v))v=1;version=v;speciesId=randomStarterOf(version);levelMinutes=0;egg=false;eggTaps=0;shiny=random(32)==0;eggShiny=shiny;for(int i=0;i<4;i++){iv[i]=random(32);training[i]=0;}enabled=true;registered[speciesId>>3]|=1<<(speciesId&7);if(shiny)shinyRegistered[speciesId>>3]|=1<<(speciesId&7);relearnMoves();save(); }
void DigiPet::startEgg(uint8_t v){if(!isDigimonDeviceVersion(v))v=1;version=v;speciesId=randomStarterOf(version);enabled=true;egg=true;shiny=false;eggShiny=random(32)==0;eggTaps=0;levelMinutes=0;for(int i=0;i<4;i++)training[i]=0;save();}
bool DigiPet::tapEgg(){if(!enabled||!egg)return false;if(++eggTaps<3){save();return false;}egg=false;eggTaps=0;shiny=eggShiny;levelMinutes=0;for(int i=0;i<4;i++){iv[i]=random(32);training[i]=0;}relearnMoves();registered[speciesId>>3]|=1<<(speciesId&7);if(shiny)shinyRegistered[speciesId>>3]|=1<<(speciesId&7);save();return true;}
void DigiPet::update(uint32_t now){if(!lastTick)lastTick=now;if(egg)return;uint32_t dm=now-lastTick;if(dm>=60000){levelMinutes+=dm/60000;lastTick+=dm/60000*60000;save();}}
uint8_t DigiPet::level()const{uint32_t n=1+levelMinutes/30;return n>100?100:n;}
const DigiSpecies&DigiPet::species()const{return DIGI_SPECIES[speciesId<DIGI_SPECIES_COUNT?speciesId:0];}
void DigiPet::train(DigiTrain k,uint8_t amount){if(k>3)return;uint16_t n=training[k]+amount;training[k]=n>999?999:n;save();}
uint16_t DigiPet::stat(DigiTrain k)const{const DigiSpecies&s=species();uint16_t base=12+s.stage*12+s.power/4;uint16_t bias=(s.style==k)?(8+s.stage*4):0;return base+bias+iv[k]*level()/100+training[k]/2+level();}
uint8_t DigiPet::type1()const{
 const uint16_t i=speciesId<DIGI_SPECIES_COUNT?speciesId:0;
 return DIGI_TYPE_PROFILE[i].type1;
}
uint8_t DigiPet::type2()const{
 const uint16_t i=speciesId<DIGI_SPECIES_COUNT?speciesId:0;
 return DIGI_TYPE_PROFILE[i].type2;
}
static void typeMoves(uint8_t t,uint8_t*out){
 switch(t){
  case T_FIRE: out[0]=MV_EMBER;out[1]=MV_FIRE_PUNCH;out[2]=MV_FLAMETHROWER;out[3]=MV_FIRE_BLAST;break;
  case T_WATER: out[0]=MV_BUBBLE;out[1]=MV_WATER_GUN;out[2]=MV_SURF;out[3]=MV_HYDRO_PUMP;break;
  case T_ELECTRIC: out[0]=MV_SPARK;out[1]=MV_THUNDERSHOCK;out[2]=MV_THUNDERBOLT;out[3]=MV_THUNDER;break;
  case T_GRASS: out[0]=MV_ABSORB;out[1]=MV_VINE_WHIP;out[2]=MV_MEGA_DRAIN;out[3]=MV_SOLAR_BEAM;break;
  case T_ICE: out[0]=MV_AURORA_BEAM;out[1]=MV_ICE_PUNCH;out[2]=MV_ICE_BEAM;out[3]=MV_BLIZZARD;break;
  case T_FIGHTING: out[0]=MV_KARATE_CHOP;out[1]=MV_ROCK_SMASH;out[2]=MV_BULK_UP;out[3]=MV_HI_JUMP_KICK;break;
  case T_BUG: out[0]=MV_BUG_BITE;out[1]=MV_PIN_MISSILE;out[2]=MV_X_SCISSOR;out[3]=MV_MEGAHORN;break;
  case T_FLYING: out[0]=MV_PECK;out[1]=MV_WING_ATTACK;out[2]=MV_DRILL_PECK;out[3]=MV_AEROBLAST;break;
  case T_PSYCHIC: out[0]=MV_CONFUSION;out[1]=MV_PSYBEAM;out[2]=MV_PSYCHIC;out[3]=MV_PSYSTRIKE;break;
  case T_DRAGON: out[0]=MV_DRAGON_RAGE;out[1]=MV_DRAGON_CLAW;out[2]=MV_OUTRAGE;out[3]=MV_DRAGON_ENERGY;break;
  case T_DARK: out[0]=MV_BITE;out[1]=MV_CRUNCH;out[2]=MV_DARK_PULSE;out[3]=MV_KOWTOW_CLEAVE;break;
  case T_STEEL: out[0]=MV_TACKLE;out[1]=MV_IRON_HEAD;out[2]=MV_FLASH_CANNON;out[3]=MV_SUNSTEEL_STRIKE;break;
  case T_FAIRY: out[0]=MV_POUND;out[1]=MV_DAZZLE_GLEAM;out[2]=MV_PLAY_ROUGH;out[3]=MV_MOONBLAST;break;
  default: out[0]=MV_TACKLE;out[1]=MV_QUICK_ATTACK;out[2]=MV_BODY_SLAM;out[3]=MV_HYPER_BEAM;break;
 }
}
uint8_t DigiPet::signatureMove()const{return (uint8_t)(MV_DIGI_PULSE+(type1()<TYPE_COUNT?type1():T_NORMAL));}
void DigiPet::relearnMoves(){uint8_t pool[4];typeMoves(type1(),pool);uint8_t unlocked=1+species().stage/2;if(unlocked>3)unlocked=3;for(uint8_t i=0;i<3;i++)moves[i]=i<unlocked?pool[i]:MV_NONE;if(type2()!=T_NONE&&unlocked>1){uint8_t alt[4];typeMoves(type2(),alt);moves[unlocked-1]=alt[unlocked-1];}moves[3]=signatureMove();}
static uint16_t pendulumFusionTarget(uint16_t i,uint8_t lv,const uint8_t*best,const uint8_t*wildMat=nullptr);
uint16_t DigiPet::fusionTarget()const{
 if(egg)return DIGI_NO_FUSION;
 return digimonJogressTarget(speciesId,level(),training[DIGI_ATK],training[DIGI_DEF],training[DIGI_SPE],training[DIGI_HP],bestLevel);
}
bool DigiPet::canJogress()const{return fusionTarget()!=DIGI_NO_FUSION;}
bool DigiPet::jogress(){if(!canJogress())return false;recordCurrentLevel();uint16_t next=fusionTarget();if(next==DIGI_NO_FUSION||next==speciesId)return false;speciesId=next;for(int i=0;i<4;i++)training[i]=0;relearnMoves();registered[speciesId>>3]|=1<<(speciesId&7);if(shiny)shinyRegistered[speciesId>>3]|=1<<(speciesId&7);save();return true;}
bool DigiPet::canEvolve()const{if(egg)return false;uint8_t s=species().stage;static const uint8_t need[]={2,5,12,25,45,60};static const uint16_t tr[]={0,0,4,8,12,0};uint32_t sum=training[0]+training[1]+training[2]+training[3];if(level()<need[s]||sum<tr[s])return false;return chooseEvolution()!=speciesId;}
uint16_t DigiPet::chooseEvolution()const{return digimonEvolutionTarget(speciesId,level(),training[0],training[1],training[2],training[3],bestLevel);}
bool DigiPet::evolve(){if(!canEvolve())return false;recordCurrentLevel();uint16_t next=chooseEvolution();if(next==speciesId)return false;speciesId=next;for(int i=0;i<4;i++)training[i]=0;relearnMoves();registered[speciesId>>3]|=1<<(speciesId&7);if(shiny)shinyRegistered[speciesId>>3]|=1<<(speciesId&7);save();return true;}
uint16_t DigiPet::registeredCount()const{uint16_t n=0;for(uint16_t i=0;i<DIGI_SPECIES_COUNT;i++)if(isRegistered(i))n++;return n;}
uint16_t DigiPet::displayIndex()const{uint16_t n=0;for(uint16_t i=0;i<speciesId;i++)if(DIGI_SPECIES[i].version==version)n++;return n;}

const char *creatureName(int16_t id) {
  if (isDigimonId(id)) return digimonNameKoShort(digimonIndex(id));
  return (id >= 1 && id <= DEX_COUNT) ? localizedSpeciesName(id) : "?";
}

static uint8_t digiPrimary(uint16_t i) {
  return i<DIGI_SPECIES_COUNT ? DIGI_TYPE_PROFILE[i].type1 : T_NORMAL;
}
uint8_t creatureType1(int16_t id) { return isDigimonId(id) ? digiPrimary(digimonIndex(id)) : DEX_TBL[id].type1; }
uint8_t creatureType2(int16_t id) {
  if (!isDigimonId(id)) return DEX_TBL[id].type2;
  const uint16_t i=digimonIndex(id);
  return i<DIGI_SPECIES_COUNT ? DIGI_TYPE_PROFILE[i].type2 : T_NONE;
}
static uint8_t digiBase(uint16_t i,uint8_t stat) {
  const DigiSpecies&s=DIGI_SPECIES[i];
  uint16_t v=26+s.stage*18+s.power/7;
  if(s.style==stat)v+=14+s.stage*3;
  if(stat==DIGI_HP)v+=8;
  return v>190?190:(uint8_t)v;
}
uint8_t creatureBaseAtk(int16_t id){return isDigimonId(id)?digiBase(digimonIndex(id),DIGI_ATK):DEX_TBL[id].bAtk;}
uint8_t creatureBaseDef(int16_t id){return isDigimonId(id)?digiBase(digimonIndex(id),DIGI_DEF):DEX_TBL[id].bDef;}
uint8_t creatureBaseSpe(int16_t id){return isDigimonId(id)?digiBase(digimonIndex(id),DIGI_SPE):DEX_TBL[id].bSpe;}
uint8_t creatureBaseHp(int16_t id){return isDigimonId(id)?digiBase(digimonIndex(id),DIGI_HP):DEX_TBL[id].bHp;}
uint8_t creatureBaseSpA(int16_t id){return isDigimonId(id)?digiBase(digimonIndex(id),DIGI_ATK):DEX_TBL[id].bSpA;}
uint8_t creatureBaseSpD(int16_t id){return isDigimonId(id)?digiBase(digimonIndex(id),DIGI_DEF):DEX_TBL[id].bSpD;}
uint16_t creatureAccent(int16_t id){return isDigimonId(id)?(uint16_t)(0x3DFF+(digimonIndex(id)%5)*0x1800):DEX_TBL[id].accent;}
uint8_t digimonSignatureMove(uint16_t i){return (uint8_t)(MV_DIGI_PULSE+(digiPrimary(i)<TYPE_COUNT?digiPrimary(i):T_NORMAL));}

static uint8_t digiCoverageType(uint16_t i,uint8_t t1,uint8_t t2){
 // A small role-themed coverage pool expands move variety without handing
 // every Digimon every move. ATK/DEF/SPE/HP styles lean toward different tools.
 static const uint8_t role[4][4]={
  {T_FIGHTING,T_GROUND,T_FIRE,T_DRAGON},{T_ROCK,T_STEEL,T_WATER,T_ICE},
  {T_FLYING,T_ELECTRIC,T_BUG,T_POISON},{T_PSYCHIC,T_FAIRY,T_GHOST,T_GRASS}};
 const DigiSpecies&s=DIGI_SPECIES[i];uint8_t start=(uint8_t)((i+s.version+s.stage)&3);
 for(uint8_t k=0;k<4;k++){uint8_t t=role[s.style&3][(start+k)&3];if(t!=t1&&t!=t2)return t;}
 return T_NORMAL;
}

// Digimon borrow the existing Pokemon move dataset instead of receiving three
// copies of their digital move. The pool is type-compatible and grows stronger
// with level/stage; the default three are shuffled deterministically from the
// species and IVs, so saves remain stable while individuals can differ.
uint8_t digimonLearnableMoves(uint16_t i,uint8_t lv,uint8_t*out,uint8_t max){
 if(i>=DIGI_SPECIES_COUNT||!out||!max)return 0;
 uint8_t w=0,t1=digiPrimary(i);uint8_t t2=DIGI_TYPE_PROFILE[i].type2,t3=digiCoverageType(i,t1,t2);
 out[w++]=digimonSignatureMove(i);
 uint16_t cap=45u+DIGI_SPECIES[i].stage*18u+lv/3u;if(cap>150)cap=150;
 for(uint16_t mv=1;mv<MV_DIGI_PULSE&&w<max;mv++){
  const MoveEntry&m=MOVE_TBL[mv];
  if(mv==MV_STRUGGLE)continue;
  if(m.type!=t1&&m.type!=t2&&m.type!=t3&&m.type!=T_NORMAL)continue;
  if(m.cat!=MC_STATUS&&m.power&&m.power>cap)continue;
  if(lv<20&&(m.effect==EF_RECHARGE||m.effect==EF_CHARGE))continue;
  out[w++]=(uint8_t)mv;
 }
 return w;
}
static uint32_t digiMoveRand(uint32_t&s){s=s*1664525UL+1013904223UL;return s;}
void digimonDefaultMoves(uint16_t i,uint8_t lv,uint8_t ia,uint8_t id,uint8_t is,uint8_t ih,uint8_t out[4]){
 for(uint8_t k=0;k<4;k++)out[k]=0;if(i>=DIGI_SPECIES_COUNT)return;
 uint8_t pool[MV_DIGI_PULSE];uint8_t n=digimonLearnableMoves(i,lv,pool,sizeof(pool));
 uint32_t seed=0xD161B00BUL^(uint32_t)(i+1)*2654435761UL^((uint32_t)ia<<24)^((uint32_t)id<<16)^((uint32_t)is<<8)^ih;
 // Slot 0 always starts with a damaging primary-type Pokemon move when one is
 // available, then slots 1-2 are deterministic random compatible moves.
 uint8_t primary[MV_DIGI_PULSE],pn=0,t1=digiPrimary(i);
 for(uint8_t k=1;k<n;k++)if(MOVE_TBL[pool[k]].type==t1&&MOVE_TBL[pool[k]].cat!=MC_STATUS)primary[pn++]=pool[k];
 if(pn)out[0]=primary[digiMoveRand(seed)%pn];
 for(uint8_t k=n;k>2;k--){uint8_t j=1+(digiMoveRand(seed)%(k-1));uint8_t q=pool[k-1];pool[k-1]=pool[j];pool[j]=q;}
 uint8_t w=out[0]?1:0;
 for(uint8_t k=1;k<n&&w<3;k++){
  uint8_t mv=pool[k];bool dup=false;for(uint8_t x=0;x<w;x++)if(out[x]==mv)dup=true;
  if(!dup)out[w++]=mv;
 }
 static const uint8_t fallback[]={MV_TACKLE,MV_SCRATCH,MV_POUND,MV_QUICK_ATTACK};
 for(uint8_t k=0;k<sizeof(fallback)&&w<3;k++){bool dup=false;for(uint8_t x=0;x<w;x++)if(out[x]==fallback[k])dup=true;if(!dup)out[w++]=fallback[k];}
 out[3]=digimonSignatureMove(i);
}
bool digimonMovesNeedRefresh(const uint8_t m[4]){
 uint8_t count=0,digital=0;
 for(uint8_t i=0;i<4;i++)if(m[i]){count++;if(m[i]>=MV_DIGI_PULSE)digital++;for(uint8_t j=0;j<i;j++)if(m[i]==m[j])return true;}
 return count<4||digital>1;
}
static uint16_t digiFind(uint8_t ver,const char*name){
 for(uint16_t i=0;i<DIGI_SPECIES_COUNT;i++)if(DIGI_SPECIES[i].version==ver&&!strcmp(DIGI_SPECIES[i].name,name))return i;
 return DIGI_NO_FUSION;
}
bool isPendulumFusionSpecies(uint16_t i){
 if(i>=DIGI_SPECIES_COUNT||DIGI_SPECIES[i].version<10)return false;
 const char*n=DIGI_SPECIES[i].name;
 return !strcmp(n,"Mastemon")||!strcmp(n,"Tlalocmon")||!strcmp(n,"Aegisdramon")||
        !strcmp(n,"Mitamamon")||!strcmp(n,"Voltobautamon")||!strcmp(n,"Cernumon")||
        !strcmp(n,"Omegamon")||!strcmp(n,"Chaosdramon")||!strcmp(n,"Proximamon")||!strcmp(n,"Alphamon Ouryuken");
}
const char *digimonDeviceLabel(uint8_t v){
 static const char*const labels[]={"P0 Virus Busters","P1 Nature Spirits","P2 Deep Savers",
   "P3 Nightmare Soldiers","P4 Wind Guardians","P5 Metal Empire"};
 if(v>=1&&v<=5){static const char*const dmc[]={"DMC Ver.1","DMC Ver.2","DMC Ver.3","DMC Ver.4","DMC Ver.5"};return dmc[v-1];}
 if(v>=10&&v<=15)return labels[v-10];
 if(v==16)return "DMUL Dragon";
 if(v==17)return "DMUL Dark";
 if(v==18)return "DMUL Deep";
 if(v==19)return "DMUL Nature";
 if(v==20)return "DMUL Nightmare";
 if(v==21)return "DMUL Secret";
 if(v==22)return "DMUL Imperial";
 return "융합";
}
static bool digiWildMaterial(uint16_t material,const uint8_t*wildMat){
 return wildMat && material<DIGI_SPECIES_COUNT && (wildMat[material>>3]&(1<<(material&7)));
}
static bool digiQualified(uint16_t material,uint16_t current,uint8_t lv,const uint8_t*best,const uint8_t*wildMat,uint8_t need=55){
 return material!=DIGI_NO_FUSION&&((material==current&&lv>=need)||(best&&best[material]>=need)||digiWildMaterial(material,wildMat));
}
static uint16_t pendulumFusionTarget(uint16_t i,uint8_t lv,const uint8_t*best,const uint8_t*wildMat){
 if(i>=DIGI_SPECIES_COUNT)return DIGI_NO_FUSION;
 const uint8_t v=DIGI_SPECIES[i].version; const char*n=DIGI_SPECIES[i].name;
 auto q=[&](uint8_t ver,const char*name){return digiQualified(digiFind(ver,name),i,lv,best,wildMat);};
 auto target=[&](const char*name){return digiFind(v,name);};
 if(v==16){
  if((!strcmp(n,"Alphamon")&&q(16,"Ouryumon"))||(!strcmp(n,"Ouryumon")&&q(16,"Alphamon")))return target("Alphamon Ouryuken");
  return DIGI_NO_FUSION;
 }
 if(v==11){
  if((!strcmp(n,"Angewomon")&&q(13,"LadyDevimon"))||(!strcmp(n,"LadyDevimon")&&q(11,"Angewomon")))return target("Mastemon");
  if((!strcmp(n,"SaberLeomon")&&(q(11,"ElDoradimon")||q(11,"MetalEtemon")))||
     ((!strcmp(n,"ElDoradimon")||!strcmp(n,"MetalEtemon"))&&q(11,"SaberLeomon")))return target("Tlalocmon");
 }else if(v==12){
  if((!strcmp(n,"Plesiomon")&&q(12,"MetalSeadramon"))||(!strcmp(n,"MetalSeadramon")&&q(12,"Plesiomon")))return target("Aegisdramon");
  if((!strcmp(n,"MarinAngemon")&&q(14,"Hououmon"))||(!strcmp(n,"Hououmon")&&q(12,"MarinAngemon")))return target("Mitamamon");
 }else if(v==13){
  if(!strcmp(n,"LadyDevimon")&&(q(11,"Angewomon")||q(10,"Angewomon")))return target("Mastemon");
  if((!strcmp(n,"Vamdemon")&&q(13,"Piemon"))||(!strcmp(n,"Piemon")&&q(13,"Vamdemon")))return target("Voltobautamon");
 }else if(v==14){
  if((!strcmp(n,"Hououmon")&&q(12,"MarinAngemon"))||(!strcmp(n,"MarinAngemon")&&q(14,"Hououmon")))return target("Mitamamon");
  if((!strcmp(n,"Griffomon")&&(q(14,"Pinochimon")||q(14,"Hydramon")))||
     (!strcmp(n,"Pinochimon")&&(q(14,"Griffomon")||q(14,"Hydramon")))||
     (!strcmp(n,"Hydramon")&&(q(14,"Pinochimon")||q(14,"Griffomon"))))return target("Cernumon");
 }else if(v==15){
  if((!strcmp(n,"WarGreymon")&&(q(15,"MetalGarurumon")||q(10,"MetalGarurumon")))||
     (!strcmp(n,"MetalGarurumon")&&(q(15,"WarGreymon")||q(10,"WarGreymon"))))return target("Omegamon");
  if((!strcmp(n,"Mugendramon")&&q(15,"HiAndromon"))||(!strcmp(n,"HiAndromon")&&q(15,"Mugendramon")))return target("Chaosdramon");
 }else if(v==10){
  if((!strcmp(n,"WarGreymon")&&(q(10,"MetalGarurumon")||q(15,"MetalGarurumon")))||
     (!strcmp(n,"MetalGarurumon")&&(q(10,"WarGreymon")||q(15,"WarGreymon"))))return target("Omegamon");
  if(!strcmp(n,"Angewomon")&&q(13,"LadyDevimon"))return target("Mastemon");
  if((!strcmp(n,"Siriusmon")&&q(10,"Arcturusmon"))||(!strcmp(n,"Arcturusmon")&&q(10,"Siriusmon")))return target("Proximamon");
 }
 return DIGI_NO_FUSION;
}
uint8_t digimonEvolutionLevel(uint16_t i){
  if(i>=DIGI_SPECIES_COUNT)return 100;
  const char*n=DIGI_SPECIES[i].name;
  if(i==83)return 60;
  if(i==14||i==32||i==51||i==66||i==48)return 55;
  if(!strcmp(n,"Alphamon")||!strcmp(n,"Ouryumon")||!strcmp(n,"Slayerdramon")||!strcmp(n,"Breakdramon")||
     !strcmp(n,"Dianamon")||!strcmp(n,"Apollomon")||!strcmp(n,"Imperialdramon Dragon Mode"))return 55;
  if(!strcmp(n,"Dukemon")||!strcmp(n,"Diablomon")||!strcmp(n,"MirageGaogamon")||!strcmp(n,"Beelzebumon")||
     !strcmp(n,"Jesmon")||!strcmp(n,"Lucemon Falldown Mode")||!strcmp(n,"Imperialdramon Fighter Mode"))return 60;
  if(!strcmp(n,"Imperialdramon Paladin Mode"))return 70;
  if(!strcmp(n,"Lucemon"))return 45;
  if(!strcmp(n,"Paildramon")||!strcmp(n,"Dinobeemon"))return 45;
  static const uint8_t need[]={2,5,12,25,45,100};return need[DIGI_SPECIES[i].stage];
}
static bool dmulUltimateNormalSource(const char*n){
 // Ultimate-stage forms that still have a non-Jogress evolution.  Keep this
 // deliberately narrower than the old catch-all list: Alphamon/Ouryumon,
 // Slayerdramon/Breakdramon, Dianamon/Apollomon and Jesmon are Jogress-only
 // sources and must not be presented as an automatic Lv.100 evolution.
 return !strcmp(n,"Dukemon")||!strcmp(n,"Diablomon")||
        !strcmp(n,"MirageGaogamon")||!strcmp(n,"Beelzebumon")||
        !strcmp(n,"Lucemon Falldown Mode")||
        !strcmp(n,"Imperialdramon Dragon Mode")||!strcmp(n,"Imperialdramon Fighter Mode")||
        !strcmp(n,"Imperialdramon Paladin Mode");
}
static bool pendulumJogressSource(uint16_t i){
 if(i>=DIGI_SPECIES_COUNT)return false;
 const DigiSpecies&d=DIGI_SPECIES[i];const char*n=d.name;
 if(d.version==10)return !strcmp(n,"WarGreymon")||!strcmp(n,"MetalGarurumon")||
                         !strcmp(n,"Angewomon")||!strcmp(n,"Siriusmon")||!strcmp(n,"Arcturusmon");
 if(d.version==11)return !strcmp(n,"Angewomon")||!strcmp(n,"SaberLeomon")||
                         !strcmp(n,"ElDoradimon")||!strcmp(n,"MetalEtemon");
 if(d.version==12)return !strcmp(n,"Plesiomon")||!strcmp(n,"MetalSeadramon")||!strcmp(n,"MarinAngemon");
 if(d.version==13)return !strcmp(n,"LadyDevimon")||!strcmp(n,"Vamdemon")||!strcmp(n,"Piemon");
 if(d.version==14)return !strcmp(n,"Hououmon")||!strcmp(n,"Griffomon")||
                         !strcmp(n,"Pinochimon")||!strcmp(n,"Hydramon");
 if(d.version==15)return !strcmp(n,"WarGreymon")||!strcmp(n,"MetalGarurumon")||
                         !strcmp(n,"Mugendramon")||!strcmp(n,"HiAndromon");
 return false;
}
bool digimonHasNormalEvolutionPotential(uint16_t i){
 if(i>=DIGI_SPECIES_COUNT)return false;
 const DigiSpecies&d=DIGI_SPECIES[i];
 if(d.stage<DIGI_ULTIMATE)return true;
 if(i==83)return true; // Mugendramon -> Chaosdramon is a normal special evolution.
 return isDmulVersion(d.version)&&dmulUltimateNormalSource(d.name);
}
bool digimonHasJogressPotential(uint16_t i){
 if(i>=DIGI_SPECIES_COUNT)return false;
 if(i==14||i==32||i==48||i==51||i==66||i==83)return true;
 if(pendulumJogressSource(i))return true;
 const DigiSpecies&d=DIGI_SPECIES[i];const char*n=d.name;
 if(d.version==16&&(!strcmp(n,"Alphamon")||!strcmp(n,"Ouryumon")||
                    !strcmp(n,"Slayerdramon")||!strcmp(n,"Breakdramon")))return true;
 if(!strcmp(n,"Dianamon")||!strcmp(n,"Apollomon"))return true;
 if(d.version==21&&!strcmp(n,"Jesmon"))return true;
 if(d.version==22&&d.stage==DIGI_ADULT&&(!strcmp(n,"ExVeemon")||!strcmp(n,"Snimon")||
                                        !strcmp(n,"Aquilamon")||!strcmp(n,"Ankylomon")))return true;
 return false;
}
uint8_t digimonJogressLevel(uint16_t i){
 if(!digimonHasJogressPotential(i))return 0;
 if(i<DIGI_SPECIES_COUNT){
  const DigiSpecies&d=DIGI_SPECIES[i];
  if(d.version==22&&d.stage==DIGI_ADULT)return 25;
  if(d.version==21&&!strcmp(d.name,"Jesmon"))return 60;
 }
 return 55;
}
bool digimonHasEvolutionPotential(uint16_t i){
 return digimonHasNormalEvolutionPotential(i)||digimonHasJogressPotential(i);
}
static uint8_t digiStageRank(uint16_t i){
 if(i>=DIGI_SPECIES_COUNT)return 0;
 const DigiSpecies&cur=DIGI_SPECIES[i];uint8_t rank=0;
 for(uint16_t x=0;x<i;x++)if(DIGI_SPECIES[x].version==cur.version&&DIGI_SPECIES[x].stage==cur.stage)rank++;
 return rank;
}
static uint8_t digiStageCount(uint8_t version,uint8_t stage){
 uint8_t count=0;for(uint16_t x=0;x<DIGI_SPECIES_COUNT;x++)if(DIGI_SPECIES[x].version==version&&DIGI_SPECIES[x].stage==stage)count++;
 return count;
}
static uint16_t digiFindAny(const char*name){
 for(uint8_t v=16;v<=22;v++){uint16_t x=digiFind(v,name);if(x!=DIGI_NO_FUSION)return x;}
 for(uint16_t i=0;i<DIGI_SPECIES_COUNT;i++)if(!strcmp(DIGI_SPECIES[i].name,name))return i;
 return DIGI_NO_FUSION;
}
static bool digiQualifiedAnyName(const char*name,uint16_t current,uint8_t lv,const uint8_t*best,const uint8_t*wildMat,uint8_t need){
 for(uint16_t x=0;x<DIGI_SPECIES_COUNT;x++)if(!strcmp(DIGI_SPECIES[x].name,name)){
  if((x==current&&lv>=need)||(best&&best[x]>=need)||digiWildMaterial(x,wildMat))return true;
 }
 return false;
}
static uint16_t digiFindRoute(uint8_t version,const char*name){
 uint16_t x=digiFind(version,name);return x!=DIGI_NO_FUSION?x:digiFindAny(name);
}
static bool dmulBalancedRoute(uint16_t a,uint16_t d,uint16_t s,uint16_t h){
 return a==d&&d==s&&s==h&&(a+d+s+h)>=4;
}
static uint8_t dmulBranches(uint16_t i,uint16_t out[4]){
 if(i>=DIGI_SPECIES_COUNT||!isDmulVersion(DIGI_SPECIES[i].version)||!out)return 0;
 const DigiSpecies&cur=DIGI_SPECIES[i];const char*n=cur.name;
 auto set4=[&](const char*atk,const char*def,const char*spe,const char*hp){
  // Route columns are exactly TamaPoke's visible ATK / DEF / SPE / HP training values.
  const char*nm[4]={atk,def,spe,hp};uint8_t valid=0;
  for(uint8_t k=0;k<4;k++){uint16_t x=digiFindRoute(cur.version,nm[k]);out[k]=x==DIGI_NO_FUSION?i:x;if(x!=DIGI_NO_FUSION)valid++;}
  return valid;
 };
 if(!strcmp(n,"Dodomon"))return set4("Dorimon","Gigimon","Dorimon","Gigimon");
 if(!strcmp(n,"Kuramon"))return set4("Tsumemon","Tsumemon","Tsumemon","Tsumemon");
 if(!strcmp(n,"Pitchmon"))return set4("Moonmon","Moonmon","Moonmon","Moonmon");
 if(!strcmp(n,"Bubbmon"))return set4("Mochimon","Mochimon","Mochimon","Mochimon");
 if(!strcmp(n,"Mokumon"))return set4("Pokomon","Pokomon","Pokomon","Pokomon");
 if(!strcmp(n,"Botamon"))return set4("Koromon","Koromon","Koromon","Koromon");
 if(!strcmp(n,"Chibomon"))return set4("DemiVeemon","DemiVeemon","DemiVeemon","DemiVeemon");
 if(!strcmp(n,"Dorimon"))return set4("DORUmon","Ryudamon","Dracomon","DORUmon");
 if(!strcmp(n,"Gigimon"))return set4("Guilmon","Dracomon","Guilmon","Dracomon");
 if(!strcmp(n,"Tsumemon"))return set4("Keramon","Dracmon","Ghostmon","Tsukaimon");
 if(!strcmp(n,"Moonmon"))return set4("Swimmon","Kamemon","Lunamon","Sangomon");
 if(!strcmp(n,"Mochimon"))return set4("Gaomon","Pomumon","Funbeemon","Lalamon");
 if(!strcmp(n,"Pokomon"))return set4("Renamon","Impmon","Gazimon","Goblimon");
 if(!strcmp(n,"Koromon"))return set4("Hackmon","Kudamon","Lucemon","Morphomon");
 if(!strcmp(n,"DemiVeemon"))return set4("Veemon","Wormmon","Hawkmon","Armadillomon");
 if(!strcmp(n,"DORUmon"))return set4("DORUgamon","Coredramon Blue","Raptordramon","Coredramon Green");
 if(!strcmp(n,"Ryudamon"))return set4("Ginryumon","Coredramon Green","Coredramon Blue","Ginryumon");
 if(!strcmp(n,"Guilmon"))return set4("Growmon","GeoGreymon","Coredramon Blue","Coredramon Green");
 if(!strcmp(n,"Dracomon"))return set4("Coredramon Blue","Coredramon Green","GeoGreymon","Coredramon Green");
 if(!strcmp(n,"DORUgamon"))return set4("DORUguremon","Grademon","Wingdramon","Groundramon");
 if(!strcmp(n,"Raptordramon"))return set4("DORUguremon","Grademon","Wingdramon","RizeGreymon");
 if(!strcmp(n,"Ginryumon"))return set4("Hisyaryumon","Groundramon","Wingdramon","Hisyaryumon");
 if(!strcmp(n,"Growmon"))return set4("MegaloGrowlmon","RizeGreymon","Wingdramon","Groundramon");
 if(!strcmp(n,"Coredramon Blue"))return set4("Wingdramon","Groundramon","RizeGreymon","Wingdramon");
 if(!strcmp(n,"Coredramon Green"))return set4("Groundramon","Wingdramon","RizeGreymon","Groundramon");
 if(!strcmp(n,"GeoGreymon"))return set4("RizeGreymon","Groundramon","Wingdramon","RizeGreymon");
 if(!strcmp(n,"DORUguremon"))return set4("DORUgoramon","Alphamon","Slayerdramon","Breakdramon");
 if(!strcmp(n,"Grademon"))return set4("Alphamon","DORUgoramon","Slayerdramon","Breakdramon");
 if(!strcmp(n,"Hisyaryumon"))return set4("Ouryumon","Slayerdramon","Breakdramon","Ouryumon");
 if(!strcmp(n,"MegaloGrowlmon"))return set4("Dukemon","Slayerdramon","Breakdramon","Dukemon");
 if(!strcmp(n,"Wingdramon"))return set4("Slayerdramon","Breakdramon","Slayerdramon","Breakdramon");
 if(!strcmp(n,"Groundramon"))return set4("Breakdramon","Breakdramon","Slayerdramon","Breakdramon");
 if(!strcmp(n,"RizeGreymon"))return set4("Slayerdramon","Breakdramon","Slayerdramon","DORUgoramon");
 if(!strcmp(n,"Keramon"))return set4("Kurisarimon","IceDevimon","Soulmon","Boogiemon");
 if(!strcmp(n,"Dracmon"))return set4("Sangloupmon","Fangmon","Witchmon","Boogiemon");
 if(!strcmp(n,"Ghostmon"))return set4("Soulmon","Witchmon","Boogiemon","IceDevimon");
 if(!strcmp(n,"Tsukaimon"))return set4("IceDevimon","Fangmon","Witchmon","Boogiemon");
 if(!strcmp(n,"Kurisarimon"))return set4("Infermon","NeoDevimon","Wisemon","Cerberumon");
 if(!strcmp(n,"Soulmon"))return set4("Wisemon","SkullBaluchimon","NeoDevimon","Matadormon");
 if(!strcmp(n,"IceDevimon"))return set4("NeoDevimon","Wisemon","SkullBaluchimon","Cerberumon");
 if(!strcmp(n,"Sangloupmon"))return set4("Matadormon","Cerberumon","Astamon","SkullBaluchimon");
 if(!strcmp(n,"Fangmon"))return set4("Cerberumon","Matadormon","Astamon","SkullBaluchimon");
 if(!strcmp(n,"Witchmon"))return set4("Wisemon","Astamon","NeoDevimon","Matadormon");
 if(!strcmp(n,"Boogiemon"))return set4("Astamon","NeoDevimon","SkullBaluchimon","Cerberumon");
 if(!strcmp(n,"Infermon"))return set4("Diablomon","Diablomon","Diablomon","Diablomon");
 if(!strcmp(n,"Matadormon"))return set4("GranDracmon","Barbamon","BeelStarmon","Murmukusmon");
 if(!strcmp(n,"Astamon"))return set4("Barbamon","GranDracmon","BeelStarmon","Lilithmon");
 if(!strcmp(n,"NeoDevimon"))return set4("Barbamon","Lilithmon","GranDracmon","Murmukusmon");
 if(!strcmp(n,"SkullBaluchimon"))return set4("Murmukusmon","Lilithmon","BeelStarmon","GranDracmon");
 if(!strcmp(n,"Wisemon"))return set4("Barbamon","GranDracmon","BeelStarmon","Murmukusmon");
 if(!strcmp(n,"Cerberumon"))return set4("GranDracmon","Lilithmon","Murmukusmon","BeelStarmon");
 if(!strcmp(n,"Lunamon"))return set4("Lekismon","Dolphmon","Tylomon","Tobiumon");
 if(!strcmp(n,"Swimmon"))return set4("Dolphmon","Tylomon","Tobiumon","Orcamon");
 if(!strcmp(n,"Kamemon"))return set4("Tylomon","Orcamon","Tobiumon","Dolphmon");
 if(!strcmp(n,"Sangomon"))return set4("Tobiumon","Tylomon","Orcamon","Dolphmon");
 if(!strcmp(n,"Penmon"))return set4("Dolphmon","Orcamon","Tylomon","Tobiumon");
 if(!strcmp(n,"Lekismon"))return set4("Crescemon","MarinChimairamon","Divemon","Gusokumon");
 if(!strcmp(n,"Dolphmon"))return set4("MarinChimairamon","Divemon","WaruSeadramon","Gusokumon");
 if(!strcmp(n,"Tylomon"))return set4("WaruSeadramon","Gusokumon","Divemon","MarinChimairamon");
 if(!strcmp(n,"Tobiumon"))return set4("Divemon","MarinChimairamon","Gusokumon","WaruSeadramon");
 if(!strcmp(n,"Orcamon"))return set4("Gusokumon","WaruSeadramon","MarinChimairamon","Divemon");
 if(!strcmp(n,"Crescemon"))return set4("Dianamon","AncientMermaimon","Neptunemon","Regalecusmon");
 if(!strcmp(n,"MarinChimairamon"))return set4("Regalecusmon","Leviamon","AncientMermaimon","Neptunemon");
 if(!strcmp(n,"Gusokumon"))return set4("Neptunemon","Leviamon","Regalecusmon","AncientMermaimon");
 if(!strcmp(n,"WaruSeadramon"))return set4("Leviamon","Neptunemon","Regalecusmon","AncientMermaimon");
 if(!strcmp(n,"Divemon"))return set4("Regalecusmon","Neptunemon","AncientMermaimon","Leviamon");
 if(!strcmp(n,"Gaomon"))return set4("Gaogamon","Parasaurmon","Waspmon","Sunflowmon");
 if(!strcmp(n,"Pomumon"))return set4("Parasaurmon","Sunflowmon","Waspmon","Gaogamon");
 if(!strcmp(n,"Funbeemon"))return set4("Waspmon","Parasaurmon","Gaogamon","Sunflowmon");
 if(!strcmp(n,"Lalamon"))return set4("Sunflowmon","Parasaurmon","Waspmon","Gaogamon");
 if(!strcmp(n,"Gaogamon"))return set4("MachGaogamon","Ajatarmon","CannonBeemon","Lilamon");
 if(!strcmp(n,"Parasaurmon"))return set4("Ajatarmon","Lilamon","CannonBeemon","MachGaogamon");
 if(!strcmp(n,"Sunflowmon"))return set4("Lilamon","Ajatarmon","CannonBeemon","MachGaogamon");
 if(!strcmp(n,"Waspmon"))return set4("CannonBeemon","Ajatarmon","MachGaogamon","Lilamon");
 if(!strcmp(n,"MachGaogamon"))return set4("MirageGaogamon","GrandisKuwagamon","TigerVespamon","Lotusmon");
 if(!strcmp(n,"Ajatarmon"))return set4("Lotusmon","Bancho Lilimon","GrandisKuwagamon","MirageGaogamon");
 if(!strcmp(n,"CannonBeemon"))return set4("TigerVespamon","GrandisKuwagamon","Bancho Lilimon","MirageGaogamon");
 if(!strcmp(n,"Lilamon"))return set4("Lotusmon","Bancho Lilimon","MirageGaogamon","GrandisKuwagamon");
 if(!strcmp(n,"Renamon"))return set4("Kyubimon","Sorcermon","BlackTailmon","Musyamon");
 if(!strcmp(n,"Impmon"))return set4("Sorcermon","Musyamon","Fugamon","BlackTailmon");
 if(!strcmp(n,"Gazimon"))return set4("Fugamon","Musyamon","Sorcermon","BlackTailmon");
 if(!strcmp(n,"Goblimon"))return set4("Fugamon","Musyamon","BlackTailmon","Sorcermon");
 if(!strcmp(n,"Phascomon"))return set4("BlackTailmon","Sorcermon","Fugamon","Kyubimon");
 if(!strcmp(n,"Kyubimon"))return set4("Taomon","Bastemon","Archnemon","Baalmon");
 if(!strcmp(n,"Sorcermon"))return set4("Baalmon","Taomon","Bastemon","SkullSatamon");
 if(!strcmp(n,"BlackTailmon"))return set4("Bastemon","Archnemon","Taomon","Baalmon");
 if(!strcmp(n,"Musyamon"))return set4("SkullSatamon","Baalmon","Archnemon","Taomon");
 if(!strcmp(n,"Fugamon"))return set4("SkullSatamon","Baalmon","Bastemon","Archnemon");
 if(!strcmp(n,"Taomon"))return set4("Sakuyamon","Kuzuhamon","Plutomon","Gulfmon");
 if(!strcmp(n,"Baalmon"))return set4("Beelzebumon","Gulfmon","Plutomon","Kuzuhamon");
 if(!strcmp(n,"Bastemon"))return set4("Kuzuhamon","Gulfmon","Sakuyamon","Plutomon");
 if(!strcmp(n,"Archnemon"))return set4("Gulfmon","Plutomon","Kuzuhamon","Beelzebumon");
 if(!strcmp(n,"SkullSatamon"))return set4("Beelzebumon","Gulfmon","Plutomon","Kuzuhamon");
 if(!strcmp(n,"Hackmon"))return set4("BaoHackmon","Gladimon","Reppamon","Pidmon");
 if(!strcmp(n,"Kudamon"))return set4("Reppamon","Pidmon","Gladimon","Darcmon");
 if(!strcmp(n,"Patamon"))return set4("Gladimon","Reppamon","Pidmon","Darcmon");
 if(!strcmp(n,"Morphomon"))return set4("Darcmon","Reppamon","Gladimon","Pidmon");
 if(!strcmp(n,"Coronamon"))return set4("Firamon","Firamon","Firamon","Firamon");
 if(!strcmp(n,"BaoHackmon"))return set4("SaviorHackmon","Chirinmon","Mistymon","Hippogriffomon");
 if(!strcmp(n,"Gladimon"))return set4("Mistymon","Chirinmon","Hippogriffomon","SaviorHackmon");
 if(!strcmp(n,"Reppamon"))return set4("Chirinmon","Hippogriffomon","Mistymon","SaviorHackmon");
 if(!strcmp(n,"Pidmon"))return set4("Hippogriffomon","Mistymon","Chirinmon","SaviorHackmon");
 if(!strcmp(n,"Darcmon"))return set4("Mistymon","Hippogriffomon","Chirinmon","SaviorHackmon");
 if(!strcmp(n,"Firamon"))return set4("Flaremon","Flaremon","Flaremon","Flaremon");
 if(!strcmp(n,"SaviorHackmon"))return set4("Jesmon","Craniummon","Duftmon","Sleipmon");
 if(!strcmp(n,"Chirinmon"))return set4("Sleipmon","Seraphimon","Ophanimon","Duftmon");
 if(!strcmp(n,"Hippogriffomon"))return set4("Ophanimon","Seraphimon","Sleipmon","Duftmon");
 if(!strcmp(n,"Mistymon"))return set4("Duftmon","Craniummon","Seraphimon","Ophanimon");
 if(!strcmp(n,"Flaremon"))return set4("Apollomon","Apollomon","Apollomon","Apollomon");
 if(!strcmp(n,"Veemon"))return set4("ExVeemon","Snimon","Aquilamon","Ankylomon");
 if(!strcmp(n,"Wormmon"))return set4("Snimon","ExVeemon","Ankylomon","Aquilamon");
 if(!strcmp(n,"Hawkmon"))return set4("Aquilamon","ExVeemon","Snimon","Ankylomon");
 if(!strcmp(n,"Armadillomon"))return set4("Ankylomon","Snimon","ExVeemon","Aquilamon");
 if(!strcmp(n,"ExVeemon"))return set4("Meteormon","JewelBeemon","Yatagaramon","Meteormon");
 if(!strcmp(n,"Snimon"))return set4("JewelBeemon","Yatagaramon","Meteormon","JewelBeemon");
 if(!strcmp(n,"Aquilamon"))return set4("Yatagaramon","Meteormon","JewelBeemon","Yatagaramon");
 if(!strcmp(n,"Ankylomon"))return set4("Meteormon","JewelBeemon","Yatagaramon","Meteormon");
 if(!strcmp(n,"JewelBeemon"))return set4("Valkyrimon","Ravmon","Valkyrimon","Ravmon");
 if(!strcmp(n,"Yatagaramon"))return set4("Ravmon","Valkyrimon","Ravmon","Valkyrimon");
 if(!strcmp(n,"Meteormon"))return set4("Valkyrimon","Ravmon","Valkyrimon","Ravmon");
 if(!strcmp(n,"Silphymon"))return set4("Valkyrimon","Valkyrimon","Valkyrimon","Valkyrimon");
 if(!strcmp(n,"Shakkoumon"))return set4("Valkyrimon","Ravmon","Valkyrimon","Ravmon");
 return 0;
}
static uint8_t dmulRoute(uint16_t i,uint16_t a,uint16_t d,uint16_t s,uint16_t h){
 if(i>=DIGI_SPECIES_COUNT)return 0;
 const DigiSpecies&cur=DIGI_SPECIES[i];
 const uint16_t tr[4]={a,d,s,h};
 uint16_t high=tr[0];for(uint8_t k=1;k<4;k++)if(tr[k]>high)high=tr[k];
 // On a tie, prefer the species' natural style when that stat is tied. This
 // prevents untrained babies from always falling into ATK while keeping the
 // result deterministic and fully explainable to the player.
 uint8_t natural=cur.style&3;if(tr[natural]==high)return natural;
 for(uint8_t k=0;k<4;k++)if(tr[k]==high)return k;
 return 0;
}

uint8_t digimonEvolutionBranches(uint16_t i,uint16_t out[4]){
 if(!out)return 0;for(uint8_t k=0;k<4;k++)out[k]=i;
 if(i>=DIGI_SPECIES_COUNT)return 0;const DigiSpecies&cur=DIGI_SPECIES[i];if(cur.stage>=DIGI_ULTIMATE)return 0;
 if(isDmulVersion(cur.version))return dmulBranches(i,out);
 uint16_t all[12];uint8_t count=0;
 for(uint16_t x=0;x<DIGI_SPECIES_COUNT&&count<12;x++)if(DIGI_SPECIES[x].version==cur.version&&DIGI_SPECIES[x].stage==cur.stage+1&&!isPendulumFusionSpecies(x))all[count++]=x;
 if(!count)return 0;

 // DMC Ver.1-5 use compact, fixed late-stage families. Normally Adult ranks
 // 0-2, 3-5 and 6 evolve to Perfect ranks 0, 1 and 2. Ver.3 has four Perfects,
 // so it uses 2/2/2/1 to keep Chimairamon obtainable. Each Perfect then evolves
 // by rank; Ver.3's fourth Perfect shares its third Ultimate. Training style no
 // longer changes either result. Pendulum routes remain unchanged.
 if(cur.version>=1&&cur.version<=5&&(cur.stage==DIGI_ADULT||cur.stage==DIGI_PERFECT)){
  uint8_t rank=digiStageRank(i);
  uint8_t targetRank=cur.stage==DIGI_ADULT?(count==4?rank/2:rank/3):rank;
  if(targetRank>=count)targetRank=count-1;
  for(uint8_t stat=0;stat<4;stat++)out[stat]=all[targetRank];
  return 1;
 }

 // Every individual has a stable, small family instead of access to the whole
 // device roster. Babies may reach all available Child forms, while later
 // stages are limited to a local family of at most four/three evolutions.
 uint8_t limit=cur.stage<=DIGI_CHILD?4:(count<=3?2:3);if(limit>count)limit=count;
 uint8_t sourceCount=digiStageCount(cur.version,cur.stage);if(!sourceCount)sourceCount=1;
 uint8_t rank=digiStageRank(i);
 uint8_t start=sourceCount>1?(uint16_t)rank*(count-limit)/(sourceCount-1):0;

 for(uint8_t stat=0;stat<4;stat++){
  out[stat]=all[start+(stat%limit)];
 }
 return limit;
}
static uint16_t dmulSpecialEvolutionTarget(uint16_t i,uint8_t lv,uint16_t a,uint16_t d,uint16_t s,uint16_t h,const uint8_t*best){
 if(i>=DIGI_SPECIES_COUNT)return DIGI_NO_FUSION;
 const DigiSpecies&cur=DIGI_SPECIES[i];const char*n=cur.name;
 auto target=[&](const char*name){return digiFindAny(name);};
 auto q=[&](const char*name,uint8_t need){return digiQualifiedAnyName(name,i,lv,best,nullptr,need);};
 // Extra controllable Child routes. Four dominant stats remain the normal routes;
 // fully balanced training unlocks the fifth Child where a field needs one.
 if(cur.version==18&&!strcmp(n,"Moonmon")&&dmulBalancedRoute(a,d,s,h))return target("Penmon");
 if(cur.version==20&&!strcmp(n,"Pokomon")&&dmulBalancedRoute(a,d,s,h))return target("Phascomon");
 if(cur.version==21&&!strcmp(n,"Koromon")){
  if(a>=3&&s>=3&&a==s&&a>d&&a>h)return target("Coronamon");
  if(dmulBalancedRoute(a,d,s,h))return target("Patamon");
 }
 // Dragon / Dark / Deep cross-line special evolutions.
 if(cur.version==17&&!strcmp(n,"Diablomon")&&lv>=60&&a>=80&&q("Kuramon",5))return target("Armagemon");
 // Reward-style mode changes.
 if(cur.version==19&&!strcmp(n,"MirageGaogamon")&&lv>=60&&a+s>=90)return target("MirageGaogamon Burst Mode");
 if(cur.version==20&&!strcmp(n,"Beelzebumon")&&lv>=60&&a+s>=90&&q("Baalmon",45))return target("Beelzebumon Blast Mode");
 if(cur.version==21&&!strcmp(n,"Lucemon")&&lv>=45&&(a+d+s+h)>=70)return target("Lucemon Falldown Mode");
 if(cur.version==21&&!strcmp(n,"Lucemon Falldown Mode")&&lv>=60&&a+h>=90)return target("Lucemon Satan Mode");
 // Imperial Ver.22 Jogress and mode changes.
 if(cur.version==22&&(!strcmp(n,"Paildramon")||!strcmp(n,"Dinobeemon"))&&lv>=45)return target("Imperialdramon Dragon Mode");
 if(cur.version==22&&!strcmp(n,"Imperialdramon Dragon Mode")&&lv>=55&&a+s>=60)return target("Imperialdramon Fighter Mode");
 if(cur.version==22&&!strcmp(n,"Imperialdramon Fighter Mode")&&lv>=60&&q("Omegamon",55))return target("Imperialdramon Paladin Mode");
 if(cur.version==22&&!strcmp(n,"Imperialdramon Paladin Mode")&&lv>=70&&a+s>=100)return target("Imperialdramon OmegaX");
 return DIGI_NO_FUSION;
}
uint16_t digimonJogressTarget(uint16_t i,uint8_t lv,uint8_t a,uint8_t d,uint8_t s,uint8_t h,const uint8_t*best,const uint8_t*wildMat){
  (void)a;(void)d;(void)s;(void)h;
  if(i>=DIGI_SPECIES_COUNT)return DIGI_NO_FUSION;
  // Legacy cross-version fusions. A qualified partner in raising history unlocks
  // the option, but does not force it over a normal evolution branch.
  if(best){
    if((i==14||i==32)&&(best[14]>=55||(i==14&&lv>=55))&&(best[32]>=55||(i==32&&lv>=55)))return DIGI_OMNIMON_ALTER_S;
    if((i==51||i==66)&&(best[51]>=55||(i==51&&lv>=55))&&(best[66]>=55||(i==66&&lv>=55)))return DIGI_CHAOSMON;
    if((i==48||i==83)&&(best[48]>=55||(i==48&&lv>=55))&&(best[83]>=55||(i==83&&lv>=55)))return DIGI_MILLENNIUMMON;
  }
  uint16_t pf=pendulumFusionTarget(i,lv,best,wildMat);
  if(pf!=DIGI_NO_FUSION)return pf;

  const DigiSpecies&cur=DIGI_SPECIES[i];
  const char*n=cur.name;
  auto target=[&](const char*name){return digiFindAny(name);};
  auto q=[&](const char*name,uint8_t need){return digiQualifiedAnyName(name,i,lv,best,wildMat,need);};

  // DMUL Jogress routes. These used to live inside digimonEvolutionTarget(),
  // which meant a qualified Jogress could make a normal stat branch impossible.
  if(cur.version==16&&lv>=55&&(!strcmp(n,"Slayerdramon")||!strcmp(n,"Breakdramon"))){
    const char*other=!strcmp(n,"Slayerdramon")?"Breakdramon":"Slayerdramon";
    if(q(other,55))return target("Examon");
  }
  if(lv>=55&&(!strcmp(n,"Dianamon")||!strcmp(n,"Apollomon"))){
    const char*other=!strcmp(n,"Dianamon")?"Apollomon":"Dianamon";
    if(q(other,55))return target("GraceNovamon");
  }
  if(cur.version==21&&!strcmp(n,"Jesmon")&&lv>=60&&q("Gankoomon",55))return target("JESmon GX");
  if(cur.version==22&&cur.stage==DIGI_ADULT&&lv>=25){
    if(!strcmp(n,"ExVeemon")&&q("Snimon",25))return target("Paildramon");
    if(!strcmp(n,"Snimon")&&q("ExVeemon",25))return target("Dinobeemon");
    if(!strcmp(n,"Aquilamon")&&q("Tailmon",25))return target("Silphymon");
    if(!strcmp(n,"Ankylomon")&&q("Angemon",25))return target("Shakkoumon");
  }
  return DIGI_NO_FUSION;
}
uint16_t digimonEvolutionTarget(uint16_t i,uint8_t lv,uint8_t a,uint8_t d,uint8_t s,uint8_t h,const uint8_t*best){
  if(i>=DIGI_SPECIES_COUNT)return i;
  // Normal/special evolution only. Jogress/fusion is resolved separately by
  // digimonJogressTarget() and must be explicitly selected by the player.
  if(i==83&&lv>=60&&a>=80&&d>=60)return DIGI_CHAOSDRAMON;
  const DigiSpecies&cur=DIGI_SPECIES[i];
  if(cur.version==16&&!strcmp(cur.name,"Dukemon")&&lv>=60&&a+s>=80){
    uint16_t cm=digiFind(16,"Dukemon Crimson Mode");if(cm!=DIGI_NO_FUSION)return cm;
  }
  uint16_t special=dmulSpecialEvolutionTarget(i,lv,a,d,s,h,best);
  if(special!=DIGI_NO_FUSION)return special;
  if(cur.stage>=DIGI_ULTIMATE||lv<digimonEvolutionLevel(i))return i;
  uint16_t branches[4];if(!digimonEvolutionBranches(i,branches))return i;
  if(isDmulVersion(cur.version))return branches[dmulRoute(i,a,d,s,h)];
  uint16_t tr[4]={a,d,s,h};uint16_t high=tr[0];for(uint8_t x=1;x<4;x++)if(tr[x]>high)high=tr[x];
  uint8_t bestStat=0;for(uint8_t x=0;x<4;x++)if(tr[x]==high){bestStat=x;break;}
  return branches[bestStat];
}
