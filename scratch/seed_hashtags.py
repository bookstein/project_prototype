"""Get hashtags from existing dataset - polarization study - 8000 political hashtags"""

import csv
import model

def load_hashtags():
	"""
	Load 'edgelist' tab-separated file, create list of all appearing hashtags.

	Output:
	-------
	A list of all hashtags that appear in the data.

	all.edgelist is data from ICWSM "Polarization on Twitter" study.
	"""
   	with open("./data/polarization/icwsm_polarization/all.edgelist") as f:
   		hashtag_reader = csv.reader(f, delimiter="\t")
   		hashtag_list = []
   		for row in hashtag_reader:
   			hashtags = row[5:]
   			for hashtag in hashtags:
   				hashtag = hashtag[1:]
				hashtag_list.append(hashtag)
		# print hashtag_list
   		return hashtag_list

def make_features_dict(hashtag_list):
	"""
	Using list of hashtags from data, create a dictionary that counts
	hashtag occurrences within the dataset.

	Sort the dictionary by frequency and append hashtags to a list of sorted hashtags.

	Output:
	------
	A list of hashtags, with more popular hashtags earlier in the list.

	"""
	hashtag_dictionary = {}
	for hashtag in hashtag_list:
		hashtag_dictionary[hashtag] = hashtag_dictionary.get(hashtag, 0) + 1


	sorted_hashtags = []
	for (hashtag, frequency) in sorted(hashtag_dictionary.iteritems(), key=lambda x: x[1], reverse=True):
		sorted_hashtags.append(hashtag)

	# print "HASHTAG LIST LENGTH ", len(sorted_hashtags)

	return sorted_hashtags

def hashtags_to_database(hashtags, session):
	"""
	Create tag from PoliticalHashtag class, save to database.

	Creates rows of hashtags with a unique id in the database. Hashtags stored earlier
	in the database were more frequently seen in the original dataset.

	Output:
	------
	Commits batch of hashtag objects to database.

	"""
	for hashtag in hashtags:
		tag = model.PoliticalHashtag()
		tag.text = hashtag
		session.add(tag)
	session.commit()

def main(session):
	hashtags = load_hashtags()
	dictionary = make_features_dict(hashtags)
	hashtags_to_database(dictionary, session)


if __name__ == "__main__":
	s = model.connect()
	main(s)
