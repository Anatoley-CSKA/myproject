def calc_avg(my_list):
    if not my_list:
        return 0
    return sum(my_list) / len(my_list)


if __name__ == "__main__":
    assert calc_avg([1, 2, 3, 4]) == 2.5
    print(calc_avg([1, 2, 3, 4]))
