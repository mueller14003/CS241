class Time:
    def __init__(self):
        self._seconds = 0
        self._minutes = 0
        self._hours = 0

    @property
    def hours(self):
        if self._hours < 0:
            return 0
        elif self._hours > 23:
            return 23
        else:
            return self._hours

    @hours.setter
    def hours(self, value):
        if value < 0:
            self._hours = 0
        elif value > 23:
            self._hours = 23
        else:
            self._hours = value

    @property
    def hours_simple(self):
        if self._hours < 1:
            return 12
        elif self._hours > 12:
            return self._hours % 12
        else:
            return self._hours

    @property
    def period(self):
        if self._hours < 12:
            return "AM"
        else:
            return "PM"

    @property
    def minutes(self):
        if self._minutes < 0:
            return 0
        elif self._minutes > 59:
            return 59
        else:
            return self._minutes

    @minutes.setter
    def minutes(self, value):
        if value < 0:
            self._minutes = 0
        elif value > 59:
            self._minutes = 59
        else:
            self._minutes = value

    @property
    def seconds(self):
        if self._seconds < 0:
            return 0
        elif self._seconds > 59:
            return 59
        else:
            return self._seconds

    @seconds.setter
    def seconds(self, value):
        if value < 0:
            self._seconds = 0
        elif value > 59:
            self._seconds = 59
        else:
            self._seconds = value

    @property
    def seconds_m(self):
        return self._seconds

    @seconds_m.setter
    def seconds_m(self, seconds):
        self._seconds = seconds % 60

    @property
    def hours_m(self):
        return self._hours

    @hours_m.setter
    def hours_m(self, seconds):
        self._hours = seconds // 3660

    @property
    def minutes_m(self):
        return self._minutes

    @minutes_m.setter
    def minutes_m(self, seconds):
        self._minutes = seconds // 60 - (60 * (seconds // 3660))


def display(t):
    print("\nMilitary Time:")
    print("{:02d}:{:02d}:{:02d}".format(t.hours, t.minutes, t.seconds))
    print("\nNormal Time:")
    print("{:02d}:{:02d}:{:02d} {}\n".format(t.hours_simple, t.minutes, t.seconds, t.period))


def prompt_and_set_normal(t):
    t.hours = int(input("Enter hours: "))
    t.minutes = int(input("Enter minutes: "))
    t.seconds = int(input("Enter seconds: "))
    return t


def prompt_and_set_midnight(t):
    seconds = int(input("Enter seconds since midnight: "))
    t.seconds_m = seconds
    t.minutes_m = seconds
    t.hours_m = seconds
    return t


def main():
    t = Time()

    print("Initial Time:")
    display(t)
    t = prompt_and_set_normal(t)
    display(t)
    t = prompt_and_set_midnight(t)
    display(t)


if __name__ == "__main__":
    main()
