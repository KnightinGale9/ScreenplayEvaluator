from matplotlib import pyplot as plt
import pandas as pd
from pycorenlp import StanfordCoreNLP
from CodeBase.Evaluator import Evaluator
import json
import regex as re
class CharacterGender(Evaluator):
    """
     An evaluator that generates a separate character legend file for improved readability of the characters
     in the screenplay along with their corresponding colors.
    """

    def run_evaluator(self):
        self.find_gender()
        self.write_charcter_gender()
        print("Character Gender",end="")

    def find_gender(self):
        self.gender_dict = {key: 'UNKNOWN' for key in self.scraper.get_characterdict()}
        nlp = StanfordCoreNLP('http://localhost:9000')
        gender_found=set()
        for idx, row in self.scraper.get_fulldf().iterrows():
            output = nlp.annotate(row['text'], properties={
                'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,coref',
                'outputFormat': 'json'
            })
            output = json.loads(output)

            # print(type(output['corefs']))

            for cluster,mention in output['corefs'].items():
                df = pd.DataFrame(mention)
                character_names = list(self.scraper.get_characterdict().keys())

                # Create regex pattern: 'Indy|Marion|Jones'
                pattern = '|'.join(re.escape(name) for name in character_names)

                # Filter rows containing any of the names
                matches = df[df['text'].str.contains(pattern, case=False, na=False)]

                # Now check which specific names matched
                matched_characters = [
                    name for name in character_names
                    if matches['text'].str.contains(name, case=False, na=False).any()
                ]
                if len(matched_characters) == 1 and matched_characters[0] not in gender_found:
                # print(df)
                    gender_count= df['gender'].value_counts()
                    # print(gender_count)
                    if 'MALE' in gender_count and 'FEMALE' in gender_count:
                        male_count = gender_count['MALE']
                        female_count = gender_count['FEMALE']
                        if male_count>female_count:
                            print("MALE count:", male_count)
                            self.gender_dict[matched_characters[0]]="MALE"
                            gender_found.add(matched_characters[0])
                        else:
                            print("FEMALE count:", female_count)
                            self.gender_dict[matched_characters[0]]="FEMALE"
                            gender_found.add(matched_characters[0])

                    elif 'MALE' in gender_count:
                        male_count = gender_count['MALE']
                        print(matched_characters,"MALE count:", male_count)
                        self.gender_dict[matched_characters[0]] = "MALE"
                        gender_found.add(matched_characters[0])
                    elif 'FEMALE' in gender_count:
                        female_count = gender_count['FEMALE']
                        print(matched_characters,"FEMALE count:", female_count)
                        self.gender_dict[matched_characters[0]] = "FEMALE"
                        gender_found.add(matched_characters[0])
                    else:
                        continue
                    print(gender_count)

    def write_charcter_gender(self):
        csvoutput = pd.DataFrame(list(self.gender_dict.items()), columns=['Name', 'Gender'])
        csvoutput.to_csv(f'{self.scraper.get_output_dir()}/{self.replace_file_extension("-character_gender.csv")}')

    def get_json_data(self):
        """
        Returns the evaluation data in a JSON-compatible format for the file Screenplay_Raw_data.json.

        :return: vocab_growth.
        """
        return {"Gender": self.gender_dict}