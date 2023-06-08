# Tarif: Group 0, Jahressonderzahlung 1, Erfarungsstufegehalt 2-7, Personalvollkosten 8, Ballungszulage 9, Arzt 10

# 1-9e = 132.50 Euro zus,
# tarif = {'Sekretariat (TV-L E6)': ['e6', 88.14,
#                                    2651.42, 2864.88, 2983.94, 3105.46, 3185.24, 3271.18,
#                                    76012.00, True, False],

#          'Gehobener Dienst (TV-L E8)': ['e8', 88.14,
#                                         2866.21, 3087.04, 3209.79, 3326.44, 3455.35, 3535.15,
#                                         82957.00,True, False],

#          'Techniker(in) (Meister, TV-L E9a)': ['e9a', 74.35,
#                                                3051.16, 3277.32, 3326.44, 3424.65, 3831.78, 3945.49,
#                                                85828.00,True, False
#                                                ],
#          'Techniker(in) (Bachelor, TV-L E9b)': ['e9b', 74.35,
#                                                 3051.16, 3277.32, 3424.65, 3831.78, 4178.10, 4303.46,
#                                                 85828.00, True, False
#                                                 ],
#          'Techniker(in) (Bachelor, TV-L E10)': ['e10', 74.35,
#                                                 3427.65, 3662.23, 3930.82, 4204.82, 4726.15, 4867.94,
#                                                 92060.00, False, False
#                                                 ],
#          'Techniker(in) (Bachelor, TV-L E11)': ['e11', 74.35,
#                                                 3553.15, 3792.20, 4064.48, 4478.85, 5080.35, 5232.76,
#                                                 103777.00, False, False
#                                                 ],
#          'Wissenschaftler(in) FH (TV-L E12)': ['e12', 46.47,
#                                                3672.04, 3930.82, 4478.85, 4960.05, 5581.59, 5749.03,
#                                                117635.00, False, False
#                                                ],
#          'Wissenschaftler(in) (TV-L E13)': ['e13', 46.47,
#                                             4074.30, 4385.28, 4619.20, 5073.66, 5701.88, 5872.94,
#                                             123818.00, False, False
#                                             ],
#          'leitende(r) Wissenschaftler(in) (TV-L E14)': ['e14', 32.53,
#                                                         4418.91, 4752.85, 5026.88, 5441.24, 6076.14, 6258.43,
#                                                         136261.00, False, False
#                                                         ],
#          'leitende(r) Wissenschaftler(in) (TV-L E15)': ['e15', 32.53,
#                                                         4880.65, 5247.42, 5441.24, 6129.64, 6650.92, 6850.45,
#                                                         151880.00, False, False
#                                                         ],
#          'Ärztin/Arzt mit entsprechender Tätigkeit': ['ä1', None,
#                                                       4841.95,
#                                                       5116.40,
#                                                       5312.43,
#                                                       5652.24,
#                                                       6057.34,
#                                                       6215.35,
#                                                       None, False, True],
#          'Fachärztin/Facharzt mit entsprechender Tätigkeit': ['ä2', None,
#                                                               6390.60,
#                                                               6926.42,
#                                                               7396.90,
#                                                               7661.27,
#                                                               7805.40,
#                                                               8004.59, None, False, True],

#          'Oberärztin/Oberarzt': ['ä3', None,
#                                  8004.59,
#                                  8475.07,
#                                  9148.09, None, None, None, None, False, True],

#          'Fachärztin/Facharzt, der/dem die ständige Vertretung des leitenden Arztes (Chefarzt) vom Arbeitgeber übertragen worden ist': [
#              'ä4', None,
#              9416.03,
#              10089.04,
#              10624.85, None, None, None, None, False, True]
#          }

drm_geber = ['DFG Normalverfahren',
             'Bayerische Ministerien (StMWIVT, StMWFK, ...)',
             'Bayerische Forschungsstiftung',
             'Bundesministerien (BMBF, BMWi,...)',
             'EU',
             'Industrie/Privat',
             'sonst. öffentl. Gelder',
             'sonst. öffentl. Gelder mit Personalvollkosten',
             'Betriebseinnahmen'
             ]

drm_geber_spec = {
    "Industrie/Privat": 0.25,
    "sonst. öffentl. Gelder mit Personalvollkosten": 0.1,
    "Betriebseinnahmen": 0.1275
}

stufe = ['Stufe 1 (0 Erfahrungsjahre)',
         'Stufe 2 (1 Erfahrungsjahre)',
         'Stufe 3 (3 Erfahrungsjahre)',
         'Stufe 4 (6 Erfahrungsjahre)',
         'Stufe 5 (10 Erfahrungsjahre)',
         'Stufe 6 (15 Erfahrungsjahre)'
         ]
