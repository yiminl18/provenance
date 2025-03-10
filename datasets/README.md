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


# MultiHop-RAG

`MultiHopRag.json` is a list of dicts, with each entry: 


```yaml
{'query': 'Who is the individual associated with the cryptocurrency industry facing a criminal trial on fraud and conspiracy charges, as reported by both The Verge and TechCrunch, and is accused by prosecutors of committing fraud for personal gain?',
 'answer': 'Sam Bankman-Fried',
 'question_type': 'inference_query',
 'evidence_list': [{'title': 'The FTX trial is bigger than Sam Bankman-Fried',
   'author': 'Elizabeth Lopatto',
   'url': 'https://www.theverge.com/2023/9/28/23893269/ftx-sam-bankman-fried-trial-evidence-crypto',
   'source': 'The Verge',
   'category': 'technology',
   'published_at': '2023-09-28T12:00:00+00:00',
   'fact': 'Before his fall, Bankman-Fried made himself out to be the Good Boy of crypto — the trustworthy face of a sometimes-shady industry.'},
  {'title': 'SBF’s trial starts soon, but how did he — and FTX — get here?',
   'author': 'Jacquelyn Melinek',
   'url': 'https://techcrunch.com/2023/10/01/ftx-lawsuit-timeline/',
   'source': 'TechCrunch',
   'category': 'technology',
   'published_at': '2023-10-01T14:00:29+00:00',
   'fact': 'The highly anticipated criminal trial for Sam Bankman-Fried, former CEO of bankrupt crypto exchange FTX, started Tuesday to determine whether he’s guilty of seven counts of fraud and conspiracy.'},
  {'title': 'Sam Altman backs teens’ startup, Google unveils the Pixel 8 and TikTok tests an ad-free tier',
   'author': 'Kyle Wiggers',
   'url': 'https://techcrunch.com/2023/10/07/sam-altman-backs-a-teens-startup-google-unveils-the-pixel-8-and-tiktok-tests-an-ad-free-tier/',
   'source': 'TechCrunch',
   'category': 'technology',
   'published_at': '2023-10-07T20:15:26+00:00',
   'fact': 'The prosecution painted Bankman-Fried as someone who knowingly committed fraud to achieve great wealth, power and influence, while the defense countered that the FTX founder acted in good faith, never meant to commit fraud or steal and basically got in over his head.'}]}

```

`corpus.json` is a list of dicts, with each entry: 

