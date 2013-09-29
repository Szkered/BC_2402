-- phpMyAdmin SQL Dump
-- version 3.5.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 29, 2013 at 02:10 PM
-- Server version: 5.5.29
-- PHP Version: 5.4.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Create database
--

CREATE DATABASE sydb;
USE sydb;

--
-- Database: `sydb`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=43 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add stock', 1, 'add_stock'),
(2, 'Can change stock', 1, 'change_stock'),
(3, 'Can delete stock', 1, 'delete_stock'),
(4, 'Can add destination', 2, 'add_destination'),
(5, 'Can change destination', 2, 'change_destination'),
(6, 'Can delete destination', 2, 'delete_destination'),
(7, 'Can add donor', 3, 'add_donor'),
(8, 'Can change donor', 3, 'change_donor'),
(9, 'Can delete donor', 3, 'delete_donor'),
(10, 'Can add vendor', 4, 'add_vendor'),
(11, 'Can change vendor', 4, 'change_vendor'),
(12, 'Can delete vendor', 4, 'delete_vendor'),
(13, 'Can add distribute', 5, 'add_distribute'),
(14, 'Can change distribute', 5, 'change_distribute'),
(15, 'Can delete distribute', 5, 'delete_distribute'),
(16, 'Can add transfer', 6, 'add_transfer'),
(17, 'Can change transfer', 6, 'change_transfer'),
(18, 'Can delete transfer', 6, 'delete_transfer'),
(19, 'Can add donate', 7, 'add_donate'),
(20, 'Can change donate', 7, 'change_donate'),
(21, 'Can delete donate', 7, 'delete_donate'),
(22, 'Can add purchase', 8, 'add_purchase'),
(23, 'Can change purchase', 8, 'change_purchase'),
(24, 'Can delete purchase', 8, 'delete_purchase'),
(25, 'Can add permission', 9, 'add_permission'),
(26, 'Can change permission', 9, 'change_permission'),
(27, 'Can delete permission', 9, 'delete_permission'),
(28, 'Can add group', 10, 'add_group'),
(29, 'Can change group', 10, 'change_group'),
(30, 'Can delete group', 10, 'delete_group'),
(31, 'Can add user', 11, 'add_user'),
(32, 'Can change user', 11, 'change_user'),
(33, 'Can delete user', 11, 'delete_user'),
(34, 'Can add content type', 12, 'add_contenttype'),
(35, 'Can change content type', 12, 'change_contenttype'),
(36, 'Can delete content type', 12, 'delete_contenttype'),
(37, 'Can add session', 13, 'add_session'),
(38, 'Can change session', 13, 'change_session'),
(39, 'Can delete session', 13, 'delete_session'),
(40, 'Can add log entry', 14, 'add_logentry'),
(41, 'Can change log entry', 14, 'change_logentry'),
(42, 'Can delete log entry', 14, 'delete_logentry');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$10000$fuZSayqFX6mf$dLAeMWVZDY/eMQF8id51fLb2WTGIqqK3F9GYE7R3wbM=', '2013-09-29 10:18:20', 1, 'admin', '', '', '', 1, 1, '2013-09-29 09:47:53');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'stock', 'stocks', 'stock'),
(2, 'destination', 'stocks', 'destination'),
(3, 'donor', 'stocks', 'donor'),
(4, 'vendor', 'stocks', 'vendor'),
(5, 'distribute', 'stocks', 'distribute'),
(6, 'transfer', 'stocks', 'transfer'),
(7, 'donate', 'stocks', 'donate'),
(8, 'purchase', 'stocks', 'purchase'),
(9, 'permission', 'auth', 'permission'),
(10, 'group', 'auth', 'group'),
(11, 'user', 'auth', 'user'),
(12, 'content type', 'contenttypes', 'contenttype'),
(13, 'session', 'sessions', 'session'),
(14, 'log entry', 'admin', 'logentry');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0ehe9vxzwdijax9dx1ha2h3rvyyk7qvg', 'NTM0NzBkYmQ3NDE0NjlmOTBkOGFmMTMzMDdkN2FmZTUzYzM5NWZjNDp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2013-10-13 10:18:20');

