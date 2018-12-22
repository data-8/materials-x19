test = {
  'name': 'Question 1.2.3',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> from collections import Counter
          >>> def check(r):
              t = test_20.row(r)
              return classify(t, train_20, train_lyrics.column('Genre'), 5) == classify_one_argument(t)
          >>> check(0)
          True
          >>> check(1)
          True
          >>> check(2)
          True
          >>> check(3)
          True
          >>> check(4)
          True
          >>> check(5)
          True
          >>> check(6)
          True
          >>> check(7)
          True
          >>> check(8)
          True
          >>> check(9)
          True
          >>> check(10)
          True
          """,
          'hidden': False,
          'locked': False
        },
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
