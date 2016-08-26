<?php

$VALEUR_hote='haffoudhijobscom1.ipagemysql.com';
$VALEUR_nom_bd='odesk_christian';
$VALEUR_user='christian';
$VALEUR_mot_de_passe='123';



$connexion = new PDO('mysql:host='.$VALEUR_hote.';dbname='.$VALEUR_nom_bd,$VALEUR_user,$VALEUR_mot_de_passe);


?>
