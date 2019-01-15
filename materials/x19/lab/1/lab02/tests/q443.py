test = {
  'name': '',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> all(annual_rates_over_ten_years == (ten_years/10)**(1/10) - 1)
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
