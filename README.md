# Challenge1
The first challenge in the class, using string matching query on data from Wikipedia

As the data files are to large to include here. We downloaded <b>enwiki-20170820-pages-articles-multistream.xml.bz2</b> found here https://meta.wikimedia.org/wiki/Data_dump_torrents

From that you can decompress and create "wiki_big" which you will have to parse using <b>parse_wiki.py</b> to be able to get "wiki_cat", "wiki_only_a" and "wiki_all".

Once you have those files you are able to run <b>query.py</b> and find some queries

# Note!
## parse_wiki.py
In order to run <b>parse_wiki.py</b> without errors please edit lines:

* Line 9  :   Define the case
* Line 24 :   Path to the folder where the big_wiki file is to be read
* Line 25 :   The name of the xml file of the wiki

Also, some of our members did have memory or clock-rate issues when running the parser for very large files.
## query.py
Make sure you have the newest regex package installed <br>
In order to run <b>query.py</b> without errors please edit lines:

* Line 130  :   The path to the folder where the data is
* Line 131  :   The name of the file you want to read in
* Line 137  :   The query you want to search for

