-- MySQL Workbench Forward Engineering


-- -----------------------------------------------------
-- Schema janssenmkt
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `janssenmkt` DEFAULT CHARACTER SET utf8 ;
USE `janssenmkt` ;



-- -----------------------------------------------------
-- Table `janssenmkt`.`bk_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`bk_product` (
  `id` INT NOT NULL,
  `name` VARCHAR(80) NOT NULL,
  `price` DECIMAL(15,2) NOT NULL,
  `stock` INT NOT NULL,
  `colors` VARCHAR(45) NOT NULL,
  `discription` VARCHAR(250) NOT NULL,
  `pub_date` DATETIME NOT NULL,
  `brand_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  `image_1` VARCHAR(150) NOT NULL,
  `image_2` VARCHAR(150) NOT NULL,
  `image_3` VARCHAR(150) NOT NULL,
  `discount` INT NULL,
  `size_id` INT NULL,
  `color_id` INT NULL)
  
ENGINE = InnoDB;


