test = {
  'name': 'Question 2_2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Correlation is a number between -1 and 1
          >>> -1 <= r <= 1
          True
          >>> #It appears that you implemented std_units, but did so incorrectly
          >>> std_units(np.arange(5)) is None or np.allclose(std_units(np.arange(5)), [-1.41421356, -0.70710678,  0,  0.70710678,  1.41421356])
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
