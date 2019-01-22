test = {
  'name': 'Question 1.3',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> death_penalty_murder_rates.num_rows
          1936
          >>> death_penalty_murder_rates.labels
          ('State', 'Year', 'Population', 'Murder Rate')
          >>> death_penalty_murder_rates.column(2).item(17)
          3690000
          >>> death_penalty_murder_rates.column(2).item(17)
          3690000
          >>> death_penalty_murder_rates.column(1).item(1738)
          1982
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
