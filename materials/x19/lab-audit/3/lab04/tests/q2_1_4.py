test = {
  'name': '2.1.4',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> set(close_songs.labels) >= {'Genre', 'Artist', 'Title', 'like', 'love'}
          True
          >>> close_songs.num_rows == 7
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> [title[:8] for title in close_songs.column('Title')]
          ['If This ', 'Big Red ', 'In the M', 'The Hard', 'One Time', 'This Tor', 'You Can ']
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
