from typing import Any


def has(_filter: "filter[Any]") -> bool:
    return len(list(_filter)) > 0

if __name__ == "__main__":
    test_collection = ["a", "ab", "c", "d"]

    result = has(filter(lambda elem: elem.startswith('a'), test_collection))
    print(f"{result=}")