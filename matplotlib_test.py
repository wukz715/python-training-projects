# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt


def curve():
    squares = [1, 4, 9, 16, 25]
    plt.plot(squares, linewidth=5)

    plt.title("Square Numbers", fontsize=24)
    plt.xlabel("Value", fontsize=14)
    plt.ylabel("Square of Value", fontsize=14)

    plt.tick_params(axis='both', labelsize=12)
    plt.show()

def scattered_point():
    x_values = list(range(1, 101))  # 区分list()和range()
    y_values = [x ** 2 for x in x_values]

    plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, edgecolors='none', s=40)
    plt.title("Square Numbers", fontsize=24)
    plt.xlabel("Value", fontsize=14)
    plt.ylabel("Square of Value", fontsize=14)
    plt.tick_params(axis="both", labelsize=14)
    plt.axis([0, 110, 0, 11000])
    plt.show()
    #需要注释show()函数才能够打印成功
    # plt.savefig('squares_plot.png', bbox_inches='tight')


if __name__ == "__main__":
    curve()
    scattered_point()