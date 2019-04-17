test = {
  'name': 'Question',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Hint 1: To understand how this question works, first set
          >>> #   you = 'fi'
          >>> # and add the line
          >>> #   print('beeper'.replace('p', you))
          >>> # and you should see the word "beefier" appear as the first output.
          >>> #
          >>> # Hint 2: Just by changing you, you can create a word with two
          >>> # double letters in a row: beekeeper
          >>> type(you) == str
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # You can make the word beekeeper by assigning
          >>> #   you = 'keep'
          >>> 'beeper'.replace('p', you)[::-1]
          'repeekeeb'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # The word you're trying to make is "bookkeeper"!
          >>> #
          >>> # To change "beekeeper" to "bookkeeper", change the "bee" to "book".
          >>> #   this = 'book'
          >>> 'beeper'.replace('p', you).replace('bee', this)[::-1]
          'repeekkoob'
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
