import signal
import time

import pytest

from notebook_loader import last_notebook

oppgave = last_notebook("oppgave")


def med_tidsgrense(sekunder, funksjon, *args):
    """Kjører funksjonen og feiler testen hvis den bruker mer enn `sekunder`."""
    def avbryt(signum, frame):
        raise TimeoutError(f"brukte mer enn {sekunder} sekunder")
    gammel = signal.signal(signal.SIGALRM, avbryt)
    signal.setitimer(signal.ITIMER_REAL, sekunder)
    try:
        return funksjon(*args)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, gammel)


@pytest.mark.parametrize("n,fasit", [
    (0, False), (1, False), (2, True), (3, True), (4, False), (9, False),
    (17, True), (21, False), (25, False), (97, True), (7919, True), (7917, False),
])
def test_er_primtall(n, fasit):
    assert oppgave.er_primtall(n) == fasit


def test_er_primtall_stort_tall_er_raskt():
    assert med_tidsgrense(1, oppgave.er_primtall, 1_000_000_007) is True
    assert med_tidsgrense(1, oppgave.er_primtall, 1_000_000_007 * 3) is False


def test_primtall_under_30():
    assert oppgave.primtall_under(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_primtall_under_sma_verdier():
    assert oppgave.primtall_under(2) == []
    assert oppgave.primtall_under(3) == [2]


def test_primtall_under_en_million_er_raskt():
    primtall = med_tidsgrense(5, oppgave.primtall_under, 1_000_000)
    assert len(primtall) == 78498
    assert primtall[-1] == 999983


@pytest.mark.parametrize("n,fasit", [
    (2, [2]), (12, [2, 2, 3]), (97, [97]), (360, [2, 2, 2, 3, 3, 5]), (1024, [2] * 10), (9991, [97, 103]),
])
def test_primtallsfaktoriser(n, fasit):
    assert oppgave.primtallsfaktoriser(n) == fasit


def test_primtallsfaktoriser_stort_tall_er_raskt():
    assert med_tidsgrense(1, oppgave.primtallsfaktoriser, 600851475143) == [71, 839, 1471, 6857]
