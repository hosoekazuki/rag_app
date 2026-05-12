# 二分探索（Binary Search）

## 概要
ソート済み配列に対して、中央値と比較しながら探索範囲を半分に絞っていく探索アルゴリズム
時間計算量はO(log n)。

## 典型的なパターン

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left+right)/2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid+1
        else:
            right = mid-1
    return -1
```

## 注意点
- 配列がソート済みであることが前提
- left <= right の条件を忘れずに
- midの計算でオーバーフローに注意

## 関連問題
- LeetCode 704: Binary Search
- LeetCode 35: Search Insert Position