test = {
  'name': 'Question 5_1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # The array should have length 2
          >>> len(coin_model_probabilities) == 2
          True
          >>> # The elements in the array should add up to 1.
          >>> sum(coin_model_probabilities) == 1
          True
          """,
          'hidden': False,
          'locked': True
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
