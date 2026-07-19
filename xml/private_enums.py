from enum import Enum, auto


class Result(Enum):
    SUCCESS = auto()
    FAIL = auto()


class SeqTrend(Enum):
    ERROR = auto
    CONSTANT = auto()
    INCREASE = auto()
    DECLINE = auto()
    UNKNOWN = auto
    OSCILLATING = auto()


if __name__ == '__main__':
    rst1 = Result.SUCCESS
    rst2 = Result.SUCCESS
    rst3 = Result.FAIL
    rst4 = SeqTrend.INCREASE
    print(rst3 == rst4)
    print(rst3.value)
    print(rst4.value)

