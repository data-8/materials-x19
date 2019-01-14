test = {
  'name': 'Question 1.2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Make sure the columns are correct
          >>> list(causes_for_plotting.labels) == ['Year'] + sorted(all_unique_causes)
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
