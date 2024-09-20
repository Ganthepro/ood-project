def generate_pairs(remaining):
    current_num = 0
    index = 0
    MAX_BUS = len(remaining)

    while any(x > 0 for x in remaining):
        if remaining[index] > 0:
            print((current_num, index), end=" ")
            remaining[index] -= 1
            current_num += 1

        # Move to the next index (cycle back to the start if needed)
        index = (index + 1) % MAX_BUS


def main():
    remaining = [1, 7, 9, 2]
    generate_pairs(remaining)


if __name__ == "__main__":
    main()
