# Code Framework 教學

## 這份文件講什麼

前面幾份都在講數學，這一份則是整理這個專案的程式框架，讓你之後要加新 demo 時知道該從哪裡下手。

## 專案結構

目前重點檔案如下：

```text
Graphics/
├─ main.py
├─ HACKMD.md
├─ docs/
│  └─ hackmd/
│     ├─ 01_circle_math.md
│     ├─ 02_ellipse_math.md
│     ├─ 03_skew_ellipse_math.md
│     ├─ 04_lightning_math.md
│     ├─ 05_flame_math.md
│     └─ 06_code_framework.md
└─ shape_demos/
   ├─ __init__.py
   ├─ circle_demo.py
   ├─ ellipse_demo.py
   ├─ skew_ellipse_demo.py
   ├─ lightning_demo.py
   └─ flame_demo.py
```

## `main.py` 在做什麼

`main.py` 負責三件事：

1. 建立視窗和滑桿
2. 持有所有 demo 物件
3. 在 `paintEvent()` 裡呼叫目前模式的繪圖邏輯

換句話說，`main.py` 是框架；`shape_demos/*.py` 才是每一種效果的實作。

## 每個 demo 必備的方法

每個 demo 類別至少都要提供這幾個方法：

### 1. `calculate_demo_point(...)`

負責把目前角度換成畫面上的代表點，並回傳側邊資訊文字。

### 2. `draw_reference_shape(...)`

負責畫該模式的主要圖形，例如：

- 圓
- 橢圓
- 雲層
- 火焰底座

### 3. `formula_value_for_graph(...)`

回傳右側函數圖在某個弧度下的值。

### 4. `formula_descriptions()`

回傳右側面板的標題和公式文字。

### 5. `status_text(...)`

回傳底部狀態列文字。

## 可選的擴充欄位

特效類型還可以額外加：

- `show_grid = False`
- `show_axes = False`
- `show_helpers = False`
- `show_vector = False`
- `show_point = False`
- `shape_subtitle = "..." `

這些欄位讓 `main.py` 可以共用同一套畫布，但不同 demo 可以決定自己要不要顯示格線、座標軸、向量等元素。

## 特效類型的額外方法：`draw_effect(...)`

如果某個 demo 不只是畫靜態輪廓，而是需要畫光暈、分支、火星之類的細節，就可以再提供：

```python
def draw_effect(self, painter, center_x, center_y, point_x, point_y, radians, angle_degrees):
    ...
```

`main.py` 會在適當時機自動呼叫它。

## 畫面流程

`GraphicsCanvas.paintEvent()` 的流程可以理解成：

1. 畫背景
2. 畫標題
3. 畫左側主視覺
4. 畫右側函數圖
5. 畫資訊框和底部狀態

其中左側主視覺又會繼續拆成：

1. `draw_reference_shape()`
2. `draw_effect()` 如果存在
3. 共用的資訊框

## 如果要新增一個 demo，步驟是什麼

1. 在 `shape_demos/` 新增一個類別檔案
2. 實作前面那五個必備方法
3. 如果需要，補 `draw_effect()` 和顯示旗標
4. 在 `shape_demos/__init__.py` 匯出
5. 在 `main.py` 加進 mode 常數、`MODE_LABELS`、`self.demos`、選單

## 這個框架的好處

- 左右面板共用同一套 UI
- 每個 demo 只專心寫自己的數學和畫法
- 想加新效果時，不需要重寫整個視窗

## 最值得記住的一句話

這個專案的框架精神是：

> `main.py` 管流程，`shape_demos/*.py` 管數學與效果。
