CREATE TABLE `survey_question` (
    `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
    `survey_id` bigint(20) UNSIGNED NOT NULL,
    `question_text` varchar(255) NOT NULL DEFAULT '',
    `type` char(1) NOT NULL DEFAULT '',
    `time_created` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    `time_updated` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    PRIMARY KEY (`id`),
    FOREIGN KEY (`survey_id`) REFERENCES `survey` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
