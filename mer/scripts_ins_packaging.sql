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
-- Table `janssenmkt`.`packaging`
-- -----------------------------------------------------
INSERT INTO `janssenmkt`.`packaging`(
  `id`,
  `weight`,
  `format`,
  `length`,
  `height`,
  `width`) VALUES
(2,'1',1,30,30,30)


