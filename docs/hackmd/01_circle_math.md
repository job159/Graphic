# Circle 數學教學

## 這份教學要解決什麼

`Circle` 是整個專案最核心的數學基礎。只要把這一份看懂，後面的橢圓、旋轉橢圓、閃電、火焰其實都只是「在圓的基礎上再加條件」。

## 主要公式

設圓心是 $(c_x, c_y)$，半徑是 $r$，角度是 $\theta$，那麼圓上的點可以寫成：

$$
x = c_x + r\cos(\theta)
$$

$$
y = c_y - r\sin(\theta)
$$

程式裡的 `-` 很重要，因為螢幕座標的 $y$ 軸是往下增加，但數學上我們通常把往上視為正方向。

## 對應到這個專案

在 `circle_demo.py` 裡：

- 半徑 `r = 140`
- `x = center_x + 140 * cos(theta)`
- `y = center_y - 140 * sin(theta)`

右側函數圖用的是：

$$
y = \sin(t)
$$

也就是說，右側其實是在單獨把「垂直投影」抽出來看。

## 為什麼是 `cos` 控制 x、`sin` 控制 y

在單位圓裡，角度 $\theta$ 對應的點就是：

$$
(\cos(\theta), \sin(\theta))
$$

如果半徑從 `1` 變成 `r`，就只要整體放大：

$$
(r\cos(\theta), r\sin(\theta))
$$

再把它平移到圓心 $(c_x, c_y)$ 就完成了。

## 角度和弧度

Python `math.sin()`、`math.cos()` 接受的是弧度，不是角度：

$$
\text{radian} = \text{degree} \times \frac{\pi}{180}
$$

所以程式裡會先做：

```python
radians = math.radians(angle_degrees)
```

## 用 30 度當例子

如果 $\theta = 30^\circ$：

- $\cos(30^\circ) \approx 0.866$
- $\sin(30^\circ) = 0.5$

所以點的位置會是：

$$
x = c_x + 140 \times 0.866
$$

$$
y = c_y - 140 \times 0.5
$$

這就是畫面上看到的向量終點。

## 你可以學到什麼

- 圓周運動其實就是 `sin`、`cos`
- 函數圖和幾何圖是同一件事的兩種視角
- 右邊的正弦波，不是額外的內容，而是左邊圓周運動的數學切片
