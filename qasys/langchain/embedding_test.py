from pretrain_sentence_splitter import nltk_sent_tokenize_for_list, get_token_num_for_list
from langchain.docstore.document import Document
from indexing import store_splits
import logging
from setup_logging import setup_logging, close_logging

logger, file_handler, console_handler, timestamp = setup_logging()

raw_provenance = [
            "Public Works Commission\nAgenda Report\n\nPublic Works\nCommission Meeting\n10-27-21\nItem\n4.A.\n\nTo:\n\nChair Simmens and Members of the Public Works Commission\n\nPrepared by:\n\nTroy Spayd, Assistant Public Works Director/City Engineer\n\nApproved by:\n\nRob DuBoux, Public Works Director/City Engineer\n\nDate prepared: October 21, 2021\n\nMeeting date: October 27, 2021\n\nSubject:\n\nCapital Improvement Projects and Disaster Recovery Projects Status\nReport\n\nRECOMMENDED ACTION: Receive and file report on the status of the City\u2019s current and\nupcoming Capital Improvements Projects and Disaster Recovery Projects.\n\nDISCUSSION: Staff will provide a status update on the following active projects in the\nFiscal Year 2021-2022 Capital Improvement Program:\n\nCapital Improvement Projects (Design)\n\nMarie Canyon Green Streets\n(cid:190) Updates:",
            "Westward Beach Road Improvements Project\n\n(cid:190) Updates:\n\n(cid:131) The design plans were approved by Planning Commission on\nSeptember 20, 2021. At the December 13, 2021, City Council meeting,\nCouncil directed staff to withdraw the proposed project and associated\nCoastal Development Permit and directed the Public Works and Public\nSafety Commissions\nto develop project\nalternatives. A joint Public Works and Public Safety Commission\nmeeting was held on January 20, 2022. Project alternatives will be\npresented to the commissions at a future date.\n\nthe project\n\nto review\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Spring 2022\n(cid:131) Begin Construction: Summer/Winter 2022\n\nCivic Center Water Treatment Facility Phase 2\n\n(cid:190) Updates:\n(cid:131)\n\nIndividual letters were mailed to all properties within Phase 2 with their\npreliminary estimated assessments. Staff has been communicating\nwith the property owners regarding their proposed assessments.",
            "Broad Beach Road Water Quality Infrastructure Repairs (CalJPIA Project)\n\n(cid:190) Updates:\n\n(cid:131) The project consultant prepared the specifications for the project. Staff\n\nis finalizing the bid documents.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: February 2022\n(cid:131) Begin Construction: Spring 2022\n\nLatigo Canyon Road Roadway/Retaining Wall Improvements (FEMA Project)\n\n(cid:190) Updates:\n\n(cid:131) Staff is finalizing the design of this project.\n(cid:131) Staff is also working with FEMA/CalOES to substitute the existing\n\ntimber with non-combustible materials.\n\n(cid:190) Project Schedule\n\n(cid:131) Complete Design: February 2022\n(cid:131) Begin Construction: April 2022\n\nTrancas Canyon Park Planting and Irrigation Repairs (CalJPIA/FEMA Project)\n\n(cid:190) Updates:\n\n(cid:131) The project consultant has started the design of this project.\n\n(cid:190) Project Schedule:\n\n(cid:131) Complete Design: Spring 2022\n(cid:131) Begin Construction: Spring 2022",
            "(cid:190) Project Description: This project was identified in the 2015 PCH Safety Study\nand includes installing new raised medians and improvements. New raised\nmedians are proposed east and west of PCH and Paradise Cove Road. The\nproposed improvements also include the relocation of the existing bus stop\nand new signage. The project will also include the installation of new raised\nmedians on PCH in the areas where the double yellow lines exist in the vicinity\nof Zuma Beach, specifically where the yellow paddles are installed.\n\nCapital Improvement Projects (Completed)\n\nCivic Center Way Improvements\n\n(cid:190) Updates: The contractor has completed the planting material maintenance\nperiod as described within the project documents. Council accepted this\nproject as complete at the September 13th City Council Meeting.\n\nCivic Center Stormwater Diversion Structure",
            "(cid:190) Updates: The contractor has completed the storm drain improvements in the\nCivic Center Way are. The improvements modified the existing concrete\nchannel underneath Civic Center Way by adding a 3\u2019 concrete curb adjacent\nto the existing flap gates. The new curb prevents brackish water intrusion\n\nPage 4 of 8\n\nAgenda Item # 4.A.\n\n\n\n\n\n\n\n\n\n\n\n\ninto the City\u2019s Civic Center Stormwater Treatment Facility. This project is\nscheduled to be accepted by the Council at the January 24, 2022 meeting.\n\n2021 Annual Street Maintenance\n\n(cid:190) Updates: This project included resurfacing Malibu Road, Broad Beach Road,\nLatigo Canyon Road, Corral Canyon Road, Webb Way, Rambla Pacifico\nStreet and Vista Pacifica with a slurry seal treatment and adding speed\nhumps to Birdview Avenue. This project was identified in the City\u2019s Pavement\nManagement Plan. This project is scheduled to be accepted by the Council\nat the January 24, 2022 meeting.\n\nDisaster Projects (Design)"
        ]

extracted_search_list = [
            "names",
            "Marie Canyon Green Streets",
            "Civic Center Way Improvements",
            "capital improvement projects",
            "Westward Beach Road Improvements Project",
            "Latigo Canyon Roadway/Retaining Wall Improvements",
            "Trancas Canyon Park Planting and Irrigation Repairs"
        ]

sentences = nltk_sent_tokenize_for_list(raw_provenance, 10)

total_token_num = get_token_num_for_list(sentences)
all_splits = [Document(page_content=s, metadata={"source": "local"}) for s in sentences]
vector_store = store_splits(all_splits)
searched_docs = []

for extracted_search in extracted_search_list:
            searched_docs+=vector_store.similarity_search_with_score(extracted_search, k=30) # using large k to return all chunks' score, then we can filter by threshold. # return is a list of tuple, (Document, score) 
            logging.info(f"searched_docs: {searched_docs}")


close_logging(logger, [file_handler, console_handler])