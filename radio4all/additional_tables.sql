CREATE DATABASE  IF NOT EXISTS `rp` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `rp`;
-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
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
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
INSERT INTO `account_emailaddress` VALUES (1,'admin@radio4all.net',0,0,1);
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add permission',3,'add_permission'),(10,'Can change permission',3,'change_permission'),(11,'Can delete permission',3,'delete_permission'),(12,'Can view permission',3,'view_permission'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add site',7,'add_site'),(26,'Can change site',7,'change_site'),(27,'Can delete site',7,'delete_site'),(28,'Can view site',7,'view_site'),(29,'Can add email address',8,'add_emailaddress'),(30,'Can change email address',8,'change_emailaddress'),(31,'Can delete email address',8,'delete_emailaddress'),(32,'Can view email address',8,'view_emailaddress'),(33,'Can add email confirmation',9,'add_emailconfirmation'),(34,'Can change email confirmation',9,'change_emailconfirmation'),(35,'Can delete email confirmation',9,'delete_emailconfirmation'),(36,'Can view email confirmation',9,'view_emailconfirmation'),(37,'Can add social account',10,'add_socialaccount'),(38,'Can change social account',10,'change_socialaccount'),(39,'Can delete social account',10,'delete_socialaccount'),(40,'Can view social account',10,'view_socialaccount'),(41,'Can add social application token',11,'add_socialtoken'),(42,'Can change social application token',11,'change_socialtoken'),(43,'Can delete social application token',11,'delete_socialtoken'),(44,'Can view social application token',11,'view_socialtoken'),(45,'Can add social application',12,'add_socialapp'),(46,'Can change social application',12,'change_socialapp'),(47,'Can delete social application',12,'delete_socialapp'),(48,'Can view social application',12,'view_socialapp'),(49,'Can add open id store',13,'add_openidstore'),(50,'Can change open id store',13,'change_openidstore'),(51,'Can delete open id store',13,'delete_openidstore'),(52,'Can view open id store',13,'view_openidstore'),(53,'Can add open id nonce',14,'add_openidnonce'),(54,'Can change open id nonce',14,'change_openidnonce'),(55,'Can delete open id nonce',14,'delete_openidnonce'),(56,'Can view open id nonce',14,'view_openidnonce'),(57,'Can add advisories',15,'add_advisories'),(58,'Can change advisories',15,'change_advisories'),(59,'Can delete advisories',15,'delete_advisories'),(60,'Can view advisories',15,'view_advisories'),(61,'Can add application key',16,'add_applicationkey'),(62,'Can change application key',16,'change_applicationkey'),(63,'Can delete application key',16,'delete_applicationkey'),(64,'Can view application key',16,'view_applicationkey'),(65,'Can add captcha',17,'add_captcha'),(66,'Can change captcha',17,'change_captcha'),(67,'Can delete captcha',17,'delete_captcha'),(68,'Can view captcha',17,'view_captcha'),(69,'Can add faq',18,'add_faq'),(70,'Can change faq',18,'change_faq'),(71,'Can delete faq',18,'delete_faq'),(72,'Can view faq',18,'view_faq'),(73,'Can add files',19,'add_files'),(74,'Can change files',19,'change_files'),(75,'Can delete files',19,'delete_files'),(76,'Can view files',19,'view_files'),(77,'Can add formats',20,'add_formats'),(78,'Can change formats',20,'change_formats'),(79,'Can delete formats',20,'delete_formats'),(80,'Can view formats',20,'view_formats'),(81,'Can add lang',21,'add_lang'),(82,'Can change lang',21,'change_lang'),(83,'Can delete lang',21,'delete_lang'),(84,'Can view lang',21,'view_lang'),(85,'Can add license',22,'add_license'),(86,'Can change license',22,'change_license'),(87,'Can delete license',22,'delete_license'),(88,'Can view license',22,'view_license'),(89,'Can add locations',23,'add_locations'),(90,'Can change locations',23,'change_locations'),(91,'Can delete locations',23,'delete_locations'),(92,'Can view locations',23,'view_locations'),(93,'Can add news',24,'add_news'),(94,'Can change news',24,'change_news'),(95,'Can delete news',24,'delete_news'),(96,'Can view news',24,'view_news'),(97,'Can add programs',25,'add_programs'),(98,'Can change programs',25,'change_programs'),(99,'Can delete programs',25,'delete_programs'),(100,'Can view programs',25,'view_programs'),(101,'Can add restrictions',26,'add_restrictions'),(102,'Can change restrictions',26,'change_restrictions'),(103,'Can delete restrictions',26,'delete_restrictions'),(104,'Can view restrictions',26,'view_restrictions'),(105,'Can add sessions',27,'add_sessions'),(106,'Can change sessions',27,'change_sessions'),(107,'Can delete sessions',27,'delete_sessions'),(108,'Can view sessions',27,'view_sessions'),(109,'Can add topic assignment',28,'add_topicassignment'),(110,'Can change topic assignment',28,'change_topicassignment'),(111,'Can delete topic assignment',28,'delete_topicassignment'),(112,'Can view topic assignment',28,'view_topicassignment'),(113,'Can add topics',29,'add_topics'),(114,'Can change topics',29,'change_topics'),(115,'Can delete topics',29,'delete_topics'),(116,'Can view topics',29,'view_topics'),(117,'Can add types',30,'add_types'),(118,'Can change types',30,'change_types'),(119,'Can delete types',30,'delete_types'),(120,'Can view types',30,'view_types'),(121,'Can add users',31,'add_users'),(122,'Can change users',31,'change_users'),(123,'Can delete users',31,'delete_users'),(124,'Can view users',31,'view_users'),(125,'Can add versions',32,'add_versions'),(126,'Can change versions',32,'change_versions'),(127,'Can delete versions',32,'delete_versions'),(128,'Can view versions',32,'view_versions');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$120000$KkkjDz1nizna$7D0VWTt6JQ02mMlu73NUyc1P5hO4L0Qka8DVrg+RWhM=','2018-12-05 01:05:04.729015',1,'admin','','','admin@radio4all.net',1,1,'2018-12-05 01:04:41.237881');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'account','emailaddress'),(9,'account','emailconfirmation'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(14,'openid','openidnonce'),(13,'openid','openidstore'),(15,'radio4all','advisories'),(16,'radio4all','applicationkey'),(17,'radio4all','captcha'),(18,'radio4all','faq'),(19,'radio4all','files'),(20,'radio4all','formats'),(21,'radio4all','lang'),(22,'radio4all','license'),(23,'radio4all','locations'),(24,'radio4all','news'),(25,'radio4all','programs'),(26,'radio4all','restrictions'),(27,'radio4all','sessions'),(28,'radio4all','topicassignment'),(29,'radio4all','topics'),(30,'radio4all','types'),(31,'radio4all','users'),(32,'radio4all','versions'),(6,'sessions','session'),(7,'sites','site'),(10,'socialaccount','socialaccount'),(12,'socialaccount','socialapp'),(11,'socialaccount','socialtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-12-04 21:13:54.594238'),(2,'auth','0001_initial','2018-12-04 21:13:54.884983'),(3,'admin','0001_initial','2018-12-04 21:13:54.953753'),(4,'admin','0002_logentry_remove_auto_add','2018-12-04 21:13:54.963360'),(5,'admin','0003_logentry_add_action_flag_choices','2018-12-04 21:13:54.973138'),(6,'contenttypes','0002_remove_content_type_name','2018-12-04 21:13:55.040218'),(7,'auth','0002_alter_permission_name_max_length','2018-12-04 21:13:55.052186'),(8,'auth','0003_alter_user_email_max_length','2018-12-04 21:13:55.067641'),(9,'auth','0004_alter_user_username_opts','2018-12-04 21:13:55.078502'),(10,'auth','0005_alter_user_last_login_null','2018-12-04 21:13:55.098912'),(11,'auth','0006_require_contenttypes_0002','2018-12-04 21:13:55.101171'),(12,'auth','0007_alter_validators_add_error_messages','2018-12-04 21:13:55.110883'),(13,'auth','0008_alter_user_username_max_length','2018-12-04 21:13:55.135812'),(14,'auth','0009_alter_user_last_name_max_length','2018-12-04 21:13:55.152059'),(15,'sessions','0001_initial','2018-12-04 21:13:55.180548'),(16,'account','0001_initial','2018-12-12 19:51:47.204829'),(17,'account','0002_email_max_length','2018-12-12 19:51:47.241690'),(18,'openid','0001_initial','2018-12-12 19:51:47.305487'),(19,'sites','0001_initial','2018-12-12 19:51:47.336186'),(20,'sites','0002_alter_domain_unique','2018-12-12 19:51:47.355861'),(21,'socialaccount','0001_initial','2018-12-12 19:51:47.587778'),(22,'socialaccount','0002_token_max_lengths','2018-12-12 19:51:47.637852'),(23,'socialaccount','0003_extra_data_default_dict','2018-12-12 19:51:47.649609');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('pl2ry1bb1zwl475eluwthvlveqs2sl7p','ZWM4MmYwM2ViNDVlNGVkNTVlYTc4MWUzZTdhNjAwYWVjMTA5MWU2Nzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJjMmQ5MzZlYTg4MGI2NzU2ZmU5YTY0NDFlZTNiODIyOTU0ZTg5OWEzIn0=','2018-12-19 01:05:04.733406');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `openid_openidnonce`
--

LOCK TABLES `openid_openidnonce` WRITE;
/*!40000 ALTER TABLE `openid_openidnonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `openid_openidnonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `openid_openidstore`
--

LOCK TABLES `openid_openidstore` WRITE;
/*!40000 ALTER TABLE `openid_openidstore` DISABLE KEYS */;
/*!40000 ALTER TABLE `openid_openidstore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-08  8:27:56
