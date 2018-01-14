import pandas as pd

class sorts:

    def __init__(self):
        pass

    def sorting(review, res):
		df_sample = res
		df_sample = df_sample[df_sample['expired']==False]
		df_sample['formattedRelativeTime'] = df_sample['formattedRelativeTime'].map(lambda x: str(x)[:2])
		df_sample['formattedRelativeTime'] = df_sample['formattedRelativeTime'].astype(str).astype(int)
		#df_sample = df_sample[['city', 'company', 'formattedRelativeTime']]
		if review == 'Date':
			df_sample = df_sample.sort_values(['formattedRelativeTime'], ascending=True)
			return df_sample
		else:
			df = pd.read_csv('RatingFinal.csv')
			criteria_list = ['Overall', 'Work Life Balance', 'Compensation', 'Job Security',
							 'Management', 'Culture', 'CEO Approval']
			if review == "":
				df = df.sort_values(['Overall'], ascending=False)
			elif review in criteria_list:
				df = df.sort_values([review], ascending=False)
			else:
				df = df.sort_values(['Overall'], ascending=False)

			df_sample = df_sample.sort_values(['formattedRelativeTime'], ascending=True)
			df_final = pd.merge(df, df_sample, on='company', how='inner')
			del df_final['Unnamed: 0']
			del df_final['source']
			del df_final['stations']
			del df_final['sponsored']
			del df_final['state']
			del df_final['onmousedown']
			del df_final['language']
			del df_final['expired']
			del df_final['country']
			df_final = df_final.drop_duplicates(['company'])
			return df_final


