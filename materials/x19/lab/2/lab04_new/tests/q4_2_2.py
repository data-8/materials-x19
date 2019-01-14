test = {
  'name': 'Question 4.2.3',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> sorted(summed_mn_data.labels) == ['Condition', 'Died sum', 'Participated sum']
          True
          >>> sorted(summed_mn_data.column('Condition')) == ['Control', 'Diet']
          True
          >>> sum(summed_mn_data.column('Died sum'))
          467
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
