import sys
sys.stdout.reconfigure(encoding='utf-8')

# 你的代码
print("你好，世界")  # 示例中文输出

print(sys.version)
from decimal import Decimal, getcontext

for i in range(1, 10):
    for j in range(1, i + 1):


        print(f"{j}*{i}={i*j}", end="\t")
    print()

    getcontext().prec = 31  # Set precision to 31 to ensure 30 decimal places
    pi = Decimal(0)
    k = 0

    while k < 1000:  # Increase the range for better accuracy
        pi += (Decimal(1) / (16 ** k)) * (
            Decimal(4) / (8 * k + 1) -
            Decimal(2) / (8 * k + 4) -
            Decimal(1) / (8 * k + 5) -
            Decimal(1) / (8 * k + 6)
        )
        k += 1

    print(f"圆周率计算,保留小数点后30位: {pi}")

    print("百家讲坛")