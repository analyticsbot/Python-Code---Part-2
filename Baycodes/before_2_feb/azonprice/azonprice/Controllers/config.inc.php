<?php
/*$VALEUR_hote='localhost';
$VALEUR_nom_bd='onparts_inventory';
$VALEUR_user='onparts_steven';
$VALEUR_mot_de_passe='developer';
  */
  
$VALEUR_hote='localhost';
$VALEUR_nom_bd='baycodes_azonprice';
$VALEUR_user='baycodes_sam';
$VALEUR_mot_de_passe='sam1234';



$connexion = new PDO('mysql:host='.$VALEUR_hote.';dbname='.$VALEUR_nom_bd,$VALEUR_user,$VALEUR_mot_de_passe);
$sql="
CREATE TABLE IF NOT EXISTS `azon_products` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `asin` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `upc` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `title` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `category` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `productrank` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `amazon_price` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `fba_price1` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `fba_price2` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `fba_price3` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `seller_price1` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `seller_price2` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `seller_price3` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1;
";
$connexion->exec($sql);

?>
