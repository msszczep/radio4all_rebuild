-- MySQL dump 10.13  Distrib 5.7.11, for osx10.11 (x86_64)
--
-- Host: localhost    Database: rp
-- ------------------------------------------------------
-- Server version	5.7.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-12-04 21:13:54.594238'),(2,'auth','0001_initial','2018-12-04 21:13:54.884983'),(3,'admin','0001_initial','2018-12-04 21:13:54.953753'),(4,'admin','0002_logentry_remove_auto_add','2018-12-04 21:13:54.963360'),(5,'admin','0003_logentry_add_action_flag_choices','2018-12-04 21:13:54.973138'),(6,'contenttypes','0002_remove_content_type_name','2018-12-04 21:13:55.040218'),(7,'auth','0002_alter_permission_name_max_length','2018-12-04 21:13:55.052186'),(8,'auth','0003_alter_user_email_max_length','2018-12-04 21:13:55.067641'),(9,'auth','0004_alter_user_username_opts','2018-12-04 21:13:55.078502'),(10,'auth','0005_alter_user_last_login_null','2018-12-04 21:13:55.098912'),(11,'auth','0006_require_contenttypes_0002','2018-12-04 21:13:55.101171'),(12,'auth','0007_alter_validators_add_error_messages','2018-12-04 21:13:55.110883'),(13,'auth','0008_alter_user_username_max_length','2018-12-04 21:13:55.135812'),(14,'auth','0009_alter_user_last_name_max_length','2018-12-04 21:13:55.152059'),(15,'sessions','0001_initial','2018-12-04 21:13:55.180548'),(16,'account','0001_initial','2018-12-12 19:51:47.204829'),(17,'account','0002_email_max_length','2018-12-12 19:51:47.241690'),(18,'openid','0001_initial','2018-12-12 19:51:47.305487'),(19,'sites','0001_initial','2018-12-12 19:51:47.336186'),(20,'sites','0002_alter_domain_unique','2018-12-12 19:51:47.355861'),(21,'socialaccount','0001_initial','2018-12-12 19:51:47.587778'),(22,'socialaccount','0002_token_max_lengths','2018-12-12 19:51:47.637852'),(23,'socialaccount','0003_extra_data_default_dict','2018-12-12 19:51:47.649609');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-12  8:36:50
