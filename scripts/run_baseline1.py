from pipeline.baseline.llm_query import LLMQuery
import datasets.get_questions as gq
from pathlib import Path
import os

with open(Path.home() / "api_keys" / "openai2.txt", "r") as f:
    os.environ["OPENAI_API_KEY"] = f.read()
f.close()

baseline = LLMQuery('gpt-4o-mini')

test_question = gq.process_dataset("hotpot", "fullwiki")



#Q = "What is the publication year of this paper?"
#A = "2018"
#P = [
#            "Michael Sharp. 2007. The sensual evaluation instrument:\nDeveloping a trans-cultural self-report measure of affect.\nInternational journal of human-computer studies 65, 4\n(2007), 315\u2013328.\n\n12. John F Kihlstrom, Eric Eich, Deborah Sandbrand, and\n\nBetsy A Tobias. 2000. Emotion and memory:\nImplications for self-report. The science of self-report:\nImplications for research and practice (2000), 81\u201399.\n\nCHI 2018 Paper CHI 2018, April 21\u201326, 2018, Montr\u00e9al, QC, CanadaPaper 253Page 9\f13. Kurt Lancaster. 2011. The Psychology of the Lens:\n\nPatrick Moreau creates \ufb01lmic intimacy with DSLRs at\nStillmotion. (June 2011).\n\n14. Kurt Lancaster. 2017. Using lenses to enhance visual\n\nstorytelling. (January 2017).",
#            "ACKNOWLEDGEMENT\nThis research was partially supported by the Advancing Well-\nbeing Initiative at the MIT Media Lab. We thank Asma Ghan-\ndeharioun, Weixuan (Vincent) Chen and Sam Spaulding for\ncomments that greatly improved the manuscript, and 3 \"anony-\nmous\" reviewers for their insights in presenting the research\nmethodology and results.\n\nREFERENCES\n\n1. Ruth A Baer, Gregory T Smith, Jaclyn Hopkins, Jennifer\nKrietemeyer, and Leslie Toney. 2006. Using self-report\nassessment methods to explore facets of mindfulness.\nAssessment 13, 1 (2006), 27\u201345.\n\n2. Joseph Bates and others. 1994. The role of emotion in\n\nbelievable agents. Commun. ACM 37, 7 (1994), 122\u2013125.\n\n3. Todd Bentley, Lorraine Johnston, and Karola von Baggo.",
#            "computing. Vol. 252. MIT press Cambridge.\n\n21. Tom Porter and Galyn Susman. 2000. On site: Creating\nlifelike characters in pixar movies. Commun. ACM 43, 1\n(2000), 25.\n\n22. Hans Rosling. 2006. Debunking third-world myths with\n\nthe best stats you\u2019ve ever seen. TED.\n\n23. Christian Roth, Peter Vorderer, and Christoph Klimmt.\n\n2009. The motivational appeal of interactive storytelling:\n\nTowards a dimensional model of the user experience. In\nJoint International Conference on Interactive Digital\nStorytelling. Springer, 38\u201343.\n\n24. Akane Sano. 2016. Measuring college students\u2019 sleep,\nstress, mental health and wellbeing with wearable\nsensors and mobile phones. Ph.D. Dissertation.\nMassachusetts Institute of Technology.\n\n25. Corina Sas, Tomasz Fratczak, Matthew Rees, Hans",
#            "30. AJN Van Breemen. 2004. Bringing robots to life:\nApplying principles of animation to robots. In\nProceedings of Shapping Human-Robot Interaction\nworkshop held at CHI 2004. 143\u2013144.\n\nCHI 2018 Paper CHI 2018, April 21\u201326, 2018, Montr\u00e9al, QC, CanadaPaper 253Page 10",
#            "15. Madelene Lindstr\u00f6m, Anna St\u00e5hl, Kristina H\u00f6\u00f6k, Petra\nSundstr\u00f6m, Jarmo Laaksolathi, Marco Combetto, Alex\nTaylor, and Roberto Bresin. 2006. Affective diary:\ndesigning for bodily expressiveness and self-re\ufb02ection. In\nCHI\u201906 extended abstracts on Human factors in\ncomputing systems. ACM, 1037\u20131042.\n\n16. Michael Mateas and Phoebe Sengers. 2003. Narrative\n\nintelligence. (2003).\n\n17. Robert R McCrae. 1984. Situational determinants of\n\ncoping responses: Loss, threat, and challenge. Journal of\npersonality and Social Psychology 46, 4 (1984), 919.\n\n18. David R Michael and Sandra L Chen. 2005. Serious\n\ngames: Games that educate, train, and inform. Muska &\nLipman/Premier-Trade.\n\n19. Rosalind W Picard and Shaundra Bryant Daily. 2005.\n\nEvaluating affective interactions: Alternatives to asking\nwhat users feel. In CHI Workshop on Evaluating Affective\nInterfaces: Innovative Approaches. ACM New York, NY,\n2119\u20132122.\n\n20. Rosalind W Picard and Roalind Picard. 1997. Affective"
#        ]

Q = test_question[0]['question']
A = test_question[0]['answer']


P = test_question[0]['context']


result = baseline.run(Q, A, P)
print(result)
print(baseline.llm_performance_history)
print(baseline.get_total_time())

