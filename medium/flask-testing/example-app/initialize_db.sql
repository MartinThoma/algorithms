CREATE TABLE `authors` (
  `id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `authors` (`id`, `first_name`, `last_name`) VALUES
(1, 'Stephen', 'King'),
(2, 'Trudi', 'Canavan');

CREATE TABLE `books` (
  `id` int NOT NULL,
  `author_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `original_language` char(2) NOT NULL,
  `isbn` char(17) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `books` (`id`, `author_id`, `title`, `original_language`, `isbn`) VALUES
(1, 1, 'The Shining', 'EN', '978-0307743657'),
(2, 1, 'The Dark Tower: The Gunslinger', 'EN', '978-0-937986-50-9'),
(3, 2, 'The Magician\'s Apprentice', 'EN', '978-0-316-03788-4');
ALTER TABLE `authors`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_id` (`author_id`);
ALTER TABLE `authors`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
ALTER TABLE `books`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;
