from classes import duty
EVENT_FIGHT, EVENT_CHOICE, EVENT_END, EVENT_GOTO = 0, 1, 2, 3

ilianaQuestName = "Le_Grand_Noir"
bigDark0 = duty(ilianaQuestName,0,{
	1:[EVENT_CHOICE,["Qu'est-ce que cet endroit ?","Tu es là depuis longtemps ?","Tu veux dire quoi par \"Tu ne dvrais pas être là\" ?"],[2,3,4]],
	2:[EVENT_CHOICE,["Donc tu as un lieu juste pour toi où concrétiser tes échecs ? C'est pas très commode","Et comment cela se fait que je sois là du coup ?"],[5,6]],
	3:[EVENT_CHOICE,["Et à quoi sert-elle ?"],[7]],
	4:[EVENT_CHOICE,["J'aimerais bien le savoir moi-même","Mais je suis un dark Sasuke voyons, être que Ténèbres c'est mon dada"],[8,9]]
})
