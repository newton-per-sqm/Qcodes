import re

from qcodes.instrument.group_parameter import GroupParameter, Group
from qcodes import Instrument


class Dummy(Instrument):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        self._a = 0
        self._b = 0

        self.add_parameter(
            "a",
            get_parser=int,
            parameter_class=GroupParameter
        )

        self.add_parameter(
            "b",
            get_parser=int,
            parameter_class=GroupParameter
        )

        Group(
            [self.a, self.b],
            set_cmd="CMD {a}, {b}",
            get_cmd="CMD?"
        )

    def write(self, cmd: str) -> None:
        result = re.search("CMD (.*), (.*)", cmd)
        assert result is not None
        self._a, self._b = [int(i) for i in result.groups()]

    def ask(self, cmd: str) -> str:
        assert cmd == "CMD?"
        return ",".join([str(i) for i in [self._a, self._b]])


def test_sanity():
    """
    Test that we can individually address parameters "a" and "b", which belong
    to the same group.
    """
    dummy = Dummy("dummy")

    assert dummy.a() == 0
    assert dummy.b() == 0

    dummy.a(3)
    dummy.b(6)

    assert dummy.a() == 3
    assert dummy.b() == 6

    dummy.b(10)
    assert dummy.a() == 3
    assert dummy.b() == 10
