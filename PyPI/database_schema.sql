-- phpMyAdmin SQL Dump
-- version 4.2.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 18. Jan 2015 um 20:13
-- Server Version: 5.5.40-0ubuntu1
-- PHP-Version: 5.5.12-2ubuntu4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Datenbank: `pypi`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `packages`
--

CREATE TABLE IF NOT EXISTS `packages` (
`id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_bin NOT NULL COMMENT 'Name of the package',
  `author` varchar(255) COLLATE utf8_bin NOT NULL,
  `author_email` varchar(255) COLLATE utf8_bin NOT NULL,
  `maintainer` varchar(255) COLLATE utf8_bin NOT NULL,
  `maintainer_email` varchar(255) COLLATE utf8_bin NOT NULL,
  `requires_python` varchar(255) COLLATE utf8_bin NOT NULL,
  `platform` varchar(255) COLLATE utf8_bin NOT NULL,
  `version` varchar(255) COLLATE utf8_bin NOT NULL,
  `license` varchar(255) COLLATE utf8_bin NOT NULL,
  `keywords` text COLLATE utf8_bin NOT NULL,
  `description` text COLLATE utf8_bin NOT NULL,
  `summary` varchar(255) COLLATE utf8_bin NOT NULL,
  `stable_version` varchar(255) COLLATE utf8_bin NOT NULL,
  `home_page` varchar(255) COLLATE utf8_bin NOT NULL,
  `release_url` varchar(255) COLLATE utf8_bin NOT NULL,
  `bugtrack_url` varchar(255) COLLATE utf8_bin NOT NULL,
  `download_url` varchar(255) COLLATE utf8_bin NOT NULL,
  `docs_url` varchar(255) COLLATE utf8_bin NOT NULL,
  `package_url` varchar(255) COLLATE utf8_bin NOT NULL,
  `_pypi_hidden` tinyint(1) NOT NULL,
  `_pypi_ordering` smallint(255) NOT NULL,
  `cheesecake_code_kwalitee_id` smallint(255) DEFAULT NULL,
  `cheesecake_documentation_id` smallint(255) DEFAULT NULL,
  `cheesecake_installability_id` smallint(255) DEFAULT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `package_classifiers`
--

CREATE TABLE IF NOT EXISTS `package_classifiers` (
`id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `classifier` varchar(255) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `releases`
--

CREATE TABLE IF NOT EXISTS `releases` (
`id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `release_number` varchar(255) COLLATE utf8_bin NOT NULL,
  `has_sig` tinyint(1) NOT NULL,
  `upload_time` varchar(255) COLLATE utf8_bin NOT NULL,
  `comment_text` varchar(255) COLLATE utf8_bin NOT NULL,
  `python_version` varchar(255) COLLATE utf8_bin NOT NULL,
  `url` varchar(255) COLLATE utf8_bin NOT NULL,
  `md5_digest` varchar(255) COLLATE utf8_bin NOT NULL,
  `downloads` int(255) NOT NULL,
  `filename` varchar(255) COLLATE utf8_bin NOT NULL,
  `packagetype` varchar(255) COLLATE utf8_bin NOT NULL,
  `size` int(255) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `urls`
--

CREATE TABLE IF NOT EXISTS `urls` (
`id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `has_sig` tinyint(1) NOT NULL,
  `upload_time` varchar(255) COLLATE utf8_bin NOT NULL,
  `comment_text` varchar(255) COLLATE utf8_bin NOT NULL,
  `python_version` varchar(255) COLLATE utf8_bin NOT NULL,
  `url` varchar(255) COLLATE utf8_bin NOT NULL,
  `md5_digest` varchar(255) COLLATE utf8_bin NOT NULL,
  `downloads` int(255) NOT NULL,
  `filename` varchar(255) COLLATE utf8_bin NOT NULL,
  `packagetype` varchar(255) COLLATE utf8_bin NOT NULL,
  `size` varchar(255) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;


-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `dependencies`
--

CREATE TABLE IF NOT EXISTS `dependencies` (
  `id` int(11) NOT NULL,
  `package` int(11) NOT NULL,
  `needs_package` int(11) NOT NULL,
  `req_type` enum('requirements.txt','imported') COLLATE utf8_bin NOT NULL,
  `times` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `dependencies`
--
ALTER TABLE `dependencies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `package` (`package`),
  ADD KEY `needs_package` (`needs_package`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `dependencies`
--
ALTER TABLE `dependencies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `packages`
--
ALTER TABLE `packages`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `package_classifiers`
--
ALTER TABLE `package_classifiers`
 ADD PRIMARY KEY (`id`), ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `releases`
--
ALTER TABLE `releases`
 ADD PRIMARY KEY (`id`), ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `urls`
--
ALTER TABLE `urls`
 ADD PRIMARY KEY (`id`), ADD KEY `package_id` (`package_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `packages`
--
ALTER TABLE `packages`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `package_classifiers`
--
ALTER TABLE `package_classifiers`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `releases`
--
ALTER TABLE `releases`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `urls`
--
ALTER TABLE `urls`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `package_classifiers`
--
ALTER TABLE `package_classifiers`
ADD CONSTRAINT `package_classifiers_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `releases`
--
ALTER TABLE `releases`
ADD CONSTRAINT `belongs_to_package` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints der Tabelle `urls`
--
ALTER TABLE `urls`
ADD CONSTRAINT `urls_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
