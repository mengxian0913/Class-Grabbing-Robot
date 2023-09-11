# 逢甲大學搶課幾人 version 1.0 (112學年度第一學期)

## 展示

<iframe width="560" height="315" src="https://www.youtube.com/watch?v=NXj6LuLb0mk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 如何使用

```sh
git clone git@github.com:mengxian0913/Class-Grabbing-Robot.git
pip install PIL
pip install pytesseract
pip install bs4
pip install selenium
```

到 main/config.py 設定帳號密碼

```py
ACCOUNT = "Account"
PASSWORD = "Password"
```

啟動

```sh
python main/app.py
```