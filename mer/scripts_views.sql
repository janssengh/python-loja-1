CREATE VIEW `vw_product` AS
    SELECT 
        p.id,
        p.name,
        price,
        stock,
        colors,
        discription,
        pub_date,
        brand_id,
        br.name nmbrand,
        category_id,
        ct.name nmcategory,
        image_1,
        image_2,
        image_3,
        discount,
        size_id,
        sz.name nmsize,
        color_id,
        cl.name nmcolor,
        packaging_id,
        pc.weight,
        pc.format,
        pc.length,
        pc.height,
        pc.width
    FROM
        janssenmkt.product p
            INNER JOIN
        brand br ON brand_id = br.id
            INNER JOIN
        category ct ON category_id = ct.id
            INNER JOIN
        size sz ON size_id = sz.id
            INNER JOIN
        color cl ON color_id = cl.id
			INNER JOIN
		packaging pc ON packaging_id = pc.id;