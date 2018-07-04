import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class Misescalations():

    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def filter_data(self):
        df = self.data
        self.failed_escalations = df.loc[df['Misescalations'] != 0]
        # print(failedEscalations)
        # print(len(failed_escalations.index))

        if (len(self.failed_escalations.index) != 0):
            # group the results
            self.grouped = self.failed_escalations.groupby('Agent_Name').apply(
                lambda x: x.sort_values('Agent_Name'))
            self.grouped.sort_index(ascending=False)
            # print(grouped)

            is_duplicate = pd.DataFrame(
                {'Duplicate_Agent_Name':
                    self.grouped.duplicated('Agent_Name')})
            # print(is_duplicate)
            self.result = pd.DataFrame(pd.concat(
                [self.grouped, is_duplicate], axis=1))
            # print(result)
        else:
            print('Lucky you! All was escalated correctly!')
            read_file()

    def write_failed_escalations_to_csv(self):

        result = self.result

        cols_to_keep = ['Ticket', 'Site_Code', 'week', 'Agent_Name',
                        'Manager_Name', 'Escalation CT', 'Closed_As',
                        'Escalations', 'Misescalations',
                        'Misescalations_Percent', 'Duplicate_Agent_Name']

        result[cols_to_keep].to_csv(
            self.filename + '_filtered.csv', sep='\t',
            encoding='utf-8', index=False)
        print("Selection grouped and sorted and saved to csv")

    def sort_agents_by_misescalation_fails(self):

        contact_type_max = pd.DataFrame(
            {'Ticket_Count': self.failed_escalations.groupby(
                ['Escalation CT']).size()}).sort_values(
                    'Ticket_Count', ascending=False).reset_index()
        contact_type_max['blank'] = ''

        self.misescalation = pd.DataFrame(
            {'Count': self.failed_escalations.groupby(
                ["Agent_Name"]).size()}).sort_values(
                    'Count', ascending=False).reset_index()

        self.misescalation_stat = pd.concat(
            [contact_type_max, self.misescalation], axis=1)
        self.misescalation_stat['Winners'] = ''
        return self.misescalation_stat

    def group_by_top_fail_agents(self):
        # personal rankings
        top_sinners = self.misescalation['Agent_Name'][:5]
        # print(type(top_sinners)) # series object
        # print(top_sinners)
        sinners_selection = pd.DataFrame(
            self.grouped.loc[self.grouped['Agent_Name'].isin(top_sinners)])
        # print(sinners_selection)
        sinners_selection['Counts'] = sinners_selection.groupby(
            ['Agent_Name'])['Agent_Name'].transform('count')
        # print(sinners_selection['Counts'])
        top_stars = pd.DataFrame(
            sinners_selection.groupby('Agent_Name').apply(
                lambda x: x.sort_values('Counts')))
        # the above 3 lines do not sort by quantity

        # print(top_stars)
        columns_to_keep = ['Ticket', 'Site_Code', 'week', 'Agent_Name',
                           'Manager_Name', 'Escalation CT', 'Closed_As']
        df = pd.DataFrame(top_stars[columns_to_keep]).reset_index(drop=True)
        df.rename(
            columns={'Agent_Name': 'Agent', 'Escalation CT': 'Escalation_CT'})
        frames = [self.misescalation_stat, df]

        self.winners = pd.concat(frames, axis=1)
        # print(self.winners)
        return self.winners

    def write_failed_groups_to_csv(self):

        self.winners.to_csv(
            self.filename + '_misescalations.csv', sep='\t',
            encoding='utf-8', index=False)
        print('Misescalation stat grouped and sorted and saved to csv')
        # plt.hist(misescalation_stat.Count, color = "skyblue")
        # plt.title(r'Histogram of Misescalations')
        # Tweak spacing to prevent clipping of ylabel
        # plt.subplots_adjust(left=0.15)
        # plt.show()

    def describe_data(self):

        df_describe = self.failed_escalations.apply(
            lambda x: x.describe(include='all'))
        df_description = pd.DataFrame(df_describe).T
        # print(df_description)
        df_description.to_csv(
            self.filename + '_describe.csv', sep='\t',
            encoding='utf-8')
        print("Dataset described and results saved to csv")


def read_file():
    filename = input("Type file name here: ")
    file = filename + ".csv"
    df = pd.read_csv(file)
    # print(df)
    return_list = [filename, df]
    return return_list


if __name__ == '__main__':
    while True:
        try:
            data = read_file()
            name = data[0]
            df = data[1]
            f = Misescalations(name, df)
            print(f)
            f.filter_data()
            f.write_failed_escalations_to_csv()
            f.sort_agents_by_misescalation_fails()
            f.group_by_top_fail_agents()
            f.write_failed_groups_to_csv()
            f.describe_data()

            # ask if want ot run again
            while True:
                answer = input('Run again? (y/n): ')
                if answer in ('y', 'n'):
                    break
                print ('Invalid input.')
            if answer == 'y':
                continue
            else:
                print ('Goodbye')
                break
        except FileNotFoundError:
            print('\n\tThere is no such file!\n')
