from queries import utils


def test_get_words():
    data = [
        {'title': 'alfa, :beta;   gamma.', 'snippet': ' gamma'},
        {'title': 'Alfa, deltA.'},
        {'snippet': 'pi-. '},
        {'title': 'BETA -+= ! ;; 123 OMEGa...'},
    ]

    popular_words = utils._get_words(data)

    assert popular_words == [
        ('alfa', 2),
        ('beta', 2),
        ('gamma', 2),
        ('delta', 1),
        ('omega', 1),
        ('pi', 1),
    ]

