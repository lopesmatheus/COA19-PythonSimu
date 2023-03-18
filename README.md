# COA19-PythonSimu

Les dossiers du projet COA19-Python s'organisent comme suit :

- fmus : contient les différents FMUs pour les PLANT et CTRL en fonction des O.S.

- Validation : valide le passage de Matlab à Python.
    *Validation.py -> Script utilisé pour la validation du code.
    *ValidationData.zip -> Data utilisé pour la validation du code.
    *Validation_FAVPOS.png -> Figure de validation FAVPOS.
    *Validation_TBAS.png -> Figure de validation TBAS_SENSOR.

- Tests : rédaction des différents cas tests fournis par le client.
    *test_plant.py -> Script de test de la plant sans controleur.
    *testcases -> classe avec les attributs des différents cas tests.
    *TestCases.py -> super classe des cas test.

- Main_Project : contient les algorithmes réalisés :
    * Main_PIE_Base_case_final.ipynb : algorithmes de RL appliqués au cas jouet.
    * Main_PIE_Plant_ResultatIntermediaire.ipynb : algorithme de RL appliqué au cas réel.


## Description du Main:
Ce code a pour but l'implémentation du méthode DDPG dans le cas du contrôle de la plant. Pour ce cas on a divers paramètres qui peuvent être réglés au-en plus de ceux qui sont habituellement réglés en Machine Learning (ML). Premièrement, on regarde les paramètres qui concernent les algorithmes de ML/DL :
-	Nombre de neurones par couche ;
-	Nombre de couches ;
-	Learning Rate ;

On remarque que tous ces paramètres peuvent être différents entre les réseaux acteur et critique et peuvent être réglés soit à l’appel de la classe DDPGAgent (nombre neurones et learning rate), soit à la construction des classes DefaultNNActor ou DefaultNNCritic. Par ailleurs, on a des paramètres qui peuvent être réglés et concernent spécifiquement des algorithmes de RL et DDPG :
-	Batch size : permettre régler la taille du nombre d'échantillons tirés du Replay Buffer à chaque itération pour entrainer l'algorithme ;
-	Gamma : Discount factor ;
-	Tau : Facteur d’update des réseaux target du DDPG. Ce paramètre permet un « trade-off » entre la vitesse et la stabilité de l’entrainement (détaillé dans https://arxiv.org/abs/1509.02971)
-	Noise_std : Écart type du bruit ajouté à l’action qui sera passé à la plant pour l’entrainement. Cela sert à laisser la possibilité d’explorer l’environnement. Un écart-type plus élevé permet une meilleure exploration de l’environnement, en revanche l’action correspondra moins à la sortie donnée par votre acteur.
Finalement, on a les paramètres qui concernent exclusivement le cas réel (cas spécifique à notre problème de système d'air):
-	Nombre d’états retenus (TBAS_SENSOR) ;
-	Informations d’entrée utilisés ;
Ces deux paramètres jouent sur l’information que sera utilisé par l’Agent DDPG. Dans ce code on a testé le réglage de 5 états de température retenus plus 3 états de l’entrée T_TPRV, pour qu’il puisse identifier la variation des paramètres d’entrée dans l’entrainement. Donc, cela donne 8 entrées au total dans le réseau, qui doivent être déclares dans l’attribut observation_space dans le constructeur de la classe de l’environnement Plant, comme l’exemple :

self.observation_space=gym.spaces.Box(np.array([-100.0 for i in range(8)]),
                                              	np.array([300.0 for i in range(8)]),(8,),np.float64)
                                                
Ainsi, il faut également changer spécifier la taille de chaque vecteur qui va retenir ces informations dans le constructeur et dans la méthode reset. Par exemple, on a dans les dernières lignes du constructeur (__init__) et de la fin de la méthode reset :
        self.state = np.zeros((5,))
        self.tvbas_ret = np.zeros((3,))
        
        
Enfin, il faut faire des petits changements de réglage de temps de simulation du cas test. Comme on a choisi pour commencer à 500 secondes (parce que dans le cas A_T01a était inutile contrôler avant car on n’a pas une manière de faire réchauffer la plante), on a une boucle dans la fin de la méthode reset qui fait la simulation de 500 secondes avec action 0. En plus, dans le début du constructeur on a changé :
self.Tend = self.CaseTest.getTsimu() - self.CaseTest.getTend()
Par 2000, ce qui fait la simulation finir à T=2000. Si vous voulez réaliser la simulation complète, il faut utiliser l’exemple ci-dessus. Finalement, comme on a testé le cas de la vanne sans hystérésis on a réglé la sortie de notre réseau acteur pour que la commande soit comprise entre 125 et 180 (espace d’action). Par conséquent, si vous voulez généraliser au cas avec hystérésis il faut changer l’espace d’action de la réseau acteur, ce qui peut être donné dans la méthode foward dans la classe DefaultNNActor par cette ligne :
running_output = 152.5 + 27.5 * running_output
Remarque : comme la fonction d’activation à la sortie du réseau acteur est une tangente hyperbolique, la sortie est comprise entre -1 et 1 avant le « scaling ».

Suggestions d’amélioration : Au-delà de l’étude et réglage des paramètres, c’est l’utilisation des pas de temps pour l’action plus petites, étude et amélioration de la fonction reward et étude sur l’utilisation de systèmes à grand inertie. Par exemple, l’article https://arxiv.org/abs/1509.02971 cite l’utilisation du bruit Ornstein-Uhlenbeck process pour l’amélioration de l’exploration.
![image](https://user-images.githubusercontent.com/74300809/226111634-57322f6d-9bbe-4ecd-a96f-d19441ee814d.png)


