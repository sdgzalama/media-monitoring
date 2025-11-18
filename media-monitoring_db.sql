-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 16, 2025 at 10:03 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `media-monitoring_db`
--

DELIMITER $$
--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `uuid_v4` () RETURNS CHAR(36) CHARSET utf8mb4 COLLATE utf8mb4_general_ci DETERMINISTIC RETURN (SELECT UUID())$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact_email` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`id`, `name`, `contact_email`, `created_at`) VALUES
('02056b59-71ae-429a-b0af-f640876787d5', 'sidaga and monica loce', 'monisida@gmail.com', '2025-11-15 17:01:01'),
('27b79492-25bc-45f1-8d8c-8d56a0ca6d6c', 'hamasa media group', 'hamasa@gmail.com', '2025-11-15 13:59:57'),
('3e1eab0d-3823-4a2e-ab9f-d31f9520e6ee', 'TAWLA', 'info@tawla.or.tz', '2025-11-15 11:19:28'),
('d0339e8b-c928-456c-9843-a2eb60053608', 'hamasa media group', 'hamasa@gmail.com', '2025-11-15 13:59:55'),
('d3e36642-dfe1-404f-a31b-b87020aaf6c2', 'string', 'user@example.com', '2025-11-15 19:45:36'),
('d65f5524-991f-4a27-a16d-35f89ea72528', 'SHEIN WAZIRI', 'waziri@gmail.com', '2025-11-16 08:49:55');

-- --------------------------------------------------------

--
-- Table structure for table `collaborators`
--

CREATE TABLE `collaborators` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `media_items`
--

CREATE TABLE `media_items` (
  `id` char(36) NOT NULL,
  `project_id` char(36) NOT NULL,
  `source_id` char(36) NOT NULL,
  `raw_title` text DEFAULT NULL,
  `raw_text` longtext DEFAULT NULL,
  `url` text DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  `scraped_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `industry_name` text DEFAULT NULL,
  `industry_tactic` text DEFAULT NULL,
  `stakeholders` text DEFAULT NULL,
  `targeted_policy` text DEFAULT NULL,
  `geographical_focus` text DEFAULT NULL,
  `outcome_impact` text DEFAULT NULL,
  `semantic_area_ids` text DEFAULT NULL,
  `analysis_status` enum('raw','extracted','error') DEFAULT 'raw'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `media_sources`
--

CREATE TABLE `media_sources` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` enum('news','blog','social','gov','tv_radio') NOT NULL,
  `base_url` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `media_sources`
--

INSERT INTO `media_sources` (`id`, `name`, `type`, `base_url`) VALUES
('d1abc3d9-ea9c-496d-9039-292ae98e0022', 'BBC', 'news', 'https://feeds.bbci.co.uk/swahili/rss.xml');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `id` char(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `client_id` char(36) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project_categories`
--

