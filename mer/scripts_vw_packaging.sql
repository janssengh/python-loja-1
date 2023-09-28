CREATE VIEW `vw_packaging` AS
 select
  id,
  concat(if(format=1, "Caixa/Pacote", if(format=2, "Rolo/Prisma", "Envelope")), " = peso:", weight, " Kg CxAxL:", length," X ", height, " X ", width) as dimension
   from packaging;
