test = {
  'name': 'Question',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Try assigning start to a negative integer based on founded.
          >>> #   start = int(founded.replace('BC ', '-'))
          >>> start in (-753, -752)
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Try assigning end to a positive integer based on sacked.
          >>> # You can replace some part of a string with nothing.
          >>> #   end = int(sacked.replace('AD ', ''))
          >>> end in (409, 410)
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> end-start in (1163, 1162)
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
