test = {
  'name': '5.1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Use .select("Row Labels", "1970") to select the two columns.
          >>> top_1970.labels == ("Row Labels", "1970")
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Use .sort("1970", descending=True) to sort in descreasing order.
          >>> print(top_1970.take(0))
          Row Labels    | 1970
          United States | 11
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
