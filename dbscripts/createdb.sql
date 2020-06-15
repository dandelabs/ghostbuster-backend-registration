CREATE SCHEMA `pfoptimization`;

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `nick_name` varchar(8) NOT NULL,
  `password` longblob NOT NULL,
  `salt` longblob NOT NULL,
  `state` varchar(9) DEFAULT NULL,
  `created` double DEFAULT NULL,
  `updated` double DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `nick_name_UNIQUE` (`nick_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;




CREATE TABLE `pfoptimization`.`downtimes` (
  `downtime_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `downtime_type_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `status_id` INT NOT NULL, 
  `downtime_start_time` DOUBLE NOT NULL,
  `downtime_finish_time` DOUBLE NOT NULL,
  PRIMARY KEY (`downtime_id`));




CREATE TABLE `pfoptimization`.`production` (
  `production_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `status_id` INT NOT NULL, 
  `production_start_time` DOUBLE NOT NULL,
  `production_finish_time` DOUBLE NOT NULL,
  `production_units_manufactured` INT NOT NULL,
  PRIMARY KEY (`production_id`));
    
  
  CREATE TABLE `pfoptimization`.`downtime_type` (
  `downtime_type_id` INT NOT NULL AUTO_INCREMENT,
  `downtime_type_name` VARCHAR(45) NOT NULL,
  `downtime_type_description` VARCHAR(45) NOT NULL,
  `downtime_type` VARCHAR(45) NOT NULL,
  `downtime_active` VARCHAR(9) NOT NULL CHECK (state IN ('ACTIVE','INACTIVE')),
  PRIMARY KEY (`downtime_type_id`));
  
  
  CREATE TABLE `pfoptimization`.`production_status` (
  `production_status_id` INT NOT NULL AUTO_INCREMENT,
  `production_status_description` VARCHAR(45) NOT NULL,
  `production_status_active` VARCHAR(9) NOT NULL CHECK (state IN ('ACTIVE','INACTIVE')),
  PRIMARY KEY (`production_status_id`));
  
  
  CREATE TABLE `pfoptimization`.`changeover_cost` (
  `changeover_cost_id` INT NOT NULL AUTO_INCREMENT,
  `from_status_id` INT NULL NOT NULL,
  `to_status_id` INT NULL NOT NULL,
  `changeover_cost_time` INT NULL NOT NULL,
  `changeover_cost_active` VARCHAR(9) NOT NULL CHECK (state IN ('ACTIVE','INACTIVE')),
  PRIMARY KEY (`changeover_cost_id`));
  
  CREATE TABLE `pfoptimization`.`products_processes` (
  `product_processes_id` INT NOT NULL AUTO_INCREMENT,
  `item_id` INT NOT NULL,
  `from_status_id` INT NOT NULL,
  `to_status_id` INT NOT NULL,
  `machine_id` INT NOT NULL,
  `product_processes_std_time` INT NOT NULL,
  `product_processes_active` VARCHAR(9) NOT NULL CHECK (state IN ('ACTIVE','INACTIVE')),
  PRIMARY KEY (`product_processes_id`));


  CREATE TABLE `pfoptimization`.`machines` (
  `machine_id` INT NOT NULL AUTO_INCREMENT,
  `machine_name` VARCHAR(9) NOT NULL,
  `status_id_primary_rm` INT NOT NULL,
  `status_id_secondary_rm` INT NOT NULL,
  `machine_active` VARCHAR(9) NOT NULL CHECK (state IN ('ACTIVE','INACTIVE')),
  PRIMARY KEY (`machine_id`));



CREATE TABLE `pfoptimization`.`orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `order_number` VARCHAR(15) NOT NULL,
  `item_id` INT NOT NULL,
  `order_customer_name` VARCHAR(50) NOT NULL,
  `order_due_date` DOUBLE NOT NULL,
  `order_quantity` INT NOT NULL,
  `order_quantity_received` INT NOT NULL,
  `order_received_date` DOUBLE NOT NULL,
  `order_status_id` INT NULL,
  PRIMARY KEY (`order_id`));
  
  CREATE TABLE `pfoptimization`.`order_status` (
  `order_status_id` INT NOT NULL AUTO_INCREMENT,
  `order_status_description` VARCHAR(45) NOT NULL,
  `order_status_active` VARCHAR(9) NOT NULL CHECK (state IN ('ACTIVE','INACTIVE')),
  PRIMARY KEY (`order_status_id`));
  
  
CREATE TABLE `machine_user` (
  `machine_user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `machine_id` int(11) NOT NULL,
  `machine_user_active` varchar(9) NOT NULL,
  PRIMARY KEY (`machine_user_id`),
  KEY `user_id_idx` (`user_id`),
  KEY `machine_id_idx` (`machine_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `machine_id` FOREIGN KEY (`machine_id`) REFERENCES `machines` (`machine_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);
  
  CREATE TABLE `pfoptimization`.`items` (
  `item_id` INT NOT NULL AUTO_INCREMENT,
  `items_code` VARCHAR(45) NOT NULL,
  `item_description` VARCHAR(45) NOT NULL,
  `item_active` VARCHAR(9) NOT NULL CHECK (state IN ('ACTIVE','INACTIVE')),
  PRIMARY KEY (`item_id`));
