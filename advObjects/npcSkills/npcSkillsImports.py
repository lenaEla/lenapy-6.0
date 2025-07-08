from advObjects.advSkills import *
from advObjects.advWeapons import *
from advObjects.advEffects import *
from advObjects.advSummons import *
from advObjects.advStuffs import *

charmingHalf = copy.deepcopy(charming)
charmingHalf.strength,charmingHalf.magie,charmingHalf.charisma,charmingHalf.intelligence = charmingHalf.strength//2,charmingHalf.magie//2,charmingHalf.charisma//2,charmingHalf.intelligence//2
charmingHalf.name, charmingHalf.id, charmingHalf.emoji = "Atorakushon", "charming4", sameSpeciesEmoji("<:charmMalB:1103342838290329701>","<:charmMalR:1103342859840667710>")