-- --------------------------------------------------------

--
-- Table structure for table `stocks_destination`
--

CREATE TABLE `stocks_destination` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `person_in_charge` varchar(30) NOT NULL,
  `contact_no` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `stocks_distribute`
--

CREATE TABLE `stocks_distribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `quantity` int(11) NOT NULL,
  `stock_id` int(11) NOT NULL,
  `family_type` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stocks_distribute_80945c99` (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `stocks_donate`
--

CREATE TABLE `stocks_donate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `quantity` int(11) NOT NULL,
  `stock_id` int(11) NOT NULL,
  `donor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stocks_donate_80945c99` (`stock_id`),
  KEY `stocks_donate_e7ca2598` (`donor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `stocks_donor`
--

CREATE TABLE `stocks_donor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `address` varchar(100) NOT NULL,
  `contact_no` int(11) NOT NULL,
  `mailing` tinyint(1) NOT NULL,
  `referral` varchar(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `stocks_purchase`
--

CREATE TABLE `stocks_purchase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `quantity` int(11) NOT NULL,
  `stock_id` int(11) NOT NULL,
  `vendor_id` int(11) NOT NULL,
  `confirm` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stocks_purchase_80945c99` (`stock_id`),
  KEY `stocks_purchase_bc787c37` (`vendor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `stocks_stock`
--

CREATE TABLE `stocks_stock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(50) NOT NULL,
  `unit_measure` varchar(10) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `purchase_sum` decimal(10,2) NOT NULL,
  `donate_sum` decimal(10,2) NOT NULL,
  `transfer_sum` decimal(10,2) NOT NULL,
  `distribute_sum` decimal(10,2) NOT NULL,
  `category` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `stocks_transfer`
--

CREATE TABLE `stocks_transfer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `quantity` int(11) NOT NULL,
  `stock_id` int(11) NOT NULL,
  `destination_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stocks_transfer_80945c99` (`stock_id`),
  KEY `stocks_transfer_ccdfa9a7` (`destination_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `stocks_vendor`
--

CREATE TABLE `stocks_vendor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `address` varchar(100) NOT NULL,
  `contact_no` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `stocks_distribute`
--
ALTER TABLE `stocks_distribute`
  ADD CONSTRAINT `stock_id_refs_id_7b2d92ff` FOREIGN KEY (`stock_id`) REFERENCES `stocks_stock` (`id`);

--
-- Constraints for table `stocks_donate`
--
ALTER TABLE `stocks_donate`
  ADD CONSTRAINT `stock_id_refs_id_be2a0a9f` FOREIGN KEY (`stock_id`) REFERENCES `stocks_stock` (`id`),
  ADD CONSTRAINT `donor_id_refs_id_1cc7e84a` FOREIGN KEY (`donor_id`) REFERENCES `stocks_donor` (`id`);

--
-- Constraints for table `stocks_purchase`
--
ALTER TABLE `stocks_purchase`
  ADD CONSTRAINT `stock_id_refs_id_3cca35a7` FOREIGN KEY (`stock_id`) REFERENCES `stocks_stock` (`id`),
  ADD CONSTRAINT `vendor_id_refs_id_d401622a` FOREIGN KEY (`vendor_id`) REFERENCES `stocks_vendor` (`id`);

--
-- Constraints for table `stocks_transfer`
--
ALTER TABLE `stocks_transfer`
  ADD CONSTRAINT `destination_id_refs_id_0cba2179` FOREIGN KEY (`destination_id`) REFERENCES `stocks_destination` (`id`),
  ADD CONSTRAINT `stock_id_refs_id_6ab26ec1` FOREIGN KEY (`stock_id`) REFERENCES `stocks_stock` (`id`);
