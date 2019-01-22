test = {
  'name': 'Question 1_2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> answer_cleaned_causes_by_year.sort("Year").select(sorted(answer_cleaned_causes_by_year.labels)).take(range(5))
          All Other Causes | Alzheimer's Disease | Cerebrovascular Disease (Stroke) | Chronic Liver Disease and Cirrhosis | Chronic Lower Respiratory Disease (CLRD) | Diabetes Mellitus | Diseases of the Heart | Intentional Self Harm (Suicide) | Malignant Neoplasms (Cancers) | Pneumonia and Influenza | Unintentional Injuries | Year
          38392            | 3934                | 18079                            | 3546                                | 13187                                    | 6004              | 69900                 | 3047                            | 52880                         | 8014                    | 8940                   | 1999
          39259            | 4398                | 18090                            | 3673                                | 12754                                    | 6203              | 68533                 | 3113                            | 53005                         | 8355                    | 8814                   | 2000
          38383            | 4897                | 18078                            | 3759                                | 13056                                    | 6457              | 69004                 | 3256                            | 53810                         | 8167                    | 9274                   | 2001
          41177            | 5405                | 17551                            | 3725                                | 12643                                    | 6783              | 68387                 | 3210                            | 53926                         | 8098                    | 9882                   | 2002
          40325            | 6585                | 17686                            | 3832                                | 13380                                    | 7088              | 69013                 | 3396                            | 54307                         | 8184                    | 10470                  | 2003
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