CREATE TABLE `project_categories` (
  `project_id` char(36) NOT NULL,
  `category_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project_collaborators`
--

CREATE TABLE `project_collaborators` (
  `project_id` char(36) NOT NULL,
  `collaborator_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project_media_sources`
--

CREATE TABLE `project_media_sources` (
  `project_id` char(36) NOT NULL,
  `media_source_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project_report_avenues`
--

CREATE TABLE `project_report_avenues` (
  `project_id` char(36) NOT NULL,
  `report_avenue_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project_report_consultations`
--

CREATE TABLE `project_report_consultations` (
  `project_id` char(36) NOT NULL,
  `report_consultation_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project_report_times`
--

CREATE TABLE `project_report_times` (
  `project_id` char(36) NOT NULL,
  `report_time_id` char(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `report_avenues`
--

CREATE TABLE `report_avenues` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `report_consultations`
--

CREATE TABLE `report_consultations` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `report_times`
--

CREATE TABLE `report_times` (
  `id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `thematic_areas`
--

CREATE TABLE `thematic_areas` (
  `id` char(36) NOT NULL,
  `project_id` char(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `collaborators`
--
ALTER TABLE `collaborators`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `media_items`
--
ALTER TABLE `media_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `url` (`url`) USING HASH,
  ADD KEY `project_id` (`project_id`),
  ADD KEY `source_id` (`source_id`);

--
-- Indexes for table `media_sources`
--
ALTER TABLE `media_sources`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `project_categories`
--
ALTER TABLE `project_categories`
  ADD PRIMARY KEY (`project_id`,`category_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `project_collaborators`
--
ALTER TABLE `project_collaborators`
  ADD PRIMARY KEY (`project_id`,`collaborator_id`),
  ADD KEY `collaborator_id` (`collaborator_id`);

--
-- Indexes for table `project_media_sources`
--
ALTER TABLE `project_media_sources`
  ADD PRIMARY KEY (`project_id`,`media_source_id`),
  ADD KEY `media_source_id` (`media_source_id`);

--
-- Indexes for table `project_report_avenues`
--
ALTER TABLE `project_report_avenues`
  ADD PRIMARY KEY (`project_id`,`report_avenue_id`),
  ADD KEY `report_avenue_id` (`report_avenue_id`);

--
-- Indexes for table `project_report_consultations`
--
ALTER TABLE `project_report_consultations`
  ADD PRIMARY KEY (`project_id`,`report_consultation_id`),
  ADD KEY `report_consultation_id` (`report_consultation_id`);

--
-- Indexes for table `project_report_times`
--
ALTER TABLE `project_report_times`
  ADD PRIMARY KEY (`project_id`,`report_time_id`),
  ADD KEY `report_time_id` (`report_time_id`);

--
-- Indexes for table `report_avenues`
--
ALTER TABLE `report_avenues`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `report_consultations`
--
ALTER TABLE `report_consultations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `report_times`
--
ALTER TABLE `report_times`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `thematic_areas`
--
ALTER TABLE `thematic_areas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_id` (`project_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `media_items`
--
ALTER TABLE `media_items`
  ADD CONSTRAINT `media_items_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `media_items_ibfk_2` FOREIGN KEY (`source_id`) REFERENCES `media_sources` (`id`);

--
-- Constraints for table `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`id`);

--
-- Constraints for table `project_categories`
--
ALTER TABLE `project_categories`
  ADD CONSTRAINT `project_categories_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `project_categories_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

--
-- Constraints for table `project_collaborators`
--
ALTER TABLE `project_collaborators`
  ADD CONSTRAINT `project_collaborators_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `project_collaborators_ibfk_2` FOREIGN KEY (`collaborator_id`) REFERENCES `collaborators` (`id`);

--
-- Constraints for table `project_media_sources`
--
ALTER TABLE `project_media_sources`
  ADD CONSTRAINT `project_media_sources_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `project_media_sources_ibfk_2` FOREIGN KEY (`media_source_id`) REFERENCES `media_sources` (`id`);

--
-- Constraints for table `project_report_avenues`
--
ALTER TABLE `project_report_avenues`
  ADD CONSTRAINT `project_report_avenues_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `project_report_avenues_ibfk_2` FOREIGN KEY (`report_avenue_id`) REFERENCES `report_avenues` (`id`);

--
-- Constraints for table `project_report_consultations`
--
ALTER TABLE `project_report_consultations`
  ADD CONSTRAINT `project_report_consultations_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `project_report_consultations_ibfk_2` FOREIGN KEY (`report_consultation_id`) REFERENCES `report_consultations` (`id`);

--
-- Constraints for table `project_report_times`
--
ALTER TABLE `project_report_times`
  ADD CONSTRAINT `project_report_times_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `project_report_times_ibfk_2` FOREIGN KEY (`report_time_id`) REFERENCES `report_times` (`id`);

--
-- Constraints for table `thematic_areas`
--
ALTER TABLE `thematic_areas`
  ADD CONSTRAINT `thematic_areas_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
