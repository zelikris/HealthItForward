CREATE TABLE `survey_response` (
    `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` bigint(20) UNSIGNED NOT NULL,
    `survey_id` bigint(20) UNSIGNED NOT NULL,
    `time_created` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    `time_updated` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
    FOREIGN KEY (`survey_id`) REFERENCES `survey` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
