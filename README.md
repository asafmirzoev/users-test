# Сборка и запуск контейнера

#### *Предварительно у вас должны быть установлены [git](https://git-scm.com/downloads) и [docker](https://www.docker.com/products/docker-desktop/)*

### 1. Клонирование
#### *Чтобы склонировать, себе на "машину", выполните следующую коммнаду в коммнадной строке:*
```
git clone https://github.com/asafmirzoev/users-test.git
```


### 2. Сборка
#### *Выполните следующие комманды в коммнадной строке*
```
cd users-test
```

```
docker build -t users-test .
```

### 3. Запуск
```
docker run -p 8000:80 users-test
```

#### Приложение будет доступно по ссылке http://localhost:8000/


# Документация

#### Документация доступна по ссылке http://localhost:8000/docs

