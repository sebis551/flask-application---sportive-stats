"""
this is the docstring for data_ingestor
DataIngestor class where csv_file is stored

"""

import csv

class DataIngestor:
    """
    clasa dataingestor in care citesc csv_file si il pun intr-o lista de dictionare
    """
    def __init__(self, csv_path: str):

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

        print(csv_path)
        self.data = []
        #citesc csv ca un dictionar pentru a fi mai usor de parcurs
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            self.data2 = csv.DictReader(csv_file)

            for lines in self.data2:
                self.data.append(lines)

            line = self.data[0]
