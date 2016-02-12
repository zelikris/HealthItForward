CREATE TABLE `survey_answer_choice` (
    `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
    `survey_question_id` bigint(20) UNSIGNED NOT NULL,
    `text` VARCHAR(255) NOT NULL DEFAULT '',
    `time_created` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    `time_updated` bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    PRIMARY KEY (`id`),
    FOREIGN KEY (`survey_question_id`) REFERENCES `survey_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
