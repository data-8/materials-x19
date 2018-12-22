test = {
  'name': 'Question 2.6',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> reject_null in [False, True]
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> which_side in ["Right", "Left"]
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> reject_null
          False
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> which_side
          'Right'
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
