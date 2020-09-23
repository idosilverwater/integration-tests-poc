import pymysql.cursors


def test_fixture(sql_server_service):
    container_ip_address = sql_server_service[0]
    connection = pymysql.connect(host=container_ip_address,
                                    user='john',
                                    password='Password1',
                                    db='test_db',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
                # Create a new record
                create_table = """
                  CREATE TABLE `users` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                     `email` varchar(255) COLLATE utf8_bin NOT NULL,
                     `password` varchar(255) COLLATE utf8_bin NOT NULL,
                     PRIMARY KEY (`id`)
                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                    AUTO_INCREMENT=1 ;
                """
                cursor.execute(create_table)
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
                sql = "SELECT * FROM users;"
                res = cursor.execute(sql)
                print(res)


        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                print(result)
    finally:
        connection.close()
