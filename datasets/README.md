# Provenance datasets

This README will contain a brief summary of each dataset for the purposes of using them in experiments for Provenance as well as links to their original repos/papers. 

Each dataset is loaded as a list of dictionaries


## chroniclingAmericaQA

A list of dictionaries, with each entry:

```yaml
{
  'x_id': 'val_1',
  'question': 'How much of the crew would Gerry want to shore up in a gale of wind?',
  'answer': 'half',
  'context': "But my lads, it was right to put in federal officers last year, and the crew knew it; they saw what was brewing well enough, and by the soul of me, if the federal men hadn't done what they did, Old Davy Jones would have had his clutches into our quarters long ago. And now who d'ye think they want to put in instead of our present Commander C. GORE, and the Chief Mate COBB, an old weather-beaten Tar, and as stout a heart as ever broke bread—why I'll tell ye, d'ye see, one Gerry, who is too old and stiff to keep his legs in a calm, and in a gale of wind would want half of the crew to shore him up—aye, and one Billy Gray, as he's called, who to be sure, has been a clerk aboard some time, but never since his mother trotted him had any command, and by the powers never ought to have, for you all know, in squally weather, he'd skulk under the long boat, or turn in, and for the life of him daren't go aloft in a heavy sea to help reef a sail. Pretty business this! turn out old experienced officers to make way for them that can't rig a cat-tackle to get an anchor on the bow. No, it won't do. Faith my lads, we must keep a sharp look-out, and put a stopper on these fellows directly."

}

```

