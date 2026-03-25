# Skew Ellipse 數學教學

## 為什麼這一份比較重要

`Skew Ellipse` 是從「單純伸縮」進一步走到「旋轉混合」。這也是專案裡第一個真正用到座標變換概念的 demo。

## 原本的橢圓公式

未旋轉的橢圓：

$$
x = a\cos(t)
$$

$$
y = b\sin(t)
$$

如果只是畫在原點附近，這樣就夠了。

## 加上旋轉角度 $\phi$

把橢圓整體旋轉 $\phi$ 之後，座標會變成：

$$
x = a\cos(t)\cos(\phi) - b\sin(t)\sin(\phi)
$$

$$
y = a\cos(t)\sin(\phi) + b\sin(t)\cos(\phi)
$$

這其實就是把原本的 $(x, y)$ 再乘上一個 2D 旋轉矩陣。

## 對應到這個專案

在 `skew_ellipse_demo.py` 裡：

- `a = 140`
- `b = 95`
- `phi = 60°`

所以畫面上的點是：

$$
x = c_x + a\cos(t)\cos(\phi) - b\sin(t)\sin(\phi)
$$

$$
y = c_y - \left(a\cos(t)\sin(\phi) + b\sin(t)\cos(\phi)\right)
$$

注意第二式在畫到螢幕上時仍然要做 `center_y - y_offset`。

## 右側圖在畫什麼

右邊不是把整個旋轉橢圓都重畫一次，而是抽出它的垂直分量：

$$
y(t) = a\cos(t)\sin(\phi) + b\sin(t)\cos(\phi)
$$

程式裡又再除以 `a` 做正規化，讓波形比較好放進同一塊圖：

$$
\frac{a\cos(t)\sin(\phi) + b\sin(t)\cos(\phi)}{a}
$$

## 這個公式在教什麼

最重要的是：

- 原本只屬於 `x` 的 `cos(t)`，開始影響 `y`
- 原本只屬於 `y` 的 `sin(t)`，也開始混進另一個軸

這就是 2D 旋轉最關鍵的觀念：不同軸的資訊會互相混合。

## 你可以學到什麼

- `Skew Ellipse` 的本質其實是旋轉後的參數方程
- 一旦開始做旋轉，`x` 和 `y` 就不能再獨立思考
- 這個概念之後會一路延伸到矩陣、變換、動畫與遊戲物件座標
