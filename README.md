Задача на позицию Python Developer 

Контекст
Мы хотим каждый день записывать в базу данных DynamoDB список значений некоторой активности пользователя.

Нужно придумать такую схему хранения, чтобы содержание базы обходилось максимально дешево.

Подробности
У нас 1 000 000 юзеров

Планируемая нагрузка по IO:

По каждому из пользователей один раз в сутки мы сохраняем список activity_scores. Это список целых чисел от 1 до 99. Активность трекается ровно каждые 30 секунд, т.е. 24 * 60 * 60 / 30 = 2880 значений за сутки.
По каждому из пользователей один раз в сутки нам приходят 2 запроса на чтение:
получить список activity_scores за конкретный час любого дня,
получить список activity_scores за конкретные 12 часов.
Отрезок времени всегда начинается в 0 минут часа. Например:

с 08:00 до 09:00,
или с 06:00 до 18:00,
или с 22:00 до 10:00.
Мы разрабатываем схему хранения, где каждый документ в базе будет выглядеть как такой json:

{
  "u": 123456,
  "t": 1693440000,
  "v": [60, 61, 78, ...]
}
где

u - целое число, id юзера от 1 до 1_000_000 (partition key)
t - целое число, unix timestamp в UTC (sort key)
v - список целых чисел значений activity_scores
Что надо сделать:
Напишите функцию:

def convert_to_dynamodb_documents(

    user_id: int,               # id юзера - от 1 до 1_000_000

    day: datetime.date,         # день, за который нужно записать данные в базу

    activity_scores: List[int]  # список ровно из 2880 значений activity_scores,
                                # каждая из которых записана с интервалом в 30 секунд
                                # с начала дня по UTC
) -> List[Dict]:
    pass
Функция должна возвращать список словарей {"u": user_id, "t": timestamp, "v": [...]}.

Каждый элемент возвращаемого списка - отдельный документ, который будет записан в базу.

Функция должна готовить документы таким образом, чтобы запись и чтение из базы за месяц суммарно стоили максимально дешево.

Ожидаемый результат
Вставьте ваше решение задачи в текстовое поле анкеты в следующем формате:

Код функции convert_to_dynamodb_documents:
<сюда вставить код функции>

Справочная информация
Как рассчитывать размер документа в DynamoDB
Размер атрибута с числовым значением = длина его названия + размер числа.
Размер числа = (1 байт на каждые 2 цифры) + 1 байт.
Размер атрибута со списком чисел = длина его названия + (размер всех его элементов) + (количество элементов) + 3 байта.
Например:

размер поля "v": [60, 61, 78]

1 (длина строки "v") +
3 * 2 (3 числа по 2 байта каждое) +
3 (всего элементов в списке) +
3
= 13 байт
Как рассчитывать стоимость запросов на чтение и запись
Учитываем только цену запросов на чтение и запись (без стоимости хранения и любых других фичей DynamoDB) и используем стандартный ценник:

$1.25 per million write request units (WRU)

$0.25 per million read request units (RRU)

Как считаются WRU: 1 WRU на документ до 1 КБ с округлением вверх. То есть:

для документов размером меньше 1 КБ для их записи потребуется ровно 1 WRU,
для документов от 1 до 2 КБ потребуется ровно 2 WRU,
и так далее: на каждый дополнительный 1 КБ нужен дополнительный 1 WRU.
При записи в базу каждой отдельной записи WRU считаются отдельно.
Как считаются RRU: 1 RRU на чтение до 4 КБ с округлением вверх. То есть:

для документов размером меньше 4 КБ для их чтения потребуется ровно 1 RRU,
для документов от 4 до 8 КБ потребуется ровно 2 RRU,
и так далее: на каждые дополнительные 4 КБ нужен дополнительный 1 RRU.
При чтении каждого отдельного документа RRU считаются отдельно.
Дополнительные ссылки
Это дополнительный контекст (для решения не обязателен).

DynamoDB:

Официальная документация: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/CapacityUnitCalculations.html
Подробный разбор стоимости: https://zaccharles.medium.com/calculating-a-dynamodb-items-size-and-consumed-capacity-d1728942eb7c
Калькулятор: https://zaccharles.github.io/dynamodb-calculator/
Цены в DynamoDB: https://aws.amazon.com/dynamodb/pricing/
FAQ
