from typing import List
from random import choice

from HDTFtypes import Header, HeaderPair

mttl = []


class Mutator:
    _name = 'mutatorBaseClass'

    @classmethod
    def mutate(cls, header: Header) -> None:
        pass


class keySpaceInsertionMutator(Mutator):
    _name = 'keySpaceInsertion'

    @classmethod
    def mutate(cls, header: Header) -> None:
        if len(header.header_list) == 0:
            return
        res = choice(header.header_list)
        res.key = ' ' + res.key


class valueSpaceInsertionMutator(Mutator):
    _name = 'valueSpaceInsertion'

    @classmethod
    def mutate(cls, header: Header) -> None:
        if len(header.header_list) == 0:
            return
        res = choice(header.header_list)
        res.value = ' ' + res.value


class keyWipeMutator(Mutator):
    _name = 'keyWipe'

    @classmethod
    def mutate(cls, header: Header) -> None:
        if len(header.header_list) == 0:
            return
        res = choice(header.header_list)
        res.key = ''


class valueWipeMutator(Mutator):
    _name = 'valueWipe'

    @classmethod
    def mutate(cls, header: Header) -> None:
        if len(header.header_list) == 0:
            return
        res = choice(header.header_list)
        res.value = ''


class pairDuplicateMutator(Mutator):
    _name = 'pairDuplicate'

    @classmethod
    def mutate(cls, header: Header) -> None:
        if len(header.header_list) == 0:
            return
        res = choice(header.header_list)
        header.header_list.append(HeaderPair(res.key, res.value))


mttl.append(keySpaceInsertionMutator)
mttl.append(valueSpaceInsertionMutator)
mttl.append(keyWipeMutator)
mttl.append(valueWipeMutator)
mttl.append(pairDuplicateMutator)


def get_mutator() -> List[Mutator]:
    return mttl.copy()
