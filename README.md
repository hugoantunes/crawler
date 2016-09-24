# poker

This project contains an implementation in python of a poker hand.

There is no external dependencies only built in libraries were used.

## to run tests:
```bash
make tests
```

## to use:

- possible numbers:
```python
NUMBERS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
```

- possible suits:
```python
SUITS = ['H', 'S', 'D', 'C']
```

```python
In [1]:from hand import Hand

In [2]: my_hand = Hand.from_string('4D 4D 4S 7H 8D')
In [2]: print my_hand
<hand ['4D', '4D', '4S', '7H', '8D'], THREE_OF_A_KIND>

In [3]:other_hand = Hand.from_string('AD AD AS KH 2D')
In [4]:print other_hand
<hand ['AD', 'AD', 'AS', 'KH', '2D'], THREE_OF_A_KIND>

In [5]: print 'I won! =D' if my_hand > other_hand else 'I lost =('
I lost =(
```