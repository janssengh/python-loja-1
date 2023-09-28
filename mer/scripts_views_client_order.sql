CREATE VIEW `vw_client_order` AS
SELECT 
        co.id,
        co.status,
        date_format(co.created_date, '%d/%m/%y') as created_date,
        date_format(co.created_date, '%H:%I') as created_hour,
        co.invoice,
        co.client_id,
        co.order,
        c.name,
        c.email,
        c.contact
         FROM
        janssenmkt.client_order co
            INNER JOIN
        janssenmkt.client c ON c.id = co.client_id;