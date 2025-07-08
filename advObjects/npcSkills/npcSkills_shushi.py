from advObjects.npcSkills.npcSkillsImports import *

SHUSHIEXTURNINIT = 5

# COULEUR
# MOWI : Magenta -> Mono
# SWARO : Jaune -> AoE
# TRALA : Cyan -> Duo

# SLARIA : Rouge -> Carré
# FACLARIA : Vert -> GarCrit
# PLATORIA : Bleu -> Vol de vie

# CLOW : Noir -> DoT
# JALOW : Violet -> Différé
# NAWO : Blanc -> Armor Percing

FIRST_SKILL_POWER = 100
SECOND_SKILL_POWER = 120
THIRD_SKILL_POWER = 140

MOWI_PERCING = 20

mowiEff = effect("Mowi", "mowi", turnInit=SHUSHIEXTURNINIT, replace=True)

mowiSkill = skill(mowiEff.name, "magenta", TYPE_DAMAGE, power=int(FIRST_SKILL_POWER/2), repetition=2, emoji=mowiEff.emoji[0][0], effectOnSelf=mowiEff, range=AREA_CIRCLE_1, percing=MOWI_PERCING, description="Inflige deux attaques monocibles à la cible en ignorant une partie de la résistance adverse et vous permet d'utiliser les compétences {} {}, des compétences spécialisées dans les dégâts monocibles".format(mowiEff.emoji[0][0], mowiEff.name))

mowislariaEff = effect("Mowi-Slaria", "mowislariaEff", turnInit=SHUSHIEXTURNINIT, replace=True)
mowislaria_1 = skill(mowiSkill.name, mowiSkill.id, TYPE_DAMAGE, power=int(SECOND_SKILL_POWER*1.2/2), emoji=mowislariaEff.emoji, effectOnSelf=mowislariaEff, percing=MOWI_PERCING, description="Inflige deux attaques monocibles puis une troisième plus puissante à l'ennemi ciblé en ignorant une partie de la résistance de la cible, tout en vous permetant d'utiliser les compétences {} {}, infligeant de gros dégâts à une cible unique".format(mowislariaEff.emoji[0][0], mowislariaEff.name))
mowislaria_c = effect("Enchainement - {replicaName}", "mowislaria_c", replique=mowislaria_1, silent=True)
mowislaria = skill(mowiSkill.name, mowiSkill.id, TYPE_DAMAGE, power=int((SECOND_SKILL_POWER*1.2 - SECOND_SKILL_POWER*1.2/2)/2), emoji=mowislaria_1.name, percing=MOWI_PERCING, effectOnSelf=mowislaria_c, description=mowislaria_1.description, replay=True, needEffect=mowiEff)

mowiSlariaTi = skill("Mowi-Slaria-Ti", "maganta", TYPE_DAMAGE, power=int(THIRD_SKILL_POWER*1.4), percing=MOWI_PERCING, description="Inflige de gros dégâts ignorant une partie de la résistance de la cible", needEffect=mowislariaEff)
mowiSlariaPlatoria = skill("Mowi-Slaria-Platoria", "maganta", TYPE_DAMAGE, power=int(THIRD_SKILL_POWER*1.2), percing=MOWI_PERCING, lifeSteal=50, armorConvert=50, descrpition="Inflige des dégâts monocibles à l'ennemi ciblé en ignorant une partie de sa résistance et vous soigne et vous octroi de l'armure en fonction des dégâts infligés", needEffect=mowislariaEff)
mowiSlariaTralaEff = effect("Mowi-Slaria-Trala", "Mowi-Slaria-Trala", MAGIE, area=AREA_DONUT_1, power=int(FIRST_SKILL_POWER/2/3), trigger=TRIGGER_INSTANT, type=TYPE_DAMAGE)
mowiSlariaTrala = skill("Mowi-Slaria-Trala", "maganta", TYPE_DAMAGE, power=int(THIRD_SKILL_POWER*1.1/3), repetition=3, effects=mowiSlariaTralaEff, percing=MOWI_PERCING, emoji=mowiSlariaTralaEff.emoji[0][0], description="Inflige à trois reprises des dégâts à l'ennemi ciblé. Pour chaque attaque qui fait mouche, inflige également des dégâts aux ennemis au corps à corps de la cible", needEffect=mowislariaEff)

mowiflaclariaEff = effect("Mowi-Faclaria", "mowiflaclariaEff", turnInit=SHUSHIEXTURNINIT, replace=True)
mowiflaclaria = skill(mowiflaclariaEff.name, "maganta", TYPE_DAMAGE, emoji=mowiflaclariaEff.emoji[0][0], power=int(SECOND_SKILL_POWER*0.9), effectOnSelf=mowiflaclariaEff, description="Inflige des dégâts critiques à l'ennemi ciblé, ignorant une partie de sa résistance, et vous permet d'utiliser les compétences {} {}, spécialisées dans la dégâts mocibles critiques".format(mowiflaclariaEff.emoji[0][0], mowiflaclariaEff.name))