```yaml
{'title': "200+ of the best deals from Amazon's Cyber Monday sale",
 'author': None,
 'source': 'Mashable',
 'published_at': '2023-11-27T08:45:59+00:00',
 'category': 'entertainment',
 'url': 'https://mashable.com/article/cyber-monday-deals-amazon-2023',
 'body': "Table of Contents Table of Contents Echo, Fire TV, and Kindle deals Apple deals TV deals Laptop deals Headphone and earbud deals Tablet deals Gaming deals Speaker deals Vacuum deals Kitchen deals Smart home deals Fitness deals Beauty tech deals Drone deals Camera deals Lego deals Gift card deals\n\nUPDATE: Nov. 27, 2023, 5:00 a.m. EST This post has been updated with all of the latest Cyber Monday deals available at Amazon.\n\nAmazon is dragging out the year\'s biggest shopping holiday(s) into 11 days of deals.\n\nThe retail giant began its Black Friday sale in the early morning of Friday, Nov. 17 (a week ahead of schedule) and was on top of making the switch to Cyber Monday language in the wee hours of Saturday, Nov. 25. Official Cyber Monday mode, which is currently on through Monday, Nov. 27, includes both a ton of deals carried over from Black Friday plus some new ones.\n\nWe\'re curating a running list of Amazon\'s best Cyber Weekend deals, spotlighting some of our favorites and noting when good deals inevitably sell out. Read on for the full rundown, and check back often: We\'re going to be updating this story incessantly as the sale continues, as well as our even bigger (if you can imagine) list of Cyber Monday deals across more retailers.\n\nNote: All newly added deals are marked with a ✨, while deals with a 🔥 have dropped to an all-time low price. Amazon\'s invite-only deals for Prime members are marked with a 📨. Deals with a strikeout were either sold out or expired at the time of writing.\n\nEcho, Fire TV, and Kindle deals\n\nWhy we like it\n\nAn Echo Show is a subtle yet game-changing addition to any room — and for less than $40 with this rollover Black Friday to Cyber Monday deal, there\'s little reason to not make your life easier. The smart screen responds to Alexa commands that are particularly handy when your hands are full, like asking for measurement conversions mid-cooking, checking the weather mid-rushing out the door, or turning off your smart lights with a sleeping kid in hand. Plus, it\'s got a 5.5-inch screen and better sound than its predecessor, making it perfect for watching videos or video calling friends and family.\n\nMore Amazon device and service deals\n\nAmazon services\n\nAudible Premium Plus — $5.95/month $14.95/month for four months (save $9/month; new customers only; get an additional $20 Audible credit)\n\nEcho Buds\n\nEcho smart displays\n\nEcho smart speakers\n\nFire tablets\n\nFire TVs\n\nNote: All Fire TVs come with a free 6-month subscription to MGM+ (a $35.94 value).\n\nFire TV streaming devices\n\neero\n\nKindles\n\nMiscellaneous Amazon devices\n\nApple deals\n\nWhy we like it\n\nNow that the 64GB 9th generation iPad has been going in and out of stock (you might be able to find it on sale for $229.99), our new favorite iPad deal at Amazon is the 10th generation 64GB model for $349. Compared to the 9th gen, the 10th gen classic iPad has a slightly bigger screen that\'s now also a Liquid Retina display (10.9 inches versus 10.2 inches), a faster A14 Bionic chip for smoother multitasking, and USB-C charging.\n\nMore Apple deals\n\nAirPods\n\nMacBook\n\nMac\n\niPad\n\nApple Watch\n\nTV deals\n\nWhy we like it\n\nThis 65-inch Fire TV from Amazon hit its lowest ever price this month, and we\'re not mad about it. With a 66 percent five-star review rating, it\'s got much to love: Including stunning 4K QLED resolution, adaptive brightness that adjusts to the lighting of your room, the ability to project famous art or personal pics on it when not streaming anything, and, of course, that quintessential Alexa voice control.\n\nMore TV deals\n\n43 to 55 inches\n\n65 inches\n\n75 to 85 inches\n\nLaptop deals\n\nWhy we like it\n\nMacBooks aside (which are all listed above in the Apple section), another stellar Cyber Monday laptop deal at Amazon is the lightweight Microsoft Surface Laptop Go 3 for $599.99. This 25% discount drops the 2023 version to the regular asking price of our favorite budget laptop, the older Surface Go 2. Compared to the Go 2, the Go 3\'s Intel Core i5 processor is 12th gen versus the Go 2\'s 11th gen, harnessing better speeds and solid power for most everyday work or school tasks. On the outside, the Go 3 is definitely giving MacBook Air — the main difference being that the Go 3\'s screen is a touchscreen.\n\nMore laptop deals\n\nTraditional laptops\n\n2-in-1 laptops\n\nChromebooks\n\nGaming laptops\n\nHeadphone and earbud deals\n\nWhy we like it\n\nNarrowing down a headphones upgrade from so many on-sale options is less overwhelming when you\'ve confirmed that you want to stick with a super premium, super reputable brand like Bose — but also that you want to stick to a budget. There\'s only one pair of Bose over-ear headphones you can grab for just under $200, and that\'s the QuietComfort 45s at a record-low price of $199. This classic pair secures top-of-the-line ANC, 20 hours of battery life, and all-day comfort for less than half of the AirPods Max\'s sale price.\n\nMore headphone and earbud deals\n\nHeadphones\n\nEarbuds\n\nTablet deals\n\nGaming deals\n\nGaming headsets\n\nMashable Deals Want more hand-picked deals in your inbox? Sign up for Mashable\'s daily Deals newsletter. Loading... Sign Me Up By signing up you agree to our Terms of Use and Privacy Policy Thanks for signing up!\n\nGaming mice\n\nGaming keyboards\n\nVR headsets\n\nMeta Quest 2 — $249 $299.99 (save $50.99) + free $50 Amazon credit with code META50 🔥\n\nSpeaker deals\n\nVacuum deals\n\nCordless vacuums\n\nRobot vacuums and vacuum/mop hybrids\n\nKitchen deals\n\nPizza ovens\n\nSparkling water makers\n\nToaster ovens\n\nSmart home deals\n\nNote: Echo devices are listed above under "Amazon device and service deals."\n\nBlink\n\nChromecast\n\nGoogle Nest\n\nFitness deals\n\nSmartwatches and fitness trackers\n\nNote: Apple Watches are listed above under "Apple deals."\n\nBeauty tech deals\n\nDrone deals\n\nCamera deals\n\nGoPro\n\nLego deals\n\nGift card deals"}
```

## Usage

Assumes the install directions in the root folder's [README](./README.md) have been followed

Examples of reading questions in from each dataset are in the `scripts` folder, examples of how the datasets were processed is in `datasets/get_questions.py`. 

The `dev` versions of the datasets are all on github; the `train` versions are too large-- they will be uploaded to Azure/Google Drive and linked here when up. 