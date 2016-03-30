CREATE TABLE `picture` (
    `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
    `picture` blob,
    `time_created` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    `time_updated` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
