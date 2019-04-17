test = {
  'name': '',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> 54.9 < two_minute_predicted_waiting_time and 55 > two_minute_predicted_waiting_time
          True
          >>> 87.1 < five_minute_predicted_waiting_time and 87.2 > five_minute_predicted_waiting_time
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