[data](https://huggingface.co/datasets/Bhawna/ChroniclingAmericaQA) | [paper](https://doi.org/10.1145/3626772.3657891) | [repo](https://github.com/DataScienceUIBK/ChroniclingAmericaQA)

## hotpotQA

A list of dicts, with each entry:

```yaml

{
    'x_id': '5a8b57f25542995d1e6f1371',
    'question': 'Were Scott Derrickson and Ed Wood of the same nationality?',
    'answer': 'yes',
    'context': [['Adam Collis',
   ['Adam Collis is an American filmmaker and actor.',
    ' He attended the Duke University from 1986 to 1990 and the University of California, Los Angeles from 2007 to 2010.',
    ' He also studied cinema at the University of Southern California from 1991 to 1997.',
    ' Collis first work was the assistant director for the Scott Derrickson\'s short "Love in the Ruins" (1995).',
    ' In 1998, he played "Crankshaft" in Eric Koyanagi\'s "Hundred Percent".']],
  ['Ed Wood (film)',
   ['Ed Wood is a 1994 American biographical period comedy-drama film directed and produced by Tim Burton, and starring Johnny Depp as cult filmmaker Ed Wood.',
    " The film concerns the period in Wood's life when he made his best-known films as well as his relationship with actor Bela Lugosi, played by Martin Landau.",
    ' Sarah Jessica Parker, Patricia Arquette, Jeffrey Jones, Lisa Marie, and Bill Murray are among the supporting cast.']],
  ['Tyler Bates',
   ['Tyler Bates (born June 5, 1965) is an American musician, music producer, and composer for films, television, and video games.',
    ' Much of his work is in the action and horror film genres, with films like "Dawn of the Dead, 300, Sucker Punch," and "John Wick."',
    ' He has collaborated with directors like Zack Snyder, Rob Zombie, Neil Marshall, William Friedkin, Scott Derrickson, and James Gunn.',
    ' With Gunn, he has scored every one of the director\'s films; including "Guardians of the Galaxy", which became one of the highest grossing domestic movies of 2014, and its 2017 sequel.',
    ' In addition, he is also the lead guitarist of the American rock band Marilyn Manson, and produced its albums "The Pale Emperor" and "Heaven Upside Down".']],
  ['Doctor Strange (2016 film)',
   ['Doctor Strange is a 2016 American superhero film based on the Marvel Comics character of the same name, produced by Marvel Studios and distributed by Walt Disney Studios Motion Pictures.',
    ' It is the fourteenth film of the Marvel Cinematic Universe (MCU).',
    ' The film was directed by Scott Derrickson, who wrote it with Jon Spaihts and C. Robert Cargill, and stars Benedict Cumberbatch as Stephen Strange, along with Chiwetel Ejiofor, Rachel McAdams, Benedict Wong, Michael Stuhlbarg, Benjamin Bratt, Scott Adkins, Mads Mikkelsen, and Tilda Swinton.',
    ' In "Doctor Strange", surgeon Strange learns the mystic arts after a career-ending car accident.']],
  ['Hellraiser: Inferno',
   ['Hellraiser: Inferno (also known as Hellraiser V: Inferno) is a 2000 American horror film.',
    ' It is the fifth installment in the "Hellraiser" series and the first "Hellraiser" film to go straight-to-DVD.',
    ' It was directed by Scott Derrickson and released on October 3, 2000.',
    " The film concerns a corrupt detective who discovers Lemarchand's box at a crime scene.",
    " The film's reviews were mixed."]],
  ['Sinister (film)',
   ['Sinister is a 2012 supernatural horror film directed by Scott Derrickson and written by Derrickson and C. Robert Cargill.',
    ' It stars Ethan Hawke as fictional true-crime writer Ellison Oswalt who discovers a box of home movies in his attic that puts his family in danger.']],
  ['Deliver Us from Evil (2014 film)',
   ['Deliver Us from Evil is a 2014 American supernatural horror film directed by Scott Derrickson and produced by Jerry Bruckheimer.',
    ' The film is officially based on a 2001 non-fiction book entitled "Beware the Night" by Ralph Sarchie and Lisa Collier Cool, and its marketing campaign highlighted that it was "inspired by actual accounts".',
    ' The film stars Eric Bana, Édgar Ramírez, Sean Harris, Olivia Munn, and Joel McHale in the main roles and was released on July 2, 2014.']],
  ['Woodson, Arkansas',
   ['Woodson is a census-designated place (CDP) in Pulaski County, Arkansas, in the United States.',
    ' Its population was 403 at the 2010 census.',
    ' It is part of the Little Rock–North Little Rock–Conway Metropolitan Statistical Area.',
    ' Woodson and its accompanying Woodson Lake and Wood Hollow are the namesake for Ed Wood Sr., a prominent plantation owner, trader, and businessman at the turn of the 20th century.',
    ' Woodson is adjacent to the Wood Plantation, the largest of the plantations own by Ed Wood Sr.']],
  ['Conrad Brooks',
   ['Conrad Brooks (born Conrad Biedrzycki on January 3, 1931 in Baltimore, Maryland) is an American actor.',
    ' He moved to Hollywood, California in 1948 to pursue a career in acting.',
    ' He got his start in movies appearing in Ed Wood films such as "Plan 9 from Outer Space", "Glen or Glenda", and "Jail Bait."',
    ' He took a break from acting during the 1960s and 1970s but due to the ongoing interest in the films of Ed Wood, he reemerged in the 1980s and has become a prolific actor.',
    ' He also has since gone on to write, produce and direct several films.']],
  ['The Exorcism of Emily Rose',
   ['The Exorcism of Emily Rose is a 2005 American legal drama horror film directed by Scott Derrickson and starring Laura Linney and Tom Wilkinson.',
    ' The film is loosely based on the story of Anneliese Michel and follows a self-proclaimed agnostic who acts as defense counsel (Linney) representing a parish priest (Wilkinson), accused by the state of negligent homicide after he performed an exorcism.']]],
    'supporting_facts': [['Scott Derrickson', 0], ['Ed Wood', 0]],
}

```

[data](https://huggingface.co/datasets/hotpotqa/hotpot_qa) | [paper](https://doi.org/10.48550/arXiv.1809.09600) | [repo](https://github.com/hotpotqa/hotpot)

## natural-questions

A list of dicts, with each entry:

```yaml
{
  'x_id': 5225754983651766092,
  'question': 'what purpose did seasonal monsoon winds have on trade',
  'annotations': [{'annotation_id': 4323936797498927989,
   'long_answer': {'candidate_index': -1, 'end_token': -1, 'start_token': -1},
   'short_answers': [],
   'yes_no_answer': 'NONE'},
  {'annotation_id': 13037645000009169623,
   'long_answer': {'candidate_index': -1, 'end_token': -1, 'start_token': -1},
   'short_answers': [],
   'yes_no_answer': 'NONE'},
  {'annotation_id': 4439059471919323171,
   'long_answer': {'candidate_index': -1, 'end_token': -1, 'start_token': -1},
   'short_answers': [],
   'yes_no_answer': 'NONE'},
  {'annotation_id': 15051359051424338858,
   'long_answer': {'candidate_index': 0, 'end_token': 161, 'start_token': 44},
   'short_answers': [{'end_token': 159, 'start_token': 140}],
   'yes_no_answer': 'NONE'},
  {'annotation_id': 5332861748513580580,
   'long_answer': {'candidate_index': 0, 'end_token': 161, 'start_token': 44},
   'short_answers': [],
   'yes_no_answer': 'NONE'}],
   'gold_has_long_answer': True,
   'gold_has_short_answer': False,
   'answer': {'long_answers': ["<P> The trade winds are the prevailing pattern of easterly surface winds found in the tropics , within the lower portion of the Earth 's atmosphere , in the lower section of the troposphere near the Earth 's equator . The trade winds blow predominantly from the northeast in the Northern Hemisphere and from the southeast in the Southern Hemisphere , strengthening during the winter and when the Arctic oscillation is in its warm phase . Trade winds have been used by captains of sailing ships to cross the world 's oceans for centuries , and enabled European empire expansion into the Americas and trade routes to become established across the Atlantic and Pacific oceans . </P>"],
  'short_answers': ['enabled European empire expansion into the Americas and trade routes to become established across the Atlantic and Pacific oceans']},
  'yes_no_answer': 'NONE'
    }
```

[data](https://ai.google.com/research/NaturalQuestions/download) | [paper](https://storage.googleapis.com/gweb-research2023-media/pubtools/4852.pdf) | [repo](https://github.com/google-research-datasets/natural-questions/tree/master)


## Usage

Assumes the install directions in the root folder's [README](./README.md) have been followed

Examples of reading questions in from each dataset are in the `scripts` folder, examples of how the datasets were processed is in `datasets/get_questions.py`. 

The `dev` versions of the datasets are all on github; the `train` versions are too large-- they will be uploaded to Azure/Google Drive and linked here when up. 