<a name="top"></a>
<p align="center">
  <img src="assets\image\git_img_top.png" width="250" height="250" />
</p>
<h2 align="center">Определение и классификация дефектов сварных швов с помощью ИИ (Атомик Хак 2.0)</h2>

<div align="center">

<a href="https://github.com/Ilnarrk/weld_defect_bot">
  <img src="https://img.shields.io/github/watchers/Ilnarrk/weld_defect_bot?label=Watch&style=social&logo=github" alt="github-watchers">
</a>
<a href="https://github.com/Ilnarrk/weld_defect_bot">
  <img src="https://img.shields.io/github/stars/Ilnarrk/weld_defect_bot?style=social&logo=github" alt="github-stars">
</a>

</div>

<br/>

<img src="https://github.githubassets.com/images/icons/emoji/octocat.png" alt="octocat" style="height: 1em;"> Содержание:
- [Описание](#description)
  - [Проблематика](#problem)
  - [Решение](#decision)
- [Команда](#team)
- [Выбранные технологии](#tech)
- [Демонстрация продукта](#mvp)
- [Действия для запуска решения](#start)
<span id="description"></span>
## Описание <a href="#top"><img src="assets/image/git_img_up.png" width="25" /></a>
Формулировка задачи - Создать программный модуль определения и классификации дефектов сварных швов.

<span id="problem"></span>
### Проблематика <a href="#top"><img src="assets/image/git_img_up.png" width="25" /></a>
При выполнении сварных швов возникают дефекты. Первый этап контроля качества сварных швов – это визуальный измерительный контроль, когда дефектоскопист визуально осматривает швы на предмет обнаружения дефектов. Часть дефектов может быть пропущена при осмотре, что может критически сказаться на качестве выпускаемой продукции. 

Также при обучении сварке человек допускает большое количество дефектов в сварных швах. В силу недостатка опыта он может не определить или неправильно определить часть дефектов. Соответственно, не понимая, какие дефекты он допустил, он не может понять причину их возникновения и найти пути решения.

<span id="decision"></span>
### Решение <a href="#top"><img src="assets/image/git_img_up.png" width="25" /></a>
Мы создали онлайн решение определения дефектов сварных швов с помощью передовых технологий компьютерного зрения. Минимально жизнеспособным продуктом (MVP) был выбран телеграм-бот, который позволяет путем загрузки фотографий выполненных сварных швов получать обратную связь от платформы с описание найденных дефектов и указанием их локации. 

Также мы внедрели базу знаний, на которой пользователи смогут обучаться прикладной профессии без необходимости привлечения наставника.
Данное решение позволит не только сэкономить большое количество сил и средств, обеспечивая работу дефектоскописта, но и повысить квалификацию сотрудников.

<span id="team"></span>
## Команда <a href="#top"><img src="assets/image/git_img_up.png" width="25" /></a>
- <a href="https://github.com/Ilnarrk">Курбангалиев Ильнар</a>
- <a href="https://github.com/AjzSahmetzyanov">Ахметзянов Айзат</a>
- <a href="https://github.com/rakhmanov-tr">Рахманов Тимур</a>

<span id="tech"></span>
## Выбранные технологии <a href="#top"><img src="assets/image/git_img_up.png" width="25" /></a>
Для реализации данной задачи были выбраны:
- язык программирования Python
- модели компьютерного зрения семейства YOLOv8

Данные технологии официально доступны на территории РФ и обладают лицензией, позволяющей свободное коммерческое использование.

<span id="mvp"></span>
## Демонстрация продукта <a href="#top"><img src="assets/image/git_img_up.png" width="25" /></a>
<details>
  <summary>⚙️Кликните, чтобы отобразить демонстрацию MVP</summary>

  ![git_gif_1](assets/gif/git_gif_mvp.gif)
</details>
 
<span id="start"></span>
## Действия для запуска решения <a href="#top"><img src="assets/image/git_img_up.png" width="25" /></a>

#### Устанавливаем виртуальное окружение 
```bash
python -m venv .venv
```

#### Активируем виртуальное окружение
```bash
.\.venv\Scripts\activate
```

#### Устанавливаем зависимости
```bash
python -m pip install -r requirements.txt
```

#### Указываем токен телеграм бота
config/config.py необходимо указать токен телеграмм бота, который можно получить @BotFather (https://t.me/BotFather)

#### Запускаем и пользуемся приложением
```bash
python main.py
```