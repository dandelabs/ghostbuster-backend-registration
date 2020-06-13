CREATE SCHEMA `pfoptimization`;

CREATE TABLE `pfoptimization`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(30) NOT NULL,
  `last_name` VARCHAR(30) NOT NULL,
  `nick_name` VARCHAR(8) NOT NULL,
  `password` LONGBLOB NOT NULL,
  `salt` LONGBLOB NOT NULL,
  `state` VARCHAR(9) NULL CHECK (state IN ('ACTIVE','INACTIVE')),
  `created` DOUBLE NULL,
  `updated` DOUBLE NULL,
  PRIMARY KEY (`id`));
