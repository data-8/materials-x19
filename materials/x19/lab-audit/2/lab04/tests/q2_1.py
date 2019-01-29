test = {
  'name': 'Question 2.1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> non_death_penalty_murder_rates.num_rows
          264
          >>> non_death_penalty_murder_rates.labels
          ('State', 'Year', 'Population', 'Murder Rate')
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> 0.25 <= run_test(non_death_penalty_murder_rates, 1971) <= 0.45
          Test statistic 1971 to 1973 : 1
          True
          >>> reject_null
          False
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
