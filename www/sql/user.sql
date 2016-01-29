CREATE TABLE `user` (
    `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL DEFAULT '',
    `email` varchar(255) NOT NULL DEFAULT '',
    `password_hash` varchar(255) NOT NULL DEFAULT '',
    `screen_name` varchar(255) NOT NULL DEFAULT '',
    `sex` char(1) NOT NULL DEFAULT '',
    `birthday` char(8) NOT NULL DEFAULT '',
    `picture_id` bigint(20) UNSIGNED NOT NULL,
    `time_created` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    `time_updated` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    PRIMARY KEY (`id`),
    UNIQUE KEY (`email`),
    UNIQUE KEY (`screen_name`),
    FOREIGN KEY (`picture_id`) REFERENCES `picture` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
