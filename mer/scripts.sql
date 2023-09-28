-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema janssenmkt
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema janssenmkt
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `janssenmkt` DEFAULT CHARACTER SET utf8 ;
USE `janssenmkt` ;

-- -----------------------------------------------------
-- Table `janssenmkt`.`brand`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`brand` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(40) NOT NULL,
  `user` VARCHAR(80) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `password` VARCHAR(180) NOT NULL,
  `profile` VARCHAR(180) NOT NULL,
  `packaging_format` VARCHAR(1) NULL,
  `zipcode_origin` VARCHAR(50) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_UNIQUE` (`user` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`clientant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`clientant` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NULL,
  `email` VARCHAR(50) NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `country` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `contact` VARCHAR(50) NULL,
  `address` VARCHAR(50) NULL,
  `zipcode` VARCHAR(50) NULL,
  `profile` VARCHAR(50) NULL,
  `created_date` DATETIME NULL,
  `code` VARCHAR(14) NULL,
  `neighborhood` VARCHAR(45) NULL,
  `complement` VARCHAR(45) NULL,
  `region` VARCHAR(15) NULL,
  `number` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `password_UNIQUE` (`password` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`size`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`size` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`color`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`color` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`packaging`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`packaging` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `weight` VARCHAR(4) NOT NULL,
  `format` INT NOT NULL,
  `length` DECIMAL(15,2) NOT NULL,
  `height` DECIMAL(15,2) NOT NULL,
  `width` DECIMAL(15,2) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
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
  `color_id` INT NULL,
  `packaging_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_product_brand_idx` (`brand_id` ASC) VISIBLE,
  INDEX `fk_product_category1_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_product_size1_idx` (`size_id` ASC) VISIBLE,
  INDEX `fk_product_color1_idx` (`color_id` ASC) VISIBLE,
  INDEX `fk_product_packaging1_idx` (`packaging_id` ASC) VISIBLE,
  CONSTRAINT `fk_product_brand`
    FOREIGN KEY (`brand_id`)
    REFERENCES `janssenmkt`.`brand` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `janssenmkt`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_size1`
    FOREIGN KEY (`size_id`)
    REFERENCES `janssenmkt`.`size` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_color1`
    FOREIGN KEY (`color_id`)
    REFERENCES `janssenmkt`.`color` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_packaging1`
    FOREIGN KEY (`packaging_id`)
    REFERENCES `janssenmkt`.`packaging` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`client`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`client` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(14) NOT NULL,
  `type` VARCHAR(2) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `zipcode` VARCHAR(50) NOT NULL,
  `address` VARCHAR(50) NOT NULL,
  `number` INT NOT NULL,
  `neighborhood` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `region` VARCHAR(15) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_date` DATETIME NOT NULL,
  `complement` VARCHAR(45) NULL,
  `profile` VARCHAR(50) NULL,
  `contact` VARCHAR(50) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `code_UNIQUE` (`code` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`client_order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`client_order` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(20) NOT NULL,
  `created_date` DATETIME NOT NULL,
  `invoice` VARCHAR(20) NOT NULL,
  `client_id` INT NOT NULL,
  `order` LONGTEXT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_client_order_client1_idx` (`client_id` ASC) VISIBLE,
  CONSTRAINT `fk_client_order_client1`
    FOREIGN KEY (`client_id`)
    REFERENCES `janssenmkt`.`client` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`cep`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`cep` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `zipcode` VARCHAR(50) NOT NULL,
  `address` VARCHAR(50) NULL,
  `number` INT NULL,
  `neighborhood` VARCHAR(45) NULL,
  `complement` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `region` VARCHAR(15) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `zipcode_UNIQUE` (`zipcode` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `janssenmkt`.`login`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`login` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(60) NULL,
  `idade` VARCHAR(60) NULL,
  `email` VARCHAR(200) NULL,
  `senha` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;

USE `janssenmkt` ;

-- -----------------------------------------------------
-- Placeholder table for view `janssenmkt`.`vw_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `janssenmkt`.`vw_product` (`id` INT, `name` INT, `price` INT, `stock` INT, `colors` INT, `discription` INT, `pub_date` INT, `brand_id` INT, `nmbrand` INT, `category_id` INT, `nmcategory` INT, `image_1` INT, `image_2` INT, `image_3` INT, `discount` INT, `size_id` INT, `nmsize` INT, `color_id` INT, `nmcolor` INT);

-- -----------------------------------------------------
-- View `janssenmkt`.`vw_product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `janssenmkt`.`vw_product`;
USE `janssenmkt`;
CREATE  OR REPLACE VIEW `vw_product` AS
SELECT p.id,p.name,price,stock,colors,discription,pub_date,brand_id,
br.name nmbrand,category_id,ct.name nmcategory,
image_1,image_2,image_3,discount,
size_id,sz.name nmsize,color_id,cl.name nmcolor
FROM janssenmkt.product p
inner join brand br on brand_id = br.id
inner join category ct on category_id = ct.id
inner join size sz on size_id = sz.id
inner join color cl on color_id = cl.id ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
