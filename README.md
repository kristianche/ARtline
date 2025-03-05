# ARtline
Национална олимпиада по Информационни технологии  2024/2025г.
Проект 317: „АРтлайн“

Стартиране на проекта в Terminal:

     cd artline

     pip install -r requirements.txt

     py manage.py runserver

1. Тема на разработвания проект:  Проект за приложение за скициране чрез   добавена реалност 
	Категория: Съвременни системи за визуална информация
Регистрационен номер на проект: № 317
2.Автори:

Имена: Кристиян Калинчев Челебиев

Училище: ППМГ ,,Академик Никола Обрешков“ гр.Бургас

Имена: Кристина Антониева Иванова

Училище: ППМГ ,,Академик Никола Обрешков“ гр.Бургас

Ръководител: д-р Александър Димитров Иванов

Длъжност: Старши учител по информатика и информационни технологии
 
4. Резюме за проекта
   
4.1 Цели на проекта
	Целта на разработваното приложение е да се направи възможно скициране на контури върху видеопоток от камера на лаптоп или друго мобилно усторйство в реално време, както и съхраняването на снимки и видео с насложени контури. Такъв тип приложение може да се използва в широк набор от практически задачи:
- като визуална помощ при преподаване на учебен материал
- като заместител на хартиени учебни пособия
- в иновативни арт приложения
- в игрови приложения
Потенциални ползи от използването на такова приложение са:
- Може да се намали използването на пластмаса и хартия при провеждането на онлайн обучение или среща, предлагайки алтернатива на учебната дъска, маркер или химикал.
- Предоставяне на нови форми на художествено изразяване - ARtline предлага ново измерение на творчеството. Художниците, дизайнерите, архитектите и всички, които работят с визуални изкуства, могат да експериментират с нови форми на изразяване, без да се ограничават от физическите граници на традиционните носители. Технологията позволява създаването на интерактивни и динамични произведения, които могат да бъдат споделени с други хора в реално време и от всяка точка на света.
- С приложението, творческите процеси стават по-гъвкави и достъпни, създавайки нови възможности за колаборации и иновации в различни сфери.
	В обобщение, тази технология може да бъде интегрирана в образованието, медицината и в ежедневните комуникации, предоставяйки на хората иновативни начини да визуализират и обменят идеи.
4.2. Основни етапи в реализирането на проекта 
Основните етапи при изготвяне на настоящият проект са следните:
1)	Проучване на съществуващи решения и технологии
2)	Структуриране на проекта,  избор на технологии и разпределяне на задачи
3)	Програмно осигуряване на необходимите средства за разработка – библиотеки, среди за разработка
4)	Реализиране на основната функционалност
5)	Интегриране на функционалност в потребителския интерфейс
6)	Тестове
7)	Изготвяне на документация, рекламни и презентационни материали
Роли на авторите: 
Кристиян Челебиев - програмна реализация на backend функционалност
Кристина Иванова - програмна реализация на frontend потребителски интерфейс, изработка на рекламни и презентационни материали
4.3. Ниво на сложност на проекта 
	Нивото на сложност на проекта може да се определи като средно. В проекта се използват съществуващи технологии, които се интегрират чрез установени практики и софтуерни архитектури. Програмната реализация изисква употребата на разнородни технологии, което прави проекта трудоемък. 

4.4. Логическо и функционално описание на решението
Проектът включва:
-	Потребителски интерфейс (Front-end) – визуалната част от проекта, съдържаваща бутони, свързани с дадена функционалност, и екран, показващ резултата
-	Логически слой (Back-end) - бизнес логиката, която обработва данните приети от презентационния слой 
Функционално описание:
	Приложението ARtline има бутони, които позволяват потребителят да сменя дебелината на линиите, които изписва с пръста си- тънки, средни или широки. Също така има възможността да сменя цветовете преди да започне да пише- черно, жълто, червено, синьо, зелено или лилаво. Ако рисуващият допусне някаква грешка, може да изтрие част от написаното с бутон, активиращ гумичката. Потребителят може да запази създаденото изображение чрез бутона с камерата, който прави екранна снимка и я запазва локално на устройството му.



4.5. Реализация на проекта
Технологии, изпозлвани за реализиране на backend функционалност:
- Програмен език Python – един от най-популярните в съвремието програмни езици, характеризиращ се с лесен синтаксис, многоплатформена поддържка и широк набор от инструменти за различни практически приложения.
- Библиотека OpenCV – библиотека на Python, предоставяща интелигентни модели, обучени за компютърно зрение (разпознаване на образи от изображения).
- Библиотека MediaPipe -  библиотека на  Python за манипулация на визуални потоци от камери.
- Платформа Django – платформа на  Python за разработка на уеб сървърни приложния.
Изброените технологии са съвместими помежду си и съвместната им употреба гарантира лесна интеграция на отделните модули на проекта.
Технологии, използвани за реализиране на потребителски интерфейс:
- HTML – език за маркриане в основата на уеб.
- CSS – език за стилове, интегрална част от HTML.
- jQuery – библиотека на JavaScript за манипулация на обекти в уеб страници. JavaScript е водещият език за реализиране на функционалности и интерактивни дизайни в уеб разработките.

Изходният код на проекта е качен в GitHub.
Линк към github: https://github.com/kristianche/ARtline


4.6. Описание на приложението 
По-долу са описани бутоните на приложението.

-бутон, позволяващ на потребителя да сменя дебелината на линиите, които изписва във въздуха – тънки, средни или широки

-бутон, който позволява на потребителя да сменя цвета на линиите- черно, червено, зелено, синьо, жълто или лилаво 

-бутон, чрез който потребителят задейства гумичката

-бутон за изтриване на създаденото от потребителя

4.7. Заключение 
	Представеният проект успешно реализира приложение за изчертаване на контури върху видеопоток чрез технологии за добавена реалност.  Проектът предлага работещ интерфейс, като някои разширени функционалности са в процес на разработка.

Използвани източници
https://opencv.org/
https://www.djangoproject.com/ 
https://moldstud.com/articles/p-python-for-augmented-reality-creating-interactive-experiences 
https://pyimagesearch.com/2021/01/04/opencv-augmented-reality-ar/ 
 


