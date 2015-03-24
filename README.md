```
Тестовое задание: проект “Афиша”
 
Стоит задача создать веб­приложение “Афиша” на Django с хранением данных в БД 
PostgreSQL. 
 
1. Используя Django ORM, создайте следующую схему:
 
Сервис хранит список событий(например, туры, концерты, выставки, и т.д.). Каждое 
событие имеет список “инстансов” имеющих дату начала/конца и место проведения. 
Например: 
         Событие: тур группы Metallica 
         Инстансы: 
             ● Air Canada Center, Toronto, 2015­09­15 19:00 
             ● Scotiabank Saddledome, Calgary, 2015­09­20 20:00 
Место проведения имеет следующие аттрибуты: 
      ● Название 
      ● Город 
      ● Координаты(используется для geo запросов) 
 
Event имеет следующие аттрибуты: 
      ● Название 
      ● Опасание 
      ● Список “Категорий” 
      ● Список “Инстансов” 
 
 
2. Используя django-rest-framework создайте следуюшие ресурсы:
 
 
GET /api/events?page=1&per_page=10&category=3 (​       list of events with an optional category 
filter) 
GET /api/events/geosearch?lat=&long=&radius=&page=1&per_page=10 (​            find events no 
further than radius km from point(lat, long)) 
 
{ 
  “pagination”: { 
    “has_next”: true, 
    “has_prev”: false 
  }, 
  “data”: [ 
    { 
      “id”: 123, 
      “title”: “Metallica Tour”, 
      “description: “Some description” 
    }, 
    ... 
  ] 
} 
 
GET /api/events/123 ​       (event details) 
{ 
  “id”: 123, 
  “title”: “Metallica Tour”, 
  “desctription”: “Some description”, 
  “instances”: [ 
    { 
      “start”: “2015­09­15 19:00”, 
      “end”: “”, 
      “place”: { 
        “id”: 1, 
        “name”: “Air Canada Center”, 
        “lat”: 43.643466, 
        “long”: ­79.379099, 
        “city”: { 
          “id”: 1, 
          “Name”: “Toronto” 
        } 
      } 
    }, 
    ... 
  ] 
} 
 
POST /api/events ​       (create a new event from JSON body and return newly created object as in 
details, or return 400 with a list of validation errors) 
PUT /api/events/123 ​       (update event with id 123 with JSON body and return updated object as in 
details, or return 400 with a list of validation errors) 
 
3. Используя любой javascript фреймворк, создать приложение для
отображения списка событий с pagination’ом, при клике на event отобразить
детали event’а со списком инстансов:
 
 
  Event 1                    Event 2 
                             Some Desctiption 
  Event 2                     
  Event 3                      start date   Place name   City 
                               start date   Place name   City 
                              
 
<< Prev page | Next page >> 
```
 
