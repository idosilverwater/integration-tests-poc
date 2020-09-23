import pymysql.cursors


def test_sql_fixture(sql_server_service):
    container_ip_address = sql_server_service[0]
    connection = pymysql.connect(host=container_ip_address,
                                    user='john',
                                    password='Password1',
                                    db='test_db',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
                create_user_table = """
                  CREATE TABLE `users` (
                    `id` int(11) NOT NULL AUTO_INCREMENT,
                     `email` varchar(255) COLLATE utf8_bin NOT NULL,
                     `password` varchar(255) COLLATE utf8_bin NOT NULL,
                     PRIMARY KEY (`id`)
                  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                    AUTO_INCREMENT=1 ;
                """
                cursor.execute(create_user_table)
                insert_user = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(insert_user, ('webmaster@python.org', 'very-secret'))

        connection.commit()

        with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ('webmaster@python.org',))
                result = cursor.fetchone()
                assert result == {'id': 1, 'password': 'very-secret'}
    finally:
        connection.close()
