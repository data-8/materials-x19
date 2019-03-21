test = {
  'name': 'Question 1_1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> "Cause of Death" in cleaned_causes.labels
          True
          >>> # It looks like you to do the third step 
          >>> # in dropping the abbreviations and renaming the description
          >>> "Cause of Death (Full Description)" not in cleaned_causes.labels
          True
          >>> len(np.unique(answer_cleaned_causes.group('Cause of Death').column(1)))
          1
          >>> int(np.unique(answer_cleaned_causes.group('Cause of Death').column(1).item(0)))
          22868
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
