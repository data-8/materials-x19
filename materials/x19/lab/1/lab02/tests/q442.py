test = {
  'name': '',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> all(np.round(annual_growth_rates, 3) == np.round((changed/initials)-1, 3))
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
