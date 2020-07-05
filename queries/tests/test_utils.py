from queries import utils


def test_get_words():
    data = [
        {'title': 'alfa, :beta;   gamma.'},
        {'title': 'Alfa, deltA.'},
        {'title': 'BETA -+= ! ;; 123 OMEGa...'}
    ]

    popular_words = utils._get_words(data)

    assert popular_words == [
        ('alfa', 2),
        ('beta', 2),
        ('gamma', 1),
        ('delta', 1),
        ('omega', 1)
    ]

