#!/usr/bin/env python

### A script to visualise the read counts for runs ###

import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import argparse
import glob

def read_count_visualisation(sample_sheet, list_of_demultiplex_stats):
	dfs = {}
	for demultiplex_stat in list_of_demultiplex_stats:
		dfs[demultiplex_stat] = pd.read_csv(demultiplex_stat)
#         print('{0} = {1}'.format(csv, location))
#         print(sample_sheet)
	main_df = dfs[list(dfs.keys())[0]][['SampleID', 'Index', '# Reads']]
	main_df = main_df.rename(columns={'SampleID': 'sample_id', 'Index': 'index', '# Reads': 'reads_lane_{lane}'.format(lane=dfs[list(dfs.keys())[0]]['Lane'][0])})
	main_df['total'] = main_df['reads_lane_{lane}'.format(lane=dfs[list(dfs.keys())[0]]['Lane'][0])]
	for i in list(dfs.keys())[1:]:
#         print(dfs[i]['Lane'][0])
		main_df['reads_lane_{lane}'.format(lane=dfs[i]['Lane'][0])] = pd.Series(dfs[i]['# Reads'])
		main_df['total'] += dfs[i]['# Reads']
	 
	main_df = main_df[main_df.sample_id != 'Undetermined']
	# print(main_df)
#     print(dfs['lane_two'])
#     for i in list(dfs.keys()):
#         print(i)
#     print(dfs['lane_one']['Lane'][0])
#     print(dfs)
		
	with open(sample_sheet,'r') as f:
		for num, line in enumerate(f):
		 # check if the current line
		 # starts with "[Data]"
			if line.startswith("[Data]"):
#             print(num, line)
				df_without_header = pd.read_csv(sample_sheet, skiprows=num+1)
	df_without_header = df_without_header[['Sample_ID', 'Sample_Plate']]
	df_without_header = df_without_header.rename(columns={'Sample_ID': 'sample_id', 'Sample_Plate': 'worksheet_id'})
#     print(df_without_header)
	merged_df = pd.merge(left=main_df, right=df_without_header, left_on=['sample_id'], right_on=['sample_id'], how='left')
#     print(merged_df)
	worksheet_ids = merged_df.worksheet_id.unique()
#     print(worksheet_ids)
	group_by_worksheet_df = merged_df.groupby(merged_df.worksheet_id)
	for worksheet in worksheet_ids:
		sub_df = group_by_worksheet_df.get_group(worksheet).sort_values(by=['sample_id'])
		g = sns.FacetGrid(sub_df, col="worksheet_id", col_wrap=1, height=10, aspect=1.5)
		g.map_dataframe(sns.barplot, x="sample_id", y="total")
		g.set(ylim=(0, 200000000))
		g.set_axis_labels("Sample ID", "Total Reads")
		g.set_xticklabels(rotation=45) 
		g.savefig('read_count_{worksheet}.png'.format(worksheet=worksheet))

#read_count_visualisation(lane_one = "Lane_1/Demultiplex_Stats.csv", lane_two = "Lane_2/Demultiplex_Stats.csv",  sample_sheet = "SampleSheet_combined.csv")


if __name__ == '__main__':

	############# Get path of where this needs to be run from Erik ###################
	# sample_sheet = glob.glob('Demultiplex_Output/Logs_Intermediates/FastqGeneration/SampleSheet_combined.csv')
	demultiplex_stats = glob.glob('Demultiplex_Output/Logs_Intermediates/FastqGeneration/Reports/Lane*/Demultiplex_Stats.csv')
	sample_sheet = 'Demultiplex_Output/Logs_Intermediates/FastqGeneration/SampleSheet_combined.csv'
	# print(demultiplex_stats)

	# pass

	# parser = argparse.ArgumentParser(description='Visualise read counts for each lane on run.')

	# parser.add_argument('--csv_file', nargs='+', help='Each csv file per lane', required=True)

	# parser.add_argument('--sample_sheet', nargs=1, type=str, help='Sample sheet csv', required=True)

	# args = parser.parse_args()

	# csv_file = args.csv_file

	# sample_sheet = args.sample_sheet[0]

	# read_count_visualisation(sample_sheet, lane=csv_file)

	# print(' '.join(csv_file), sample_sheet)
	# print(str(sample_sheet))
	# print(csv_file)


	read_count_visualisation(sample_sheet, demultiplex_stats)




