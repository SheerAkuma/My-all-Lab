<html>
<head>
    <meta charset="utf-8">
    <meta name="keywords" content="Лабораторна робота, MySQL, з'єднання з базою даних">
    <meta name="description" content="Лабораторна робота. З'єднання з базою даних">
    <title>Таблиця з повідомленнями</title>
</head>
<body>
    <h1>Всі повідомлення</h1>

    <?php

    $mysqli = new mysqli('localhost', 'root', '', 'db'); // Створюємо нове підключення з назвою $mysqli за допомогою створення об'єта класу mysqli. Параметри підключення по порядку: сервер, логін, пароль, БД
    $mysqli->set_charset("utf8"); // Встановлюємо кодування utf8
    
    if (mysqli_connect_errno()) {
    printf("Підключення до сервера не вдалось. Код помилки: %s\n", mysqli_connect_error());
    exit;
    }

    /* Надсилаємо запит серверу */
    if($result = $mysqli->query('SELECT u.user_name, m.message_text FROM users AS u INNER JOIN messages AS m ON u.user_id = m.user_id')) {   // $mysqli - наш об'єкт, через який здійснюємо підключення, query - метод, який дозволяє виконати довільний запит

        printf("<table><tr><th>Користувач</th><th>Повідомлення</th></tr>");
        /* Вибірка результатів запиту  */
        while( $row = $result->fetch_assoc() ){
            printf("<tr><td>%s</td><td>%s</td></tr>", $row['user_name'], $row['message_text']); //виводимо результат на сторінку
        };
        printf("</table>");
        /*Звільняємо пам'ять*/
        $result->close();
    }

    /*Закриваємо з'єднання*/
    $mysqli->close();
    ?>
    
</body>
</html>
