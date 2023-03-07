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





