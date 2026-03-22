# 基礎 2D 圖形學教學：PyQt6、三角函數、基礎數學

## 專案目標

這個範例用 `PyQt6` 做一個很適合入門的 2D 圖形學小程式，重點不是做複雜功能，而是把下面幾件事講清楚：

- 什麼是 2D 座標系
- 為什麼畫圖會用到 `sin` 和 `cos`
- 角度與弧度怎麼轉換
- 如何把數學公式變成畫面上的點、線、圓

這個程式分成兩個視覺區塊：

- 左邊：目前圖形的座標與向量示意
- 右邊：對應公式的函數變化

現在也可以用選單切換三種模式：

- `Circle`
- `Ellipse`
- `Skew Ellipse`

你拖動滑桿，或讓動畫自己跑，就能看到角度變化如何影響：

- 向量終點位置
- `cos(theta)` 的水平投影
- `sin(theta)` 的垂直投影
- 正弦曲線上的對應點

---

## 執行方式

### 1. 安裝套件

```bash
pip install -r requirements.txt
```

### 2. 執行程式

```bash
python main.py
```

---

## 你會學到的數學

### 1. 2D 座標系

在 2D 平面上，一個點通常寫成：

```text
(x, y)
```

例如：

```text
(100, 50)
```

代表這個點在水平方向是 `100`，垂直方向是 `50`。

不過在電腦圖學裡，常常要注意一件事：

- 數學課常見的座標系：`y` 往上是正
- 螢幕座標系：`y` 往下是正

所以在程式裡，如果你想讓「數學上的往上」看起來真的往上，常會寫成：

```python
screen_y = center_y - math.sin(theta) * radius
```

這裡的減號很重要。

---

### 2. 角度與弧度

Python 的 `math.sin()` 和 `math.cos()` 接收的是「弧度」，不是角度。

轉換公式：

```text
radian = degree * pi / 180
```

在 Python 裡最常寫成：

```python
radians = math.radians(degrees)
```

例如：

- `0 度 = 0`
- `90 度 = pi / 2`
- `180 度 = pi`
- `360 度 = 2pi`

---

### 3. 三角函數如何決定點的位置

假設有一個圓心 `(cx, cy)`，半徑是 `r`，角度是 `theta`。

圓上的點可以寫成：

```text
x = cx + r * cos(theta)
y = cy - r * sin(theta)
```

這就是圖形學裡最常見、也最重要的基礎公式之一。

它代表：

- `cos(theta)` 決定水平位置
- `sin(theta)` 決定垂直位置

如果半徑是 `1`，這就是數學裡常講的單位圓概念。

---

### 4. 橢圓公式

如果不是圓，而是橢圓，就會把 `x` 和 `y` 的半徑分開：

```text
x = cx + a * cos(theta)
y = cy - b * sin(theta)
```

這裡：

- `a` 是水平半徑
- `b` 是垂直半徑

只要 `a` 和 `b` 不一樣，圖形就會從圓變成橢圓。

---

### 5. 斜橢圓公式

斜橢圓可以理解成「橢圓再加上一點水平斜切」。

這份範例用簡單、容易理解的方式表示：

```text
x = cx + a * cos(theta) + skew * b * sin(theta)
y = cy - b * sin(theta)
```

重點在這一項：

```text
skew * b * sin(theta)
```

它會把原本只影響 `y` 的 `sin(theta)`，也拿來影響 `x`，所以整個橢圓會往斜的方向傾斜。

---

## 程式重點拆解

### 1. 主繪圖區：`GraphicsCanvas`

這個類別繼承 `QWidget`，主要用途是自己控制畫面怎麼畫。

在 PyQt6 中，最常見的方式是覆寫：

```python
def paintEvent(self, event):
```

每次視窗需要重繪時，Qt 都會呼叫這個函式。

裡面我們建立：

```python
painter = QPainter(self)
```

然後就可以用 `painter` 來畫：

- 背景
- 線段
- 圓形
- 文字

---

