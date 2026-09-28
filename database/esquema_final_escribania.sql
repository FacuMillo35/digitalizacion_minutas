-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: proyecto_final_bd
-- ------------------------------------------------------
-- Server version	8.4.6

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
-- Table structure for table `inmuebles`
--

DROP TABLE IF EXISTS `inmuebles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inmuebles` (
  `id_inmueble` int NOT NULL AUTO_INCREMENT,
  `partida_inmobiliaria` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `domicilio_inmueble` varchar(255) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `superficie` varchar(255) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `departamento` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT 'La Rioja',
  `localidad` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `registro_propiedad` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `folio_real` double DEFAULT NULL,
  `tomo_numero` varchar(30) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `anio_inscripcion` int DEFAULT NULL,
  `tipo_propiedad` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT 'Vertical',
  `ph_unidad_funcional` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `ph_poligono` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `ph_porcentaje` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `entre_calles` varchar(255) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `lote` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `manzana` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `nom_circunscripcion` varchar(10) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `nom_seccion` varchar(10) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `nom_manzana` varchar(10) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `nom_parcela` varchar(10) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_inmueble`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inmuebles`
--

LOCK TABLES `inmuebles` WRITE;
/*!40000 ALTER TABLE `inmuebles` DISABLE KEYS */;
INSERT INTO `inmuebles` VALUES (1,'12345','Copiapo y Santa Fe 158','342.00','La Rioja','La Rioja','23',2,'4',2026,'Vertical',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'123445','Cleofe Arias 158','343.00','La Rioja','La Rioja','34',3,'34',2026,'Vertical',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'12','Cleofe Arias 58','4500 mts2','La Rioja','La Rioja','47',7,'7',2026,'Propiedad Horizontal','212','2','2',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'547','Los Cedros 29','245mts2','La Rioja','La Rioja','8',3,'9',2026,'Propiedad Horizontal','2','32','25',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'56','Pringles 197','235Mts2','La Rioja','La Rioja','5',6,'7',2015,'Propiedad',NULL,NULL,NULL,'Artigas y Pringles','20','23',NULL,NULL,NULL,NULL),(6,NULL,'Calle Falsa 123','123mts2','La Rioja',NULL,NULL,NULL,NULL,NULL,'Propiedad',NULL,NULL,NULL,'Avenida Siempreviva 742 y Calle Presidente Clinton','2','4','A','I','342','9'),(7,NULL,'Calle Falsa 123','321 mts2','La Rioja',NULL,NULL,NULL,NULL,NULL,'Propiedad',NULL,NULL,NULL,'Avenida siempreviva 742 y Calle Presidente Clinton','34','45','A','I','234','2'),(8,NULL,'Santa Maria de Oro 321','321mts2','La Rioja',NULL,NULL,NULL,NULL,NULL,'Propiedad Horizontal',NULL,NULL,NULL,'Cleofe Arias y Jose Garibaldi','34','43','R','E','23','43'),(9,'23','Jose Garibaldi 23','321mts2','La Rioja','La Rioja','7',4,'4',2026,'Propiedad Horizontal','23','2','1','Cleofe Arias y Santa Maria de oro','56','65','R','N','45','90'),(10,'67','Avenida Peron 123','6767 Mts2','La Rioja','La Rioja','67',8,'9',2026,'Propiedad',NULL,NULL,NULL,'Avenida Peron y Santa fe','4','9','F','5','4','9'),(11,'85','Pringles 491','67 Mts2','La Rioja','La Rioja','7',9,'5',2026,'Propiedad Horizontal','3','78','60','Pringles y Artigas','8','2','9','A','7','9');
/*!40000 ALTER TABLE `inmuebles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `intervinientes_minuta`
--

DROP TABLE IF EXISTS `intervinientes_minuta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intervinientes_minuta` (
  `id_interviniente` int NOT NULL AUTO_INCREMENT,
  `id_minuta` int NOT NULL,
  `id_persona` int NOT NULL,
  `rol` enum('Titular','Vendedor','Comprador','Apoderado','Solicitante') COLLATE utf8mb4_spanish_ci NOT NULL,
  PRIMARY KEY (`id_interviniente`),
  KEY `id_minuta` (`id_minuta`),
  KEY `id_persona` (`id_persona`),
  CONSTRAINT `intervinientes_minuta_ibfk_1` FOREIGN KEY (`id_minuta`) REFERENCES `minuta_c_inmueble` (`id_minuta`),
  CONSTRAINT `intervinientes_minuta_ibfk_2` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id_persona`)
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intervinientes_minuta`
--

LOCK TABLES `intervinientes_minuta` WRITE;
/*!40000 ALTER TABLE `intervinientes_minuta` DISABLE KEYS */;
INSERT INTO `intervinientes_minuta` VALUES (1,1,1,'Vendedor'),(2,1,2,'Comprador'),(3,2,1,'Vendedor'),(4,2,2,'Comprador'),(5,3,1,'Vendedor'),(6,3,3,'Comprador'),(7,4,1,'Vendedor'),(8,4,3,'Comprador'),(9,5,3,'Vendedor'),(10,5,1,'Comprador'),(11,5,3,'Comprador'),(12,6,1,'Vendedor'),(13,6,2,'Comprador'),(14,7,1,'Vendedor'),(15,7,2,'Comprador'),(16,8,1,'Vendedor'),(17,8,3,'Comprador'),(18,9,3,'Vendedor'),(19,9,1,'Comprador'),(20,10,1,'Vendedor'),(21,10,3,'Vendedor'),(22,10,1,'Comprador'),(23,11,2,'Vendedor'),(24,11,1,'Comprador'),(25,12,1,'Vendedor'),(26,12,2,'Comprador'),(27,13,1,'Vendedor'),(28,13,4,'Comprador'),(29,14,2,'Vendedor'),(30,14,5,'Comprador'),(31,15,3,'Vendedor'),(32,15,5,'Comprador'),(33,16,1,'Vendedor'),(34,16,3,'Comprador'),(35,17,1,'Vendedor'),(36,17,2,'Comprador'),(37,18,1,'Vendedor'),(38,18,2,'Vendedor'),(39,18,3,'Comprador'),(40,18,4,'Comprador'),(41,19,1,'Vendedor'),(42,19,3,'Vendedor'),(43,19,2,'Comprador'),(44,19,4,'Comprador'),(45,20,1,'Vendedor'),(46,20,2,'Vendedor'),(47,20,3,'Vendedor'),(48,20,4,'Vendedor'),(49,20,5,'Vendedor'),(50,20,2,'Comprador'),(51,21,3,'Vendedor'),(52,21,2,'Comprador'),(53,22,2,'Vendedor'),(54,22,2,'Comprador'),(55,23,1,'Vendedor'),(56,23,2,'Vendedor'),(57,23,3,'Comprador'),(58,23,4,'Comprador'),(59,24,3,'Vendedor'),(60,24,1,'Comprador'),(61,25,1,'Vendedor'),(62,25,3,'Vendedor'),(63,25,2,'Comprador'),(64,26,1,'Vendedor'),(65,26,2,'Comprador'),(66,27,1,'Vendedor'),(67,27,2,'Comprador'),(68,28,3,'Vendedor'),(69,28,2,'Comprador'),(70,29,1,'Vendedor'),(71,29,2,'Comprador'),(72,30,1,'Vendedor'),(73,30,2,'Comprador'),(74,31,1,'Vendedor'),(75,31,2,'Comprador'),(76,32,1,'Vendedor'),(77,32,3,'Comprador'),(78,32,4,'Comprador'),(79,33,1,'Vendedor'),(80,33,2,'Comprador'),(81,34,2,'Vendedor'),(82,34,3,'Comprador'),(83,35,1,'Vendedor'),(84,35,3,'Comprador'),(85,36,1,'Vendedor'),(86,36,2,'Comprador'),(87,37,1,'Vendedor'),(88,37,3,'Comprador'),(89,38,1,'Vendedor'),(90,38,2,'Comprador'),(91,39,1,'Vendedor'),(92,39,2,'Comprador'),(93,40,4,'Vendedor'),(94,40,3,'Comprador'),(95,40,5,'Comprador'),(96,41,4,'Vendedor'),(97,41,5,'Comprador'),(98,42,4,'Vendedor'),(99,42,5,'Comprador'),(100,43,1,'Vendedor'),(101,43,5,'Comprador'),(102,44,6,'Vendedor'),(103,44,4,'Comprador'),(104,45,6,'Vendedor'),(105,45,3,'Comprador'),(106,46,6,'Vendedor'),(107,46,8,'Comprador'),(108,47,6,'Vendedor'),(109,47,4,'Comprador'),(110,48,4,'Vendedor'),(111,48,6,'Comprador'),(112,49,6,'Vendedor'),(113,49,2,'Comprador');
/*!40000 ALTER TABLE `intervinientes_minuta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `minuta_c_inmueble`
--

DROP TABLE IF EXISTS `minuta_c_inmueble`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `minuta_c_inmueble` (
  `id_minuta` int NOT NULL AUTO_INCREMENT,
  `id_inmueble` int NOT NULL,
  `id_usuario_escribano` int NOT NULL,
  `id_usuario` int NOT NULL,
  `motivo` text COLLATE utf8mb4_spanish_ci,
  `observaciones` text COLLATE utf8mb4_spanish_ci,
  `protocolo` int DEFAULT NULL,
  `tomo` varchar(20) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `folio` varchar(20) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `id_tramite` int DEFAULT NULL,
  `tipo_acto` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_minuta`),
  KEY `id_inmueble` (`id_inmueble`),
  KEY `id_usuario_escribano` (`id_usuario_escribano`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `minuta_c_inmueble_ibfk_1` FOREIGN KEY (`id_inmueble`) REFERENCES `inmuebles` (`id_inmueble`),
  CONSTRAINT `minuta_c_inmueble_ibfk_2` FOREIGN KEY (`id_usuario_escribano`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `minuta_c_inmueble_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `minuta_c_inmueble`
--

LOCK TABLES `minuta_c_inmueble` WRITE;
/*!40000 ALTER TABLE `minuta_c_inmueble` DISABLE KEYS */;
INSERT INTO `minuta_c_inmueble` VALUES (1,1,1,1,'Monto de Operacion: $2000000','Rojo Facundo vende a Soledad Aguilar',NULL,NULL,NULL,'2026-06-17 15:41:28',NULL,NULL),(2,1,1,1,'Monto de Operacion: $50000','Rojo Vende a Aguilar',NULL,NULL,NULL,'2026-06-17 15:42:41',NULL,NULL),(3,2,1,1,'Monto de Operacion: $500000','',NULL,NULL,NULL,'2026-06-18 00:51:03',NULL,NULL),(4,1,1,1,'Monto de Operacion: $600000','ufvhghggh',NULL,NULL,NULL,'2026-07-28 20:11:43',NULL,NULL),(5,2,1,1,'Monto de Operacion: $600000','fffffffffffffffffffffffffffff',NULL,NULL,NULL,'2026-07-28 21:23:22',NULL,NULL),(6,1,1,1,'Monto de Operacion: $25555','probando',NULL,NULL,NULL,'2026-08-20 12:19:39',NULL,NULL),(7,1,1,1,'Monto de Operacion: $4555555','probando',NULL,NULL,NULL,'2026-08-20 12:21:08',NULL,NULL),(8,2,1,1,'Monto de Operacion: $3222323','probando',NULL,NULL,NULL,'2026-08-20 12:23:16',NULL,NULL),(9,1,1,1,'Monto de Operacion: $7845248','probando',NULL,NULL,NULL,'2026-08-20 13:00:24',NULL,NULL),(10,4,1,1,'Monto de Operacion: $47888888','probando para ver la propiedad horizontal',NULL,NULL,NULL,'2026-08-20 13:06:32',NULL,NULL),(11,4,1,1,'Monto de Operacion: $78787878','probando otra ves la propiedad horizontal',NULL,NULL,NULL,'2026-08-20 13:13:11',NULL,NULL),(12,2,1,1,'Monto de Operacion: $5010000','asddadas',NULL,NULL,NULL,'2026-08-26 14:26:02',NULL,NULL),(13,4,1,1,'Monto de Operacion: $78999','prueba con el agregado de datos de conyugue esta vez el cliente es soltero',NULL,NULL,NULL,'2026-08-26 15:03:19',NULL,NULL),(14,1,1,1,'Monto de Operacion: $779888888|','prueba con datos de cliente siendo casado y agregando datos de conyuge',NULL,NULL,NULL,'2026-08-26 15:06:39',NULL,NULL),(15,2,1,1,'Monto de Operacion: $456987','Prueba 2 de generaciion de pdf con datos de conyuge',NULL,NULL,NULL,'2026-08-26 15:18:40',NULL,NULL),(16,4,1,1,'Monto de Operacion: $75000000','prueba',NULL,NULL,NULL,'2026-08-27 01:29:14',NULL,NULL),(17,2,1,1,'Monto de Operacion: $22222','prueba de nueva opcion de tipo de acto',NULL,NULL,NULL,'2026-08-27 15:45:48',NULL,'Donacion'),(18,2,1,1,'Monto de Operacion: $0','sadasdsada',NULL,NULL,NULL,'2026-08-27 15:56:15',NULL,'Donacion'),(19,1,1,1,'Monto de Operacion: $2222','',NULL,NULL,NULL,'2026-08-28 12:41:38',NULL,'Compraventa'),(20,2,1,1,'Monto de Operacion: $0','prueba para probar el tipo de acto',NULL,NULL,NULL,'2026-08-28 13:00:10',NULL,'Donacion'),(21,2,1,1,'Monto de Operacion: $0','',NULL,NULL,NULL,'2026-08-28 13:00:36',NULL,'Donacion'),(22,3,1,1,'Monto de Operacion: $0','otra prueba para ver los tipos de actos',NULL,NULL,NULL,'2026-08-28 13:10:20',NULL,'Donacion'),(23,1,1,1,'Monto de Operacion: $0','prueba nueva con especie de derechos',NULL,NULL,NULL,'2026-08-28 13:54:17',NULL,'Donacion'),(24,1,1,1,'Monto de Operacion: $NO CORRESPONDE','prueba de especie de derechos para ver qe sale en monto operacion',NULL,NULL,NULL,'2026-08-28 14:04:13',NULL,'Compraventa'),(25,1,1,1,'Monto de Operacion: $0','prueba para ver que sale sino no lleno monto de operacion',NULL,NULL,NULL,'2026-08-28 14:09:35',NULL,'Sesion de Derechos'),(26,4,1,1,'Monto de Operacion: $0','PRueba para que se vea los datos del escribano',NULL,NULL,NULL,'2026-08-28 15:15:22',NULL,'donacion'),(27,4,1,1,'Monto de Operacion: $0','prueba de para ver si se muestran los datos del escribano',NULL,NULL,NULL,'2026-08-28 15:31:49',NULL,'Donacion'),(28,2,1,1,'Monto de Operacion: $2322323','Prueba para ver que no se repitan los bloques 8 y 10',NULL,NULL,NULL,'2026-08-28 15:35:46',NULL,'compraventa'),(29,5,1,1,'Monto de Operacion: $300000','Prueba para ver si salen todos los datos del inmbueble',NULL,NULL,NULL,'2026-09-01 14:32:27',NULL,'Compraventa'),(30,5,1,1,'Monto de Operacion: $2000000','Prueba de nuevo para ver si se ven todos los datos del inmbueble',NULL,NULL,NULL,'2026-09-01 14:44:54',NULL,'Compraventa'),(31,5,1,1,'Monto de Operacion: $20000000','Otra prueba paar ver si se ven los datos del inmueble',NULL,NULL,NULL,'2026-09-01 14:46:08',NULL,'Compraventa'),(32,5,1,1,'Monto de Operacion: $300000000','Prueba otra ves para ver que se muestren los datos del inmueble',NULL,NULL,NULL,'2026-09-01 15:14:02',NULL,'Compraventa'),(33,6,1,1,'Monto de Operacion: $20000','prueba de datos para ver uqe salgan todos los datos del inmueble',NULL,NULL,NULL,'2026-09-01 21:58:46',NULL,'Compraventa'),(34,6,1,1,'Monto de Operacion: $500000','otra prueba para que  se muestren los datos del inmbueble',NULL,NULL,NULL,'2026-09-01 22:02:35',NULL,'Compraventa'),(35,7,1,1,'Monto de Operacion: $30000','Otra Prueba',NULL,NULL,NULL,'2026-09-01 22:03:53',NULL,'Compraventa'),(36,7,1,1,'Monto de Operacion: $0','Prueba',NULL,NULL,NULL,'2026-09-01 22:12:34',NULL,'Donacion'),(37,8,1,1,'Monto de Operacion: $200000','Otra Prueba',NULL,NULL,NULL,'2026-09-01 22:15:13',NULL,'Compraventa'),(38,8,1,1,'Monto de Operacion: $200000','otra prueba para hacer que se vean los datos del inmueble',NULL,NULL,NULL,'2026-09-01 22:24:44',NULL,'Compraventa'),(39,9,1,1,'Monto de Operacion: $3000','otra prueba',NULL,NULL,NULL,'2026-09-01 22:27:16',NULL,'Compraventa'),(40,4,1,1,'Monto de Operacion: $0','prueba de ultimas modificaciones',NULL,NULL,NULL,'2026-09-21 21:29:14',NULL,'Donacion'),(41,4,1,1,'Monto de Operacion: $0','otra prueba',NULL,NULL,NULL,'2026-09-21 21:36:39',NULL,'Donacion'),(42,8,1,1,'Monto de Operacion: $500000','otra prueba',NULL,NULL,NULL,'2026-09-21 21:45:21',NULL,'Compra Venta'),(43,10,1,1,'Monto de Operacion: $0','prueba de muestreo de datos',NULL,NULL,NULL,'2026-09-21 21:51:47',NULL,'Donacion'),(44,10,1,1,'Monto de Operacion: $8000000','prueba para ver nupcias',NULL,NULL,NULL,'2026-09-22 00:13:25',NULL,'Compra Venta'),(45,10,1,1,'Monto de Operacion: $8000000','prueba',NULL,NULL,NULL,'2026-09-22 01:39:01',NULL,'Compra Venta'),(46,11,1,1,'Monto de Operacion: $800000','prueba de funcionamiento de modulacion',NULL,NULL,NULL,'2026-09-23 13:00:20',NULL,'Compra Venta'),(47,11,1,1,'Monto de Operacion: $0','prueba para saber como queda ya todo',NULL,NULL,NULL,'2026-09-23 14:32:59',NULL,'Donacion'),(48,10,1,1,'Monto de Operacion: $255555','ghfghfgh',NULL,NULL,NULL,'2026-09-24 15:16:17',NULL,'compra venta'),(49,11,1,1,'Monto de Operacion: $450000','prueba de nombre de minuta',NULL,NULL,NULL,'2026-09-25 12:52:37',NULL,'Compra venta');
/*!40000 ALTER TABLE `minuta_c_inmueble` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `minuta_personas`
--

DROP TABLE IF EXISTS `minuta_personas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `minuta_personas` (
  `id_minuta` int NOT NULL,
  `id_persona` int NOT NULL,
  `rol` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `proporcion` varchar(20) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_minuta`,`id_persona`,`rol`),
  KEY `id_persona` (`id_persona`),
  CONSTRAINT `minuta_personas_ibfk_1` FOREIGN KEY (`id_minuta`) REFERENCES `minuta_c_inmueble` (`id_minuta`) ON DELETE CASCADE,
  CONSTRAINT `minuta_personas_ibfk_2` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id_persona`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `minuta_personas`
--

LOCK TABLES `minuta_personas` WRITE;
/*!40000 ALTER TABLE `minuta_personas` DISABLE KEYS */;
/*!40000 ALTER TABLE `minuta_personas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perfil_escribano`
--

DROP TABLE IF EXISTS `perfil_escribano`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `perfil_escribano` (
  `id` int NOT NULL,
  `nombre_completo` varchar(200) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `matricula` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `numero_registro` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perfil_escribano`
--

LOCK TABLES `perfil_escribano` WRITE;
/*!40000 ALTER TABLE `perfil_escribano` DISABLE KEYS */;
INSERT INTO `perfil_escribano` VALUES (1,'Rojo Facundo Nicolas','33422','1');
/*!40000 ALTER TABLE `perfil_escribano` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personas`
--

DROP TABLE IF EXISTS `personas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personas` (
  `id_persona` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `dni` varchar(15) COLLATE utf8mb4_spanish_ci NOT NULL,
  `cuil` varchar(15) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `domicilio` varchar(200) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `localidad` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `provincia` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT 'La Rioja',
  `telefono` varchar(30) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `estado_civil` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `nombre_conyuge` varchar(255) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `nupcias` varchar(10) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_persona`),
  UNIQUE KEY `dni` (`dni`),
  UNIQUE KEY `cuil` (`cuil`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personas`
--

LOCK TABLES `personas` WRITE;
/*!40000 ALTER TABLE `personas` DISABLE KEYS */;
INSERT INTO `personas` VALUES (1,'Facundo','Rojo','12345678','20123456789','2000-01-01',NULL,'La Rioja','La Rioja',NULL,NULL,NULL,NULL,NULL),(2,'Soledad','Aguilar','28087588','29280875889',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'Silvia','Barros','22135006','20221350060','1971-03-01','Cleofe Arias 158','La Rioja','La Rioja','3804248432','silviabeatriz310@hotmail.com',NULL,NULL,NULL),(4,'Claudio','Rivadera','25425078',NULL,NULL,'Los Cedros 29 Barrio Los Olmos',NULL,'La Rioja',NULL,NULL,'Soltero/a',NULL,NULL),(5,'Julieta','Granillo','10203040',NULL,NULL,'Barrio Jardin Norte',NULL,'La Rioja',NULL,NULL,'Casado/a','Bradd Pitt Dni 123456789',NULL),(6,'Facundo Nicolas','Rojo','39701343',NULL,NULL,'Parco Parisi 158',NULL,'La Rioja',NULL,NULL,'Casado/a','Olsen Elizabeth DNI: 123456; Clark Emilia DNI 654321','2da'),(7,'Pedro Nicolas','Rojo','22714034',NULL,NULL,'Parco Parisi 158',NULL,'La Rioja',NULL,NULL,'Casado/a','SIlvia Barros Depetris DNI: 22135006','1era'),(8,'Gabriela Ramona','Fuentes','33399774',NULL,NULL,'B° Parque Industrial',NULL,'La Rioja',NULL,NULL,'Soltero/a',NULL,NULL);
/*!40000 ALTER TABLE `personas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_persona` int NOT NULL,
  `usuario` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_spanish_ci NOT NULL,
  `rol` varchar(30) COLLATE utf8mb4_spanish_ci NOT NULL DEFAULT 'empleado',
  `matricula` varchar(30) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `registro_notarial` varchar(50) COLLATE utf8mb4_spanish_ci DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `id_persona` (`id_persona`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_persona`) REFERENCES `personas` (`id_persona`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,1,'facundo_rojo','admin123','Escribano',NULL,NULL,'2026-04-27 23:57:58','2026-04-27 23:57:58');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-25 11:19:51
