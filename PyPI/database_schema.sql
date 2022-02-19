--
-- Database: `PyPI`
--

-- --------------------------------------------------------

--
-- Table structure for table `dependencies`
--

CREATE TABLE IF NOT EXISTS `dependencies` (
  `id` int(11) NOT NULL,
  `package` int(11) NOT NULL,
  `needs_package` int(11) NOT NULL,
  `req_type` TEXT CHECK ( req_type in ('requirements.txt','imported','setup.py')) NOT NULL,
  `times` int(11) NOT NULL DEFAULT '0'
);

-- --------------------------------------------------------

--
-- Table structure for table `github`
--

CREATE TABLE IF NOT EXISTS `github` (
  `id` int(11) NOT NULL,
  `stargazers_count` int(11) NOT NULL DEFAULT '-1',
  `watchers_count` int(11) NOT NULL DEFAULT '-1',
  `forks_count` int(11) NOT NULL DEFAULT '-1'
);

-- --------------------------------------------------------

--
-- Table structure for table `packages`
--

CREATE TABLE IF NOT EXISTS `packages` (
  `id` int(11) NOT NULL,
  `on_pypi` tinyint(1) NOT NULL DEFAULT '1',
  `name` varchar(255) NOT NULL, --  COMMENT 'Name of the package'
  `author` varchar(255) NOT NULL,
  `author_email` varchar(255) NOT NULL,
  `maintainer` varchar(255) NOT NULL,
  `maintainer_email` varchar(255) NOT NULL,
  `requires_python` varchar(255) NOT NULL,
  `platform` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL,
  `license` varchar(255) NOT NULL,
  `keywords` text NOT NULL,
  `description` text NOT NULL,
  `summary` varchar(255) NOT NULL,
  `stable_version` varchar(255) NOT NULL,
  `home_page` varchar(255) NOT NULL,
  `release_url` varchar(255) NOT NULL,
  `bugtrack_url` varchar(255) NOT NULL,
  `download_url` varchar(255) NOT NULL,
  `docs_url` varchar(255) NOT NULL,
  `package_url` varchar(255) NOT NULL,
  `_pypi_hidden` tinyint(1) NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `package_classifiers`
--

CREATE TABLE IF NOT EXISTS `package_classifiers` (
  `id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `classifier` varchar(255) NOT NULL
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `package_github`
--
CREATE TABLE IF NOT EXISTS `package_github` (
`id` int(11)
,`name` varchar(255)
,`home_page` varchar(255)
,`stargazers_count` int(11)
,`watchers_count` int(11)
,`forks_count` int(11)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `package_names`
--
CREATE TABLE IF NOT EXISTS `package_names` (
`id` int(11)
,`name` varchar(255)
);

-- --------------------------------------------------------

--
-- Table structure for table `releases`
--

CREATE TABLE IF NOT EXISTS `releases` (
  `id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `release_number` varchar(255) NOT NULL,
  `has_sig` tinyint(1) NOT NULL,
  `upload_time` varchar(255) NOT NULL,
  `comment_text` varchar(255) NOT NULL,
  `python_version` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `md5_digest` varchar(255) NOT NULL,
  `downloads` int(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `packagetype` varchar(255) NOT NULL,
  `size` int(255) NOT NULL,
  `downloaded_bytes` int(255) NOT NULL DEFAULT '0'
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `small_dependencies`
--
CREATE TABLE IF NOT EXISTS `small_dependencies` (
`package` int(11)
,`needs_package` int(11)
,`times` int(11)
);

-- --------------------------------------------------------

--
-- Table structure for table `urls`
--

CREATE TABLE IF NOT EXISTS `urls` (
  `id` int(11) NOT NULL,
  `package_id` int(11) NOT NULL,
  `has_sig` tinyint(1) NOT NULL,
  `upload_time` varchar(255) NOT NULL,
  `comment_text` varchar(255) NOT NULL,
  `python_version` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `md5_digest` varchar(255) NOT NULL,
  `downloads` int(255) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `packagetype` varchar(255) NOT NULL,
  `size` varchar(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS `computed_values` (
  `package_id`  int(11) NOT NULL PRIMARY KEY,
  `latest_release_id` int(11) NULL,
  `unusable` tinyint(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS `package_files` (
  `id` int(11) NOT NULL PRIMARY KEY,
  `package_id`  int(11) NOT NULL,
  `release_id` int(11) NULL,
  `file_path` varchar(255) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_extension` varchar(255) NOT NULL,
  `lines` int(11) NOT NULL,
  `file_size` int(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS `package_file_lines` (
  `id` int(11) NOT NULL PRIMARY KEY,
  `package_id`  int(11) NOT NULL,
  `release_id` int(11) NULL,
  `package_file_id` int(11) NULL,
  `line_length` int(11) NOT NULL
);

-- --------------------------------------------------------

--
-- Structure for view `package_github`
--
DROP TABLE IF EXISTS `package_github`;

CREATE VIEW `package_github` AS select `packages`.`id` AS `id`,`packages`.`name` AS `name`,`packages`.`home_page` AS `home_page`,`github`.`stargazers_count` AS `stargazers_count`,`github`.`watchers_count` AS `watchers_count`,`github`.`forks_count` AS `forks_count` from (`packages` left join `github` on((`packages`.`id` = `github`.`id`))) where ((`packages`.`license` like '%MIT%') and (`packages`.`summary` <> '') and (`packages`.`home_page` like 'https://github.com/%') and (`github`.`stargazers_count` is not null)) order by `packages`.`name`;

-- --------------------------------------------------------

--
-- Structure for view `package_names`
--
DROP TABLE IF EXISTS `package_names`;

CREATE VIEW `package_names` AS select `packages`.`id` AS `id`,`packages`.`name` AS `name` from `packages` order by `packages`.`name`;

-- --------------------------------------------------------

--
-- Structure for view `small_dependencies`
--
DROP TABLE IF EXISTS `small_dependencies`;

CREATE VIEW `small_dependencies` AS select `dependencies`.`package` AS `package`,`dependencies`.`needs_package` AS `needs_package`,`dependencies`.`times` AS `times` from `dependencies`;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dependencies`
--
ALTER TABLE `dependencies`
  ADD KEY `id`,
  ADD UNIQUE KEY `no_multiedges` (`package`,`needs_package`),
  ADD KEY `package` (`package`),
  ADD KEY `needs_package` (`needs_package`);

--
-- Indexes for table `github`
--
ALTER TABLE `github`
  ADD KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `packages`
--
ALTER TABLE `packages`
  ADD KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `package_classifiers`
--
ALTER TABLE `package_classifiers`
  ADD KEY (`id`),
  ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `releases`
--
ALTER TABLE `releases`
  ADD KEY (`id`),
  ADD KEY `package_id` (`package_id`);

--
-- Indexes for table `urls`
--
ALTER TABLE `urls`
  ADD KEY (`id`),
  ADD KEY `package_id` (`package_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- Constraints for table `package_classifiers`
--
ALTER TABLE `package_classifiers`
  ADD CONSTRAINT `package_classifiers_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `releases`
--
ALTER TABLE `releases`
  ADD CONSTRAINT `belongs_to_package` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `urls`
--
ALTER TABLE `urls`
  ADD CONSTRAINT `urls_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `packages` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