### 2. 左半部：旋轉向量與投影

左邊會依照選單模式，切換不同的參數方程：

```python
point_x = center_x + radius * math.cos(radians)
point_y = center_y - radius * math.sin(radians)
```

如果切成橢圓，則會變成：

```python
point_x = center_x + radius_x * math.cos(radians)
point_y = center_y - radius_y * math.sin(radians)
```

如果切成斜橢圓，則會變成：

```python
point_x = center_x + radius_x * math.cos(radians) + skew * radius_y * math.sin(radians)
point_y = center_y - radius_y * math.sin(radians)
```

假設左邊畫布中心固定，當角度改變時：

- `cos(theta)` 影響水平分量
- `sin(theta)` 影響垂直分量
- `skew` 會讓 `sin(theta)` 額外參與水平位移

這樣就能畫出：

- 從圓心指向圓上的向量
- 點在 `x` 軸的投影
- 點在 `y` 軸的投影

投影線的概念很重要，因為它會直接把抽象的 `sin`、`cos`，以及斜切後的混合位移，變成可見的幾何意義。

---

### 3. 右半部：函數對應圖

右邊會依照模式顯示不同的公式概念：

```text
Circle: y = sin(x)
Ellipse: y = 0.75 * sin(x)
Skew Ellipse: y = cos(x) + 0.35 * sin(x)
```

它不是在畫完整的幾何圖，而是在補充說明「目前模式底層到底用了哪些三角函數組合」。

核心概念：

```python
ratio = pixel_x / graph_width
x_radian = ratio * math.tau
y_value = formula_value_for_graph(x_radian)
```

這裡的：

- `ratio` 是目前位置在整張圖裡的比例
- `math.tau` 等於 `2pi`
- `y_value` 就是正弦函數的結果

接著再把數學值映射到螢幕座標：

```python
draw_y = mid_y - amplitude * y_value
```

這樣就能在畫面上看到，當公式變成不同形式時，函數的整體樣子也會跟著改變。

---

## 為什麼這個範例適合初學者

這份程式刻意保持簡單：

- 檔案少
- 命名直接
- 數學公式集中
- 每一塊畫面都有明確目的

它很適合拿來做下面幾件事：

- 練習 `QPainter`
- 理解座標轉換
- 把 `sin` 和 `cos` 跟畫圖連起來
- 當作之後學旋轉、碰撞、動畫的起點

---

## 建議你接著練習的方向

### 練習 1：把 `sin` 改成 `cos`

試著把右邊波形改成：

```python
y_value = math.cos(x_radian)
```

看看整條曲線怎麼平移。

### 練習 2：改變振幅

目前振幅大約是：

```python
amplitude = 90
```

把它改大或改小，觀察波的高度。

### 練習 3：改變頻率

你可以把公式改成：

```python
y_value = math.sin(2 * x_radian)
```

這代表同樣寬度內，波會震盪兩次。

### 練習 4：加入滑鼠互動

之後可以試著加入：

- 滑鼠移動控制角度
- 點擊某個位置顯示座標
- 顯示目前向量長度
- 用滑鼠拖曳改變橢圓的 `a`、`b`、`skew`

---

## 程式結構建議

目前專案很精簡：

```text
Graphics/
├─ main.py
├─ requirements.txt
├─ .gitignore
└─ HACKMD.md
```

如果之後要擴充，可以改成：

```text
Graphics/
├─ main.py
├─ widgets/
│  └─ graphics_canvas.py
├─ docs/
│  └─ HACKMD.md
└─ requirements.txt
```

---

## 總結

這個範例最核心的概念只有一句話：

> 2D 圖形學常常就是把數學公式，轉成螢幕上的座標。

而在旋轉、圓周運動、波形、動畫裡，最常見的工具就是：

- `sin`
- `cos`
- 座標系
- 比例映射

如果你把這份程式看懂，後面要學：

- 旋轉變換
- 向量
- 矩陣
- 基礎遊戲開發

都會輕鬆很多。
