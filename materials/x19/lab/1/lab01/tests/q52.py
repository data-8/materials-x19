test = {
  'name': '5.2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Use .select("Row Labels", "1970", "2009") to select the columns.
          >>> top_1970_with_2009.labels == ("Row Labels", "1970", "2009")
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Use .sort("1970", descending=True) to sort in descreasing order.
          >>> print(top_1970_with_2009.take(0))
          Row Labels    | 1970 | 2009
          United States | 11   | 13.7
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
