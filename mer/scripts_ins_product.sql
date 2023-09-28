-- MySQL Workbench Forward Engineering


-- -----------------------------------------------------
-- Schema janssenmkt
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `janssenmkt` DEFAULT CHARACTER SET utf8 ;
USE `janssenmkt` ;



-- -----------------------------------------------------
-- Table `janssenmkt`.`bk_product`
-- -----------------------------------------------------
INSERT INTO `janssenmkt`.`product` SELECT
  `id`,
  `name`,
  `price`,
  `stock`,
  `colors`,
  `discription`,
  `pub_date`,
  `brand_id`,
  `category_id`,
  `image_1`,
  `image_2`,
  `image_3`,
  1,
  `discount`,
  `size_id`,
  `color_id`
    from  `janssenmkt`.`bk_product`