mowiFaclariaClowEff = effect("Mowi-Faclaria-Clow", "mowiFaclariaClowEff", MAGIE, power=int(SECOND_SKILL_POWER/3), turnInit=3, trigger=TRIGGER_START_OF_TURN, type=TYPE_INDIRECT_DAMAGE)
mowiFaclariaClow = skill(mowiFaclariaClowEff.name, "maganta", TYPE_DAMAGE, power=FIRST_SKILL_POWER, percing=MOWI_PERCING, garCrit=True, effects=mowiFaclariaClowEff, emoji=mowiFaclariaClowEff.emoji[0][0], description="Inflige une attaque monocible critique à la cible en ignorant une partie de sa défense et lui inflige un effet de dégâts sur la durée", needEffect=mowiflaclariaEff)
mowiFaclariaSlaria = skill("Mowi-Faclaria-Slaria", "maganta", TYPE_DAMAGE, power=int(THIRD_SKILL_POWER*0.65), repetition=2, percing=int(MOWI_PERCING*1.5), garCrit=True, description="Inflige deux attaques monocibles critiques à l'ennemi ciblé en ignorant une bonne partie de la résistance de la cible", needEffect=mowiflaclariaEff)
mowiFaclariaNawo_1 = skill("Mowi-Faclaria-Nawo", "maganta", TYPE_DAMAGE, power=int(THIRD_SKILL_POWER * 1.2 * 0.4), effects=weakGuard, damageOnArmor=1.5, percing=MOWI_PERCING, description="Inflige plusieurs attaques monocibles à l'ennemi ciblé, infligeant de gros dégâts sur l'armure de la cible et lui inflige {}".format(weakGuard))
mowiFaclariaNawo_c = effect("Enchainement - {replicaName}", "mowiFaclariaNawo_1", replique=mowiFaclariaNawo_1, silent=True)
mowiFaclariaNawo = skill(mowiFaclariaNawo_1.name, mowiFaclariaNawo_1.id, TYPE_DAMAGE, power=int((THIRD_SKILL_POWER * 1.2) - (THIRD_SKILL_POWER * 1.2 * 0.4)/4), repetition=4, effectOnSelf=mowiFaclariaNawo_c, replay=True, needEffect=mowiflaclariaEff, description=mowiFaclariaNawo_1.description, emoji=mowiFaclariaNawo_1.emoji)

mowiJallowEff = effect("Mowi-Jallow", "mowiJallowEff", turnInit=SHUSHIEXTURNINIT, replace=True)
mowiJallowDiffer = effect(mowiJallowEff.name, "mowiJallowDiffer", MAGIE, power=int(SECOND_SKILL_POWER*0.7), trigger=TRIGGER_ON_REMOVE, type=TYPE_INDIRECT_DAMAGE)
mowiJallow = skill(mowiJallowEff.name, "maganta", TYPE_DAMAGE, power=mowiJallowDiffer.power, effects=mowiJallowDiffer, emoji=mowiJallowDiffer.emoji[0][0], effectOnSelf=mowiJallowEff, description="Inflige des dégâts monocibles à la cible. Au début de votre prochain tour, la compétence est répliquée. Vous permet également d'utiliser les compétences {} {}, de puissantes compétences monocibles aux effets difféfés")

mowiJallowClowEff = effect("Mowi-Jallow-Clow", "mowiJallowClowEff", MAGIE, power=int(THIRD_SKILL_POWER/3), turnInit=3, trigger=TRIGGER_END_OF_TURN, type=TYPE_INDIRECT_DAMAGE)
mowiJallowClow = skill(mowiJallowClowEff.name, "", TYPE_DAMAGE, power=FIRST_SKILL_POWER, effects=mowiJallowClowEff, emoji=mowiJallowClowEff.emoji[0][0], description="Inflige une attaque à l'ennemi ciblé, ignorant une partie de sa résistance, et lui inflige un effet de dégâts sur la durée")

mowiJallowSlaria = effect('Mowi-Jallow-Slaria', 'mowiJallowSlaria')

shushiExSkill1 = skill(mowiSkill.name, mowiSkill.id, TYPE_DAMAGE, become=[
	mowiSkill,
		mowislaria,
			mowiSlariaTi, mowiSlariaPlatoria, mowiSlariaTrala,
		mowiflaclaria, 
			mowiFaclariaClow, mowiFaclariaSlaria, mowiFaclariaNawo])