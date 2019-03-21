test = {
  'name': 'Question 3_2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> abs(np.mean(resample_yes_proportions) - .525) < .1 and np.std(resample_yes_proportions) < .1
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
