-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: acd_game
-- ------------------------------------------------------
-- Server version	8.0.40-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cartas`
--

DROP TABLE IF EXISTS `cartas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cartas` (
  `id_carta` int NOT NULL AUTO_INCREMENT,
  `id_tipo_baraja` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `valor_juego` decimal(3,1) NOT NULL,
  `palo` varchar(20) NOT NULL,
  PRIMARY KEY (`id_carta`),
  KEY `id_tipo_baraja` (`id_tipo_baraja`),
  CONSTRAINT `cartas_ibfk_1` FOREIGN KEY (`id_tipo_baraja`) REFERENCES `tipos_barajas` (`id_tipo_baraja`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=149 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cartas`
--

LOCK TABLES `cartas` WRITE;
/*!40000 ALTER TABLE `cartas` DISABLE KEYS */;
INSERT INTO `cartas` VALUES (1,1,'As de Oros',1.0,'oros'),(2,1,'Dos de Oros',2.0,'oros'),(3,1,'Tres de Oros',3.0,'oros'),(4,1,'Cuatro de Oros',4.0,'oros'),(5,1,'Cinco de Oros',5.0,'oros'),(6,1,'Seis de Oros',6.0,'oros'),(7,1,'Siete de Oros',7.0,'oros'),(8,1,'Ocho de Oros',0.5,'oros'),(9,1,'Nueve de Oros',0.5,'oros'),(10,1,'Diez de Oros',0.5,'oros'),(11,1,'Sota de Oros',0.5,'oros'),(12,1,'Caballo de Oros',0.5,'oros'),(13,1,'Rey de Oros',0.5,'oros'),(14,1,'As de Copas',1.0,'copas'),(15,1,'Dos de Copas',2.0,'copas'),(16,1,'Tres de Copas',3.0,'copas'),(17,1,'Cuatro de Copas',4.0,'copas'),(18,1,'Cinco de Copas',5.0,'copas'),(19,1,'Seis de Copas',6.0,'copas'),(20,1,'Siete de Copas',7.0,'copas'),(21,1,'Ocho de Copas',0.5,'copas'),(22,1,'Nueve de Copas',0.5,'copas'),(23,1,'Diez de Copas',0.5,'copas'),(24,1,'Sota de Copas',0.5,'copas'),(25,1,'Caballo de Copas',0.5,'copas'),(26,1,'Rey de Copas',0.5,'copas'),(27,1,'As de Espadas',1.0,'espadas'),(28,1,'Dos de Espadas',2.0,'espadas'),(29,1,'Tres de Espadas',3.0,'espadas'),(30,1,'Cuatro de Espadas',4.0,'espadas'),(31,1,'Cinco de Espadas',5.0,'espadas'),(32,1,'Seis de Espadas',6.0,'espadas'),(33,1,'Siete de Copas',7.0,'espadas'),(34,1,'Ocho de Espadas',0.5,'espadas'),(35,1,'Nueve de Espadas',0.5,'espadas'),(36,1,'Diez de Espadas',0.5,'espadas'),(37,1,'Sota de Espadas',0.5,'espadas'),(38,1,'Caballo de Espadas',0.5,'espadas'),(39,1,'Rey de Espadas',0.5,'espadas'),(40,1,'As de Bastos',1.0,'bastos'),(41,1,'Dos de Bastos',2.0,'bastos'),(42,1,'Tres de Bastos',3.0,'bastos'),(43,1,'Cuatro de Bastos',4.0,'bastos'),(44,1,'Cinco de Bastos',5.0,'bastos'),(45,1,'Seis de Bastos',6.0,'bastos'),(46,1,'Siete de Bastos',7.0,'bastos'),(47,1,'Ocho de Bastos',0.5,'bastos'),(48,1,'Nueve de Bastos',0.5,'bastos'),(49,1,'Diez de Bastos',0.5,'bastos'),(50,1,'Sota de Bastos',0.5,'bastos'),(51,1,'Caballo de Bastos',0.5,'bastos'),(52,1,'Rey de Bastos',0.5,'bastos'),(53,2,'As de Picas',1.0,'picas'),(54,2,'Dos de Picas',2.0,'picas'),(55,2,'Tres de Picas',3.0,'picas'),(56,2,'Cuatro de Picas',4.0,'picas'),(57,2,'Cinco de Picas',5.0,'picas'),(58,2,'Seis de Picas',6.0,'picas'),(59,2,'Siete de Picas',7.0,'picas'),(60,2,'Jack de Picas',0.5,'picas'),(61,2,'Queen de Picas',0.5,'picas'),(62,2,'King de Picas',0.5,'picas'),(63,2,'As de Corazones',1.0,'corazones'),(64,2,'Dos de Corazones',2.0,'corazones'),(65,2,'Tres de Corazones',3.0,'corazones'),(66,2,'Cuatro de Corazones',4.0,'corazones'),(67,2,'Cinco de Corazones',5.0,'corazones'),(68,2,'Seis de Corazones',6.0,'corazones'),(69,2,'Siete de Corazones',7.0,'corazones'),(70,2,'Jack de Corazones',0.5,'corazones'),(71,2,'Queen de Corazones',0.5,'corazones'),(72,2,'King de Corazones',0.5,'corazones'),(73,2,'As de Treboles',1.0,'treboles'),(74,2,'Dos de Treboles',2.0,'treboles'),(75,2,'Tres de Treboles',3.0,'treboles'),(76,2,'Cuatro de Treboles',4.0,'treboles'),(77,2,'Cinco de Treboles',5.0,'treboles'),(78,2,'Seis de Treboles',6.0,'treboles'),(79,2,'Siete de Treboles',7.0,'treboles'),(80,2,'Jack de Treboles',0.5,'treboles'),(81,2,'Queen de Treboles',0.5,'treboles'),(82,2,'King de Treboles',0.5,'treboles'),(83,2,'As de Diamantes',1.0,'diamantes'),(84,2,'Dos de Diamantes',2.0,'diamantes'),(85,2,'Tres de Diamantes',3.0,'diamantes'),(86,2,'Cuatro de Diamantes',4.0,'diamantes'),(87,2,'Cinco de Diamantes',5.0,'diamantes'),(88,2,'Seis de Diamantes',6.0,'diamantes'),(89,2,'Siete de Diamantes',7.0,'diamantes'),(90,2,'Jack de Diamantes',0.5,'diamantes'),(91,2,'Queen de Diamantes',0.5,'diamantes'),(92,2,'King de Diamantes',0.5,'diamantes'),(93,3,'1 de Corazones',1.0,'Corazones'),(94,3,'2 de Corazones',2.0,'Corazones'),(95,3,'3 de Corazones',3.0,'Corazones'),(96,3,'4 de Corazones',4.0,'Corazones'),(97,3,'5 de Corazones',5.0,'Corazones'),(98,3,'6 de Corazones',6.0,'Corazones'),(99,3,'7 de Corazones',7.0,'Corazones'),(100,3,'8 de Corazones',8.0,'Corazones'),(101,3,'9 de Corazones',9.0,'Corazones'),(102,3,'10 de Corazones',10.0,'Corazones'),(103,3,'Unter de Corazones',0.5,'Corazones'),(104,3,'Ober de Corazones',0.5,'Corazones'),(105,3,'König de Corazones',0.5,'Corazones'),(106,3,'Jahreszeit de Corazones (Primavera, Tierra)',0.5,'Corazones'),(107,3,'1 de Campanas',1.0,'Campanas'),(108,3,'2 de Campanas',2.0,'Campanas'),(109,3,'3 de Campanas',3.0,'Campanas'),(110,3,'4 de Campanas',4.0,'Campanas'),(111,3,'5 de Campanas',5.0,'Campanas'),(112,3,'6 de Campanas',6.0,'Campanas'),(113,3,'7 de Campanas',7.0,'Campanas'),(114,3,'8 de Campanas',8.0,'Campanas'),(115,3,'9 de Campanas',9.0,'Campanas'),(116,3,'10 de Campanas',10.0,'Campanas'),(117,3,'Unter de Campanas',0.5,'Campanas'),(118,3,'Ober de Campanas',0.5,'Campanas'),(119,3,'König de Campanas',0.5,'Campanas'),(120,3,'Jahreszeit de Campanas (Verano, Fuego)',0.5,'Campanas'),(121,3,'1 de Hojas',1.0,'Hojas'),(122,3,'2 de Hojas',2.0,'Hojas'),(123,3,'3 de Hojas',3.0,'Hojas'),(124,3,'4 de Hojas',4.0,'Hojas'),(125,3,'5 de Hojas',5.0,'Hojas'),(126,3,'6 de Hojas',6.0,'Hojas'),(127,3,'7 de Hojas',7.0,'Hojas'),(128,3,'8 de Hojas',8.0,'Hojas'),(129,3,'9 de Hojas',9.0,'Hojas'),(130,3,'10 de Hojas',10.0,'Hojas'),(131,3,'Unter de Hojas',0.5,'Hojas'),(132,3,'Ober de Hojas',0.5,'Hojas'),(133,3,'König de Hojas',0.5,'Hojas'),(134,3,'Jahreszeit de Hojas (Otoño, Aire)',0.5,'Hojas'),(135,3,'1 de Bellotas',1.0,'Bellotas'),(136,3,'2 de Bellotas',2.0,'Bellotas'),(137,3,'3 de Bellotas',3.0,'Bellotas'),(138,3,'4 de Bellotas',4.0,'Bellotas'),(139,3,'5 de Bellotas',5.0,'Bellotas'),(140,3,'6 de Bellotas',6.0,'Bellotas'),(141,3,'7 de Bellotas',7.0,'Bellotas'),(142,3,'8 de Bellotas',8.0,'Bellotas'),(143,3,'9 de Bellotas',9.0,'Bellotas'),(144,3,'10 de Bellotas',10.0,'Bellotas'),(145,3,'Unter de Bellotas',0.5,'Bellotas'),(146,3,'Ober de Bellotas',0.5,'Bellotas'),(147,3,'König de Bellotas',0.5,'Bellotas'),(148,3,'Jahreszeit de Bellotas (Invierno, Agua)',0.5,'Bellotas');
/*!40000 ALTER TABLE `cartas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-15 19:45:37